from fastapi import APIRouter, Response
from database.entities import *
from usermodels.models import *
import datetime
router = APIRouter()

#Добавление выбранного варианта ответа на вопрос
@router.post("/question/add/choice",status_code=200)
async def add_choice(response: Response, body:UserAnswerChoice):
    time = datetime.datetime.now()
    session_id = body.session_id
    question_id = body.question_id
    with SessionLocal() as session:
        for answer_id in body.answers:
            answer = session.query(QuestionAnswer).filter(QuestionAnswer.id==answer_id).first()
            correct = answer.answer_correct
            point = answer.answer_points if answer.answer_points!=None else 0
            choice = QuestionUserAnswerChoice()
            choice.session_id = session_id
            choice.question_id = question_id
            choice.answer_id = answer_id
            choice.answer_time = time 
            choice.answer_points = point 
            choice.answer_correct = correct
            session.add(choice)
        session.commit()
        return{"success":1}




#Изменение выбора ответа
@router.put("/question/update/choice/{id}",status_code=200)
async def add_choice(response: Response, body:UserUpdateAnswerChoice, id:int):
    time = datetime.datetime.now()
    with SessionLocal() as session:
        us_choice_ans = session.query(QuestionUserAnswerChoice).filter(QuestionUserAnswerChoice.id==id).first()
        if not(us_choice_ans):
            response.status_code = 404
        for answer_id in body.answers:
            answer = session.query(QuestionAnswer).filter(QuestionAnswer.id==answer_id).first()
            correct = answer.answer_correct
            point = answer.answer_points if answer.answer_points!=None else 0
            choice = QuestionUserAnswerChoice()
            choice.answer_id = answer_id
            choice.answer_time = time 
            choice.answer_points = point 
            choice.answer_correct = correct
            session.add(choice)
        session.commit()
        return{"success":1}



#Удаление выбора ответа
@router.delete("/question/delete/choice/{id}",status_code=200)
async def remove_user_answer_choice_by_index(response: Response, id:int):
    with SessionLocal() as session:
        us_choice_ans = session.query(QuestionUserAnswerChoice).filter(QuestionUserAnswerChoice.id==id).first()
        if not(us_choice_ans):
            response.status_code = 404
            return {"success": 0,"error": f"Ответ с id {id} не существует"}
        session.query(QuestionUserAnswerChoice).filter(QuestionUserAnswerChoice.id==id).delete()
        session.delete(us_choice_ans)
        session.commit()
        return {"success": 1,"data": id}




#Добавление текстового ответа
@router.post("/question/add/text",status_code=200)
async def add_choice(response: Response, body:UserAnswerText):
    time = datetime.datetime.now()
    session_id = body.session_id
    question_id = body.question_id
    with SessionLocal() as session:
        correct = None
        point = None
        text = QuestionUserAnswerText()
        text.session_id = session_id
        text.question_id = question_id
        text.answer = body.answer
        text.answer_time = time 
        text.answer_points = point 
        text.answer_correct = correct
        session.add(text)
        session.commit()
        return{"success":1}    
    



#Изменение текстового ответа
@router.put("/question/update/text/{id}",status_code=200)
async def add_choice(response: Response, body:UserUpdateAnswerText, id:int):
    time = datetime.datetime.now()
    with SessionLocal() as session:
        text = session.query(QuestionUserAnswerText).filter(QuestionUserAnswerText.id==id).first()
        text.answer = body.answer
        text.answer_time = time
        return{"success":1,"data": id}  
    



#Удаление текстового ответа
@router.delete("/question/delete/text/{id}",status_code=200)
async def remove_user_answer_text_by_index(response: Response, id:int):
    with SessionLocal() as session:
        us_text_ans = session.query(QuestionUserAnswerText).filter(QuestionUserAnswerText.id==id).first()
        if not(us_text_ans):
            response.status_code = 404
            return {"success": 0,"error": f"Ответ с id {id} не существует"}
        session.query(QuestionUserAnswerText).filter(QuestionUserAnswerText.id==id).delete()
        session.delete(us_text_ans)
        session.commit()
        return {"success": 1,"data": id}