from fastapi import APIRouter, Response
from database.entities import *
from usermodels.models import *
router = APIRouter()


#Удаление вопроса
@router.delete("/question/{id}/delete",status_code=200)
async def remove_question_by_index(response: Response, id:int):
    with SessionLocal() as session:
        question = session.query(QuizQuestion).filter(QuizQuestion.id==id).first()
        if not(question):
            response.status_code = 404
            return {"success": 0,"error": f"Вопрос с id {id} не существует"}
        session.delete(question)
        quiz = session.query(Quiz).filter_by(quiz_id=question.quiz_id).first()
        quiz.questions_amount = quiz.questions_amount-1
        session.commit()
        return {"success": 1,"data": id}

#Изменение вопроса
@router.put("/question/{id}/update",status_code=200)
async def update_question(response: Response, body:UpdateQuizQuestion, id:int):
    with SessionLocal() as session:
         question = session.query(QuizQuestion).filter(QuizQuestion.id==id).first()
         if question:
             if body.question_text!=None:
                 question.question_text =body.question_text
             if body.question_description!=None:
                 question.question_description = body.question_description  
             if body.question_time!=None:
                 question.question_time = body.question_time
             if body.question_points!=None:
                 question.question_points = body.question_points
             if body.question_number!=None:
                 question.question_number = body.question_number
             if body.question_difficulty!=None:
                 question.question_difficulty = body.question_difficulty
             if body.question_hint!=None:
                 question.question_hint = body.question_hint
             session.commit()
             return {"success":1,"data":question.id}
         response.status_code = 404
         return {"success":0,"error":f"Вопрос с id {id} не существует"}
    
#Получение вопроса по id
@router.get("/question/{id}",status_code=200)
async def get_question_by_id(response: Response,id:int):
    with SessionLocal() as session:
        question = session.query(QuizQuestion).filter(QuizQuestion.id==id).order_by(asc(QuizQuestion.question_number)).first()
        if not(question):
            response.status_code = 404
            return {"success":0,"error":f"Вопрос с id {id} не существует"}
        return {"success":1,"data":{
                "id":question.id,
                "question_text":question.question_text,
                "question_description":question.question_description,
                "question_time":question.question_time,
                "question_points":question.question_points,
                "question_type":question.question_type,
                "quiz_id":question.quiz_id,
                "question_number":question.question_number,
                "question_difficulty":question.question_difficulty,
                "question_hint":question.question_hint
            }}


#Получение списка вариантов ответа на вопрос
@router.get("/question/{id}/answer_list",status_code=200)
async def  get_answer_list(response: Response,id:int):
    with SessionLocal() as session:
        question = session.query(QuizQuestion).filter(QuizQuestion.id==id).first()
        if not(question):
            response.status_code = 404
            return {"succes":0,"error":f"Вопрос с id {id} не существует"}
        list_answers = session.query(QuestionAnswer).filter(QuestionAnswer.question_id==id).order_by(asc(QuestionAnswer.answer_number)).all()
        result = []
        for answer in list_answers:
            result.append({
                "question_id":question.id,
                "id":answer.id,
                "answer_text":answer.answer_text,
                "answer_points":answer.answer_points,
                "answer_number":answer.answer_number,
                "answer_correct":answer.answer_correct
            })
        return {"success":1,"data":result}