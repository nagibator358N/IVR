from fastapi import APIRouter, Response
from sqlalchemy import asc
from app.database.entities import User
from app.database.entities import QuizCreator
from app.database.entities import Quiz
from app.database.entities import QuizQuestion
from app.usermodels.models import AddQuizRequest
from app.usermodels.models import UpdateQuizRequest
from app.usermodels.models import AddQuizQuestion
from datetime import datetime as dt
import app.constants.tests_constants as constant
from app.db.database import SessionLocal
router = APIRouter()

# Добавление теста


@router.post("/quiz/add/", status_code=201)
async def add_quiz(response: Response, body: AddQuizRequest):
    with SessionLocal() as session:
        cond_1 = body.question_easy is not None
        cond_2 = body.question_medium is not None
        cond_3 = body.question_hard is not None
        if cond_1 and cond_2 and cond_3:
            if body.question_easy + body.question_medium + \
                    body.question_hard > body.questions_amount_to_complete:
                response.status_code = 400
                return {
                    "success": 0,
                    "error": constant.Q_AM_TO_COMP}
        if body.creator_id is not None or body.user_id is not None:
            if body.user_id is not None:
                user = session.query(User).filter(
                    User.id == body.user_id).first()
                if not (user):
                    error = f"Пользователь с id: {body.user_id}"
                    error += " не найден в базе данных"
                    return {"success": 0, "error": error}
                creator = session.query(QuizCreator).filter(
                    QuizCreator.user_id == body.user_id).first()
                if not (creator):
                    creator = QuizCreator()
                    creator.user_id = body.user_id
                    session.add(creator)
                    session.commit()
            if body.creator_id is not None:
                creator = session.query(QuizCreator).filter(
                    QuizCreator.id == body.creator_id).first()
                if not (creator):
                    error = f"Пользователь с id {body.creator_id}"
                    error += " не найден в базе данных"
                    return {
                        "success": 0, "error": error}
        else:
            return {
                "success": 0,
                "error": constant.US_CR_ID_MISS}
        quiz = Quiz()
        quiz.creator_id = creator.user_id
        print(creator.user_id)
        quiz.quiz_name = body.quiz_name
        quiz.questions_amount_to_complete = body.questions_amount_to_complete
        quiz.quiz_description = body.quiz_description
        quiz.duration = body.duration
        quiz.created_date = dt.now()
        quiz.quiz_tries = body.quiz_tries
        quiz.show_ans_res = body.show_ans_res
        print(quiz.show_ans_res)
        quiz.quiz_mark_type = body.quiz_mark_type
        quiz.question_switch = body.question_switch
        quiz.reanswer = body.reanswer
        quiz.question_easy = body.question_easy
        quiz.question_medium = body.question_medium
        quiz.question_hard = body.question_hard
        session.add(quiz)
        session.commit()
        return {
            "success": 1,
            "data": {
                "id": quiz.quiz_id,
                "name": quiz.quiz_name}}

# Удаление теста


@router.delete("/quiz/{id}/delete", status_code=200)
async def remove_quiz_by_index(response: Response, id: int):
    with SessionLocal() as session:
        quiz = session.query(Quiz).filter(Quiz.quiz_id == id).first()
        if not (quiz):
            response.status_code = 404
            return {"success": 0, "error": f"Тест с id {id} не существует"}
        session.query(QuizQuestion).filter(QuizQuestion.quiz_id == id).delete()
        session.delete(quiz)
        session.commit()
        return {"success": 1, "data": id}

# Изменение теста


@router.put("/quiz/{id}/update", status_code=200)
async def update_quiz(response: Response, body: UpdateQuizRequest, id: int):
    with SessionLocal() as session:
        cond_1 = body.question_easy is not None
        cond_2 = body.question_medium is not None
        cond_3 = body.question_hard is not None
        if cond_1 and cond_2 and cond_3:
            if body.question_easy + body.question_medium + \
                    body.question_hard > body.questions_amount_to_complete:
                response.status_code = 400
                return {
                    "success": 0,
                    "error": constant.Q_AM_TO_COMP}
        quiz = session.query(Quiz).filter(Quiz.quiz_id == id).first()
        if quiz:
            if body.questions_amount_to_complete is not None:
                q_am_to_comp = body.questions_amount_to_complete
                quiz.questions_amount_to_complete = q_am_to_comp
            if body.quiz_description is not None:
                quiz.quiz_description = body.quiz_description
            if body.quiz_name is not None:
                quiz.quiz_name = body.quiz_name
            if body.duration is not None:
                quiz.duration = body.duration
            if body.quiz_tries is not None:
                quiz.quiz_tries = body.quiz_tries
            if body.show_ans_res is not None:
                quiz.show_ans_res = body.show_ans_res
            if body.quiz_mark_type is not None:
                quiz.quiz_mark_type = body.quiz_mark_type
            if body.question_switch is not None:
                quiz.question_switch = body.question_switch
            if body.reanswer is not None:
                quiz.reanswer = body.reanswer
            session.commit()
            return {"success": 1, "data": quiz.quiz_id}
        response.status_code = 404
        return {"success": 0, "error": f"Тест с id {id} не существует"}

# Получение списка всех тестов


@router.get("/quiz/all", status_code=200)
async def get_quiz_list():
    with SessionLocal() as session:
        list_quiz = session.query(Quiz).all()
        result = []
        for quiz in list_quiz:
            q_am_to_comp = quiz.questions_amount_to_complete
            if quiz.questions_amount >= q_am_to_comp:
                result.append(
                    {
                        "id": quiz.quiz_id,
                        "creator": {
                            "user_id": quiz.creator.user.id,
                            "user_email": quiz.creator.user.email,
                            "creator_id": quiz.creator.id},
                        "quiz_name": quiz.quiz_name,
                        "quiz_description": quiz.quiz_description,
                        "duration": quiz.duration,
                        "question_amount": quiz.questions_amount,
                        "questions_amount_to_complete": q_am_to_comp,
                        "created_date": quiz.created_date,
                        "quiz_tries": quiz.quiz_tries,
                        "show_ans_res": quiz.show_ans_res,
                        "mark_type": quiz.quiz_mark_type,
                        "question_switch": quiz.question_switch,
                        "reanswer": quiz.reanswer})
        return {"success": 1, "data": result}

# Получение теста по id


@router.get("/quiz/{id}", status_code=200)
async def get_quiz_by_id(response: Response, id: int):
    with SessionLocal() as session:
        quiz = session.query(Quiz).filter(Quiz.quiz_id == id).first()
        if not (quiz):
            response.status_code = 404
            return {"success": 0, "error": f"Тест с id {id} не существует"}
        q_am_to_comp = quiz.questions_amount_to_complete
        return {
            "success": 1,
            "data": {
                "id": quiz.quiz_id,
                "creator": {
                    "user_id": quiz.creator.user.id,
                    "user_email": quiz.creator.user.email,
                    "creator_id": quiz.creator.id},
                "quiz_name": quiz.quiz_name,
                "quiz_description": quiz.quiz_description,
                "duration": quiz.duration,
                "question_amount": quiz.questions_amount,
                "questions_amount_to_complete": q_am_to_comp,
                "created_date": quiz.created_date,
                "quiz_tries": quiz.quiz_tries,
                "show_ans_res": quiz.show_ans_res,
                "mark_type": quiz.quiz_mark_type,
                "question_switch": quiz.question_switch,
                "reanswer": quiz.reanswer,
                "question_easy": quiz.question_easy,
                "question_medium": quiz.question_medium,
                "question_hard": quiz.question_hard}}

# Получение списка вопросов на тест


@router.get("/quiz/{id}/question_list", status_code=200)
async def get_question_list_by_quiz_id(response: Response, id: int):
    with SessionLocal() as session:
        quiz = session.query(Quiz).filter(Quiz.quiz_id == id).first()
        if not (quiz):
            response.status_code = 404
            return {"success": 0, "error": f"Тест с id {id} не существует"}
        list_questions = session.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == id).order_by(asc(
                QuizQuestion.question_number)).all()
        result = []
        for question in list_questions:
            result.append({
                "id": question.id,
                "question_text": question.question_text,
                "question_description": question.question_description,
                "question_time": question.question_time,
                "question_points": question.question_points,
                "question_type": question.question_type,
                "quiz_id": question.quiz_id,
                "question_number": question.question_number,
                "question_difficulty": question.question_difficulty,
                "question_hint": question.question_hint
            })
        return {"success": 1, "data": result}

# Добавление вопроса в тест


@router.post("/quiz/question/add", status_code=201)
async def add_question(response: Response, body: AddQuizQuestion):
    with SessionLocal() as session:
        question = QuizQuestion()
        question.question_text = body.question_text
        question.question_description = body.question_description
        question.question_time = body.question_time
        question.question_points = body.question_points
        print(2)
        question.question_type = body.question_type
        print(1)
        question.quiz_id = body.quiz_id
        question.question_number = body.question_number
        question.question_difficulty = body.question_difficulty
        question.question_hint = body.question_hint
        session.add(question)
        quiz = session.query(Quiz).filter(Quiz.quiz_id == body.quiz_id).first()
        quiz.questions_amount += 1
        session.commit()
        return {"success": 1, "data": {"id": question.id}}


@router.get("/quiz/all/{user_id}", status_code=200)
async def get_quiz_list_by_user(user_id: int):
    with SessionLocal() as session:
        quiz_creator = session.query(QuizCreator).filter(
            QuizCreator.user_id == user_id).first()
        if not (quiz_creator):
            return {
                "success": 0,
                "error": "Вы пока не создали ни одного теста"}
        creator_id = quiz_creator.id
        list_quiz = session.query(Quiz).filter(
            Quiz.creator_id == creator_id).all()
        if not (list_quiz):
            return {"success": 1, "data": []}
        result = []
        i = 0
        for quiz in list_quiz:
            q_am_to_comp = quiz.questions_amount_to_complete
            result.append(
                {
                    "id": quiz.quiz_id,
                    "creator": {
                        "user_id": quiz.creator.user.id,
                        "user_email": quiz.creator.user.email,
                        "creator_id": quiz.creator.id},
                    "quiz_name": quiz.quiz_name,
                    "quiz_description": quiz.quiz_description,
                    "duration": quiz.duration,
                    "question_amount": quiz.questions_amount,
                    "questions_amount_to_complete": q_am_to_comp,
                    "created_date": quiz.created_date,
                    "quiz_tries": quiz.quiz_tries,
                    "show_ans_res": quiz.show_ans_res,
                    "mark_type": quiz.quiz_mark_type,
                    "question_switch": quiz.question_switch,
                    "reanswer": quiz.reanswer,
                    "question_easy": quiz.question_easy,
                    "question_medium": quiz.question_medium,
                    "question_hard": quiz.question_hard})
            i += 1
            if i == 20:
                break
        return {"success": 1, "data": result}
