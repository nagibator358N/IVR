from fastapi import APIRouter, Response
from app.database.entities import QuestionAnswer
from app.usermodels.models import AddQuestionAnswer
from app.db.database import SessionLocal
router = APIRouter()

# Добавление варианта ответа на вопрос


@router.post("/question/answer/add", status_code=201)
async def add_answer(response: Response, body: AddQuestionAnswer):
    with SessionLocal() as session:
        answer = QuestionAnswer()
        answer.answer_text = body.answer_text
        answer.question_id = body.question_id
        answer.answer_points = body.answer_points
        answer.answer_number = body.answer_number
        answer.answer_correct = body.answer_correct
        session.add(answer)
        session.commit()
        return {"success": 1, "data": {"id": answer.id}}

# Изменение варианта ответа на вопрос


@router.put("/question/answer/{id}/update", status_code=201)
async def update_answer(response: Response, body: AddQuestionAnswer, id: int):
    with SessionLocal() as session:
        answer = session.query(QuestionAnswer).filter(
            QuestionAnswer.id == id).first()
        if answer:
            if body.answer_text is not None:
                answer.answer_text = body.answer_text
            if body.answer_correct is not None:
                answer.answer_correct = body.answer_correct
            if body.answer_number is not None:
                answer.answer_number = body.answer_number
            if body.answer_points is not None:
                answer.answer_points = body.answer_points
            session.commit()
            response.status_code = 404
            return {"success": 1, "data": answer.id}
        response.status_code = 200
        return {"success": 0, "error": "Вопрос с id {id} не существует"}

# Удаление варианта ответа на вопрос


@router.delete("/answer/{id}/delete", status_code=200)
async def remove_answer_by_index(response: Response, id: int):
    with SessionLocal() as session:
        answer = session.query(QuestionAnswer).filter(
            QuestionAnswer.id == id).first()
        if not (answer):
            response.status_code = 404
            return {"success": 0, "error": f"Ответ с id {id} не существует"}
        session.delete(answer)
        session.commit()
        return {"success": 1, "data": id}

# Получение варианта ответа по id


@router.get("/answer/{id}", status_code=200)
async def get_question_by_id(response: Response, id: int):
    with SessionLocal() as session:
        answer = session.query(QuestionAnswer).filter(
            QuestionAnswer.id == id).first()
        if not (answer):
            response.status_code = 404
            return {"succes": 0, "error": f"Ответ с id {id} не существует"}
        return {"succes": 1, "data": {
                "question_id": answer.question_id,
                "id": answer.id,
                "answer_text": answer.answer_text,
                "answer_points": answer.answer_points,
                "answer_number": answer.answer_number,
                "answer_correct": answer.answer_correct
                }}
