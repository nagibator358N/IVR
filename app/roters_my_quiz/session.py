import json
from fastapi import APIRouter, Request, Response
from sqlalchemy.sql.expression import func
from sqlalchemy import and_
from app.database.entities import Quiz
from app.database.entities import QuizQuestion
from app.database.entities import User
from app.database.entities import QuestionAnswer
from app.database.entities import QuestionUserAnswerChoice
from app.database.entities import QuestionUserAnswerText
from app.database.entities import QuizCreator
from app.usermodels.models import QuizSession
from app.usermodels.models import Points
from app.usermodels.models import UserAnswer
from datetime import datetime as dt
from app.db.database import SessionLocal
import app.constants.session_constants as constant
router = APIRouter()


def question_randomizer(quiz_id):
    with SessionLocal() as session:
        quiz = session.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
        if quiz is None:
            return f"Тест с quiz_id {quiz_id} не найден."
        q_am_to_comp = quiz.questions_amount_to_complete
        if quiz.question_easy is not None:
            quiz.question_easy = quiz.question_easy
        else:
            quiz.question_easy = (q_am_to_comp)//3
        if quiz.question_medium is not None:
            quiz.question_medium = quiz.question_medium
        else:
            quiz.question_medium = (q_am_to_comp)//3
        if quiz.question_hard is not None:
            quiz.question_hard = quiz.question_hard
        else:
            quiz.question_hard = q_am_to_comp-quiz.question_easy
            quiz.question_hard = quiz.question_hard-quiz.question_medium
        list_easy = session.query(QuizQuestion.id).filter(and_(
            QuizQuestion.quiz_id == quiz_id,
            QuizQuestion.question_difficulty == 1)).order_by(
                func.random()).limit(quiz.question_easy).all()
        list_medium = session.query(QuizQuestion.id).filter(and_(
            QuizQuestion.quiz_id == quiz_id,
            QuizQuestion.question_difficulty == 2)).order_by(
                func.random()).limit(quiz.question_medium).all()
        list_hard = session.query(QuizQuestion.id).filter(and_(
            QuizQuestion.quiz_id == quiz_id,
            QuizQuestion.question_difficulty == 3)).order_by(
                func.random()).limit(quiz.question_hard).all()
        generated = list_easy+list_medium+list_hard
        print(quiz.question_easy)
        print(quiz.question_medium)
        print(quiz.question_hard)
        list_id = []
        for row in generated:
            list_id.append(row[0])
        if len(list_id) < quiz.questions_amount_to_complete:
            more_questions = session.query(QuizQuestion.id).filter(and_(
                QuizQuestion.quiz_id == quiz_id,
                QuizQuestion.id.notin_(list_id))).order_by(
                    func.random()).limit(
                        quiz.questions_amount_to_complete-len(list_id)).all()
            generated += more_questions
        result = []
        for row in generated:
            result.append(row[0])
        return result

# Начало сессии


@router.post("/session/user/{user_id}/start_quiz/{quiz_id}/")
async def start_quiz(response: Response, user_id: int, quiz_id: int):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not (user):
            error = f"Пользователь с id {user_id} не существует"
            return {"success": 0, "error": error}
        quiz = session.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
        if not (quiz):
            error = f"Тест с id {quiz_id} не существует"
            return {"success": 0, "error": error}
        if (quiz.questions_amount == 0):
            error = f"Тест с id {quiz_id} не содержит вопросов"
            return {"success": 0, "error": error}
        quiz_session = QuizSession()
        quiz_session.user_id = user_id
        quiz_session.quiz_id = quiz_id
        quiz_session.question_index = -1
        quiz_session.beginning_time = dt.now()
        quiz_session.questions_ids = json.dumps(question_randomizer(quiz_id))
        session.add(quiz_session)
        session.commit()
        question_list = json.loads(quiz_session.questions_ids)
        print(f"Количество вопросов:{question_list}")
        response.set_cookie(key="quiz_session_id", value=quiz_session.id)
        return {"success": 1, "data": {"session_id": quiz_session.id,
                                       "question_amount": len(question_list)}}

# Получение следующего вопроса сессии


@router.get("/get_next_question/{session_id}")
async def get_next_question(session_id: int):
    with SessionLocal() as db:
        session = db.query(QuizSession).filter_by(id=session_id).first()
        if not session:
            error = f"Сессия с id {session_id} не существует"
            return {"success": 0, "error": error}
        quiz = db.query(Quiz).filter_by(quiz_id=session.quiz_id).first()
        if not quiz:
            return {"success": 0, "error": constant.TEST_NOT_FOUND}
        next_question_id = session.question_index+1
        all_question_ids = json.loads(session.questions_ids)
        print(type(all_question_ids))
        session.question_index += 1
        if len(all_question_ids) <= next_question_id:
            return {"success": 0, "error": constant.FINISHED_QUESTIONS}
        question = db.query(QuizQuestion).filter_by(
            id=all_question_ids[next_question_id]).first()
        answers = db.query(QuestionAnswer).filter_by(
            question_id=question.id).all()
        db.commit()
        answers_list_for_question = []
        for i in answers:
            answers_list_for_question.append(
                {"id": i.id, "answer_text": i.answer_text})
        q_with_choice = question.question_type
        q_mulitple_choice = False
        if q_with_choice == 2:
            q_mulitple_choice = True
        if q_with_choice == 1 or q_with_choice == 2:
            q_with_choice = True
        else:
            q_with_choice = False
        return {"success": 1, "data": {
            "session_id": session_id,
            "question_total_amount": len(all_question_ids),
            "question_number": session.question_index,
            "question_id": question.id,
            "question_text": question.question_text,
            "answer_list": answers_list_for_question,
            "question_hint": question.question_hint,
            "question_with_choice": q_with_choice,
            "question_multiple_choice": q_mulitple_choice
        }}
# Окончание сессии


@router.post("/end_session/{session_id}")
async def end_session(session_id: int):
    with SessionLocal() as db:
        session = db.query(QuizSession).filter_by(id=session_id).first()
        if not session:
            error = f"Сессия с id {session_id} не существует"
            return {"success": 0, "error": error}
        session.finishing_time = dt.now()
        session.total_time = (session.finishing_time -
                              session.beginning_time).total_seconds()
        print(session.total_time)
        db.commit()
        result = session.result
        return {"success": 1, "data": {"completed": True, "result": result}}


# Сохранение ответов
@router.post("/set_answers/")
async def set_answers(request: Request, body: UserAnswer):
    with SessionLocal() as db:
        session_id = request.cookies.get('quiz_session_id')
        session = db.query(QuizSession).filter_by(id=session_id).first()
        if not session:
            error = f"Сессия с id {session_id} не существует"
            return {"success": 0, "error": error}
        if session.result is None:
            session.result = 0
        question_id = json.loads(session.questions_ids)[session.question_index]
        question = db.query(QuizQuestion).filter_by(id=question_id).first()
        if not question:
            error = f"Вопрос с id {question_id} не найден"
            return {"success": 0, "error": error}
        if question.question_type == 1:
            answer = db.query(QuestionAnswer).filter_by(
                id=body.answers[0]).first()
            answers = QuestionUserAnswerChoice()
            answers.session_id = session_id
            answers.question_id = question_id
            answers.answer_id = body.answers[0]
            answers.answer_correct = answer.answer_correct
            answers.answer_points = answer.answer_points
            session.result += answer.answer_points
            db.add(answers)
        elif question.question_type == 2:
            for i in body.answers:
                answer = db.query(QuestionAnswer).filter_by(id=i).first()
                answers = QuestionUserAnswerChoice()
                answers.session_id = session_id
                answers.question_id = question_id
                answers.answer_id = i
                answers.answer_correct = answer.answer_correct
                answers.answer_points = answer.answer_points
                session.result += answer.answer_points
                db.add(answers)
        elif question.question_type == 3:
            answers = QuestionUserAnswerText()
            answers.session_id = session_id
            answers.question_id = question_id
            answers.answer = body.text_answer
            answers.answer_points = 0
            db.add(answers)
        db.commit()
        return {"success": 1}
# Получение результатов пользователя


@router.get("/session_list/{user_id}")
async def get_all_sesions_for_user(request: Request, user_id: int):
    with SessionLocal() as db:
        sessions = db.query(QuizSession).filter_by(user_id=user_id).filter(
            QuizSession.finishing_time.isnot(None)).all()
        list_sessions = []
        for i in sessions:
            quiz = db.query(Quiz).filter_by(quiz_id=i.quiz_id).first()
            if not (quiz):
                continue
            list_sessions.append(
                {
                    "quiz_name": quiz.quiz_name,
                    "quiz_id": i.quiz_id,
                    "beginning_time": i.beginning_time,
                    "finishing_time": i.finishing_time,
                    "total_time": round(i.total_time),
                    "result": i.result,
                    "session_id": i.id
                }
            )
        return {"success": 1, "data": list_sessions}

# Получение вопросов в сесии для отображения результатов


@router.get("/questions_for_session/{session_id}")
async def get_results_for_session(request: Request, session_id: int):
    with SessionLocal() as db:
        session = db.query(QuizSession).filter_by(id=session_id).first()
        if not (session):
            error = f"Сессии с id {session_id} не существует"
            return {"success": 0, "error": error}
        question_ids = json.loads(session.questions_ids)
        list_result = []
        for i in range(0, len(question_ids)):
            q_ans_choice = db.query(QuestionUserAnswerChoice).filter_by(
                session_id=session_id).filter_by(
                    question_id=question_ids[i]).all()
            points = 0
            if len(q_ans_choice) > 0:
                for x in q_ans_choice:
                    points += x.answer_points
            else:
                q_ans_text = db.query(QuestionUserAnswerText).filter_by(
                    session_id=session_id).filter_by(
                        question_id=question_ids[i]).first()
                if q_ans_text:
                    points += q_ans_text.answer_points
            list_result.append(points)
        data = []
        for i in range(1, len(list_result)+1):
            data.append(
                {
                    "question_number": i,
                    "question_points": list_result[i-1]
                }
            )
        return {"success": 1, "data": data}


# Получение вопросов в сесии для отображения статистики
@router.get("/question_for_session_creator/{session_id}")
async def get_results_for_session_creator(request: Request, session_id: int):
    with SessionLocal() as db:
        session = db.query(QuizSession).filter_by(id=session_id).first()
        if not (session):
            error = f"Сессии с id {session_id} не существует"
            return {"success": 0, "error": error}
        question_ids = json.loads(session.questions_ids)
        data = []
        counter = 1
        for i in range(0, len(question_ids)):
            question = db.query(QuizQuestion).filter_by(
                id=question_ids[i]).first()
            if not question:
                continue
            points = 0
            q_ans_choice = db.query(QuestionUserAnswerChoice).filter_by(
                session_id=session_id).filter_by(
                    question_id=question_ids[i]).all()
            if len(q_ans_choice) > 0:
                for x in q_ans_choice:
                    points += x.answer_points
                data.append(
                    {
                        "question_number": counter,
                        "question_text": question.question_text,
                        "question_points": points,
                        "answer_checked": True
                    }
                )
            else:
                q_ans_text = db.query(QuestionUserAnswerText).filter_by(
                    session_id=session_id).filter_by(
                        question_id=question_ids[i]).first()
                if q_ans_text:
                    points += q_ans_text.answer_points
                    data.append(
                        {
                            "question_number": counter,
                            "question_text": question.question_text,
                            "question_points": points,
                            "user_answer": q_ans_text.answer
                        }
                    )
            counter += 1
        return {"success": 1, "data": data}

# Добавление баллов


@router.post("/set_points/{session_id}/{question_number}")
async def set_points(request: Request, response: Response,
                     body: Points, session_id: int, question_number: int):
    with SessionLocal() as db:
        session = db.query(QuizSession).filter_by(id=session_id).first()
        if not (session):
            response.status_code = 404
            return {"success": 0, "error": constant.SESSION_NOT_FOUND}
        list_questions_ids = json.loads(session.questions_ids)
        question_id = list_questions_ids[question_number-1]
        answer = db.query(QuestionUserAnswerText).filter_by(
            session_id=session_id).filter_by(question_id=question_id).first()
        if not (answer):
            response.status_code = 404
            return {"success": 0, "error": constant.ANSWER_NOT_FOUND}
        session.result = session.result-answer.answer_points+body.points
        answer.answer_points = body.points
        answer.answer_correct = True
        db.commit()
        return {"success": 1}
# Получение сесии по id


@router.get("/get_session_by_id/{session_id}")
async def get_session_by_id(request: Request, session_id: int):
    with SessionLocal() as db:
        session = db.query(QuizSession).filter_by(id=session_id).filter(
            QuizSession.finishing_time.isnot(None)).first()
        if not (session):
            error = f"Сессии с id {session_id} не существует или не завершена"
            return {"success": 0, "error": error}
        quiz_name = (db.query(Quiz).filter_by(
            quiz_id=session.quiz_id).first()).quiz_name
        user_email = (db.query(User).filter_by(
            id=session.user_id).first()).email
        data = {
            "quiz_name": quiz_name,
            "quiz_id": session.quiz_id,
            "user_email": user_email,
            "user_id": session.user_id,
            "beginning_time": session.beginning_time,
            "finishing_time": session.finishing_time,
            "total_time": round(session.total_time),
            "result": session.result,
            "session_id": session.id
        }
    return {"success": 1, "data": data}

# Получение средниих результатов и кол-ва попыток на тест


@router.get("/get_session_results_and_amount/{quiz_id}")
async def get_session_results_and_amount(request: Request, quiz_id: int):
    with SessionLocal() as db:
        session = db.query(QuizSession).filter_by(quiz_id=quiz_id).filter(
            QuizSession.finishing_time.isnot(None)).all()
        results_sum = 0
        results_am = 0
        session_amount = 0
        for x in session:
            result = x.result
            if result is not None:
                results_sum += result
                results_am += 1
            session_amount += 1
        if results_am == 0:
            results_am = 1
    return {"success": 1, "data": {
        "medium_result": results_sum//results_am,
        "session_amount": session_amount
    }}

# Получение всех сесии юзера на тест


@router.get("/all_sessions/{user_id}/{quiz_id}")
async def get_all_sesions_for_quiz(request: Request, user_id: int,
                                   quiz_id: int):
    with SessionLocal() as db:
        creator_id = (db.query(QuizCreator).filter_by(
            user_id=user_id).first()).id
        if creator_id is None:
            error = f"Создатель с user_id {user_id} не существует"
            return {"success": 0, "error": error}
        quiz = db.query(Quiz).filter_by(creator_id=creator_id).all()
        if quiz is None:
            error = f"Пользователь с id {user_id} пока не создал тест"
            return {"success": 0, "error": error}
        list_sessions = []
        sessions = db.query(QuizSession).filter_by(quiz_id=quiz_id).filter(
            QuizSession.finishing_time.isnot(None)).all()
        for i in sessions:
            quiz_name = (db.query(Quiz).filter_by(
                quiz_id=i.quiz_id).first()).quiz_name
            user_email = (db.query(User).filter_by(id=i.user_id).first()).email
            list_sessions.append(
                {
                    "quiz_name": quiz_name,
                    "quiz_id": i.quiz_id,
                    "user_email": user_email,
                    "user_id": i.user_id,
                    "beginning_time": i.beginning_time,
                    "finishing_time": i.finishing_time,
                    "total_time": round(i.total_time),
                    "result": i.result,
                    "session_id": i.id
                }
            )
        return {"success": 1, "data": list_sessions}
