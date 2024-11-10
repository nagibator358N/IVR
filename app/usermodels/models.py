import datetime
from fastapi import HTTPException, status
from pydantic import EmailStr, field_validator, model_validator
from typing import Union, List
from pydantic import BaseModel
import re
from app.db.database import SessionLocal
from app.database.entities import User, Quiz, QuizQuestion, QuizSession
from app.database.entities import QuestionAnswer as QA
import app.constants.models_constants as constant


# Создаём функцию для валидации пароля
def validate_password(password):
    if len(password) < 8:
        raise HTTPException(detail=constant.SHORT_PASSWORD,
                            status_code=422)
    pattern = re.compile(r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})")
    if not (pattern.match(password)):
        raise HTTPException(detail=constant.NOT_APPROPRIATE_PASSWORD,
                            status_code=422)
    return password


# Класс описывающий входные данные на запрос на добавление нового пользователя
class AddUserRequest(BaseModel):
    mail: EmailStr
    password: str

    @field_validator("mail")
    def validate_mail(cls, mail, **kwargs):
        with SessionLocal() as session:
            if session.query(User).filter(User.email == mail).first():
                raise HTTPException(
                    detail=constant.USED_EMAIL,
                    status_code=status.HTTP_400_BAD_REQUEST)
            return mail

    @field_validator("password")
    def validate_password(cls, password, **kwargs):
        return validate_password(password)


class LogInUserRequest(BaseModel):
    mail: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, password, **kwargs):
        return validate_password(password)


# Класс описывающий входные данные на запрос на изменения данных пользователя
class UpdateUserRequest(BaseModel):
    mail: Union[EmailStr, None] = None
    new_password: Union[str, None] = None
    old_password: Union[str, None] = None

    @field_validator("new_password")
    def validate_password(cls, password, **kwargs):
        if password is None:
            return None
        return validate_password(password)


# Класс описывающий входные данные на запрос на добавление нового теста
class AddQuizRequest(BaseModel):
    quiz_name: str
    duration: Union[int, None] = None
    user_id: Union[int, None] = None
    creator_id: Union[int, None] = None
    questions_amount_to_complete: int
    quiz_description: Union[str, None] = None
    quiz_tries: Union[int, None] = None
    show_ans_res: bool
    quiz_mark_type: int
    question_switch: bool
    reanswer: bool
    question_easy: Union[int, None] = None
    question_medium: Union[int, None] = None
    question_hard: Union[int, None] = None

    @field_validator("quiz_name")
    def validate_quiz_name(cls, quiz_name, **kwargs):
        if len(" ".join(quiz_name.split())) < 4:
            raise HTTPException(detail=constant.SHORT_NAME_TEST,
                                status_code=422)
        return quiz_name

    @field_validator("duration")
    def validate_duration(cls, duration, **kwargs):
        if duration < 300:
            raise HTTPException(
                detail=constant.SHORT_DURATION_TEST,
                status_code=422)
        return duration

    @model_validator(mode="after")
    def validate_ids(self):
        if self.creator_id is None and self.user_id is None:
            raise HTTPException(detail=constant.NO_CREATOR_ID_TEST,
                                status_code=422)
        return self

    @field_validator("quiz_description")
    def validate_quiz_description(cls, quiz_description, **kwargs):
        if len(" ".join(quiz_description.split())) < 5:
            raise HTTPException(detail=constant.SHORT_DESCRIPTION_TEST,
                                status_code=422)
        return quiz_description

    @field_validator("questions_amount_to_complete")
    def validate_q_am_to_comp(cls, questions_amount_to_complete, **kwargs):
        if questions_amount_to_complete < 1:
            raise HTTPException(detail=constant.SMALL_QUESTION_AM_COMP_TEST,
                                status_code=422)
        return questions_amount_to_complete

    @field_validator("question_easy")
    def validate_question_easy(cls, question_easy, **kwargs):
        if not (question_easy is None) and question_easy < 1:
            raise HTTPException(detail=constant.EASY_Q_AM_TEST,
                                status_code=422)
        return question_easy

    @field_validator("question_medium")
    def validate_question_medium(cls, question_medium, **kwargs):
        if not (question_medium is None) and question_medium < 1:
            raise HTTPException(detail=constant.MED_Q_AM_TEST,
                                status_code=422)
        return question_medium

    @field_validator("question_hard")
    def validate_question_hard(cls, question_hard, **kwargs):
        if not (question_hard is None) and question_hard < 1:
            raise HTTPException(detail=constant.HARD_Q_AM_TEST,
                                status_code=422)
        return question_hard


# Класс описывающий входные данные на запрос на изменение теста
class UpdateQuizRequest(BaseModel):
    quiz_name: Union[str, None] = None
    duration: Union[int, None] = None
    quiz_description: Union[str, None] = None
    quiz_tries: Union[int, None] = None
    show_ans_res: bool
    questions_amount_to_complete: int
    quiz_mark_type: int
    question_switch: bool
    reanswer: bool
    question_easy: Union[int, None] = None
    question_medium: Union[int, None] = None
    question_hard: Union[int, None] = None

    @model_validator(mode="after")
    def validate_ids(self):
        cond_1 = self.quiz_name is None
        cond_2 = self.duration is None
        cond_3 = self.quiz_description is None
        if cond_1 and cond_2 and cond_3:
            raise HTTPException(detail=constant.NOT_NAME_DUR_DESC_TEST,
                                status_code=422)
        return self

    @field_validator("duration")
    def validate_duration(cls, duration, **kwargs):
        if duration < 300:
            print("duration")
            raise HTTPException(detail=constant.SHORT_DURATION_TEST,
                                status_code=422)
        return duration

    @field_validator("quiz_description")
    def validate_quiz_description(cls, quiz_description, **kwargs):
        if len(" ".join(quiz_description.split())) < 5:
            raise HTTPException(detail=constant.SHORT_DESCRIPTION_TEST,
                                status_code=422)
        return quiz_description

    @field_validator("quiz_name")
    def validate_quiz_name(cls, quiz_name, **kwargs):
        if len(" ".join(quiz_name.split())) < 4:
            raise HTTPException(detail=constant.SHORT_NAME_TEST,
                                status_code=422)
        return quiz_name

    @field_validator("quiz_mark_type")
    def validate_quiz_mark_type(cls, quiz_mark_type, **kwargs):
        cond_1 = quiz_mark_type != 1
        cond_2 = quiz_mark_type != 2
        cond_3 = quiz_mark_type != 3
        cond_4 = quiz_mark_type != 4
        if cond_1 and cond_2 and cond_3 and cond_4:
            raise HTTPException(detail=constant.WRONG_M_TYPE_TEST,
                                status_code=422)
        return quiz_mark_type

    @field_validator("questions_amount_to_complete")
    def validate_q_am_to_comp(cls, questions_amount_to_complete, **kwargs):
        if questions_amount_to_complete < 1:
            raise HTTPException(detail=constant.SMALL_QUESTION_AM_COMP_TEST,
                                status_code=422)
        return questions_amount_to_complete

    @field_validator("question_easy")
    def validate_question_easy(cls, question_easy, **kwargs):
        if not (question_easy is None) and question_easy < 1:
            raise HTTPException(detail=constant.EASY_Q_AM_TEST,
                                status_code=422)
        return question_easy

    @field_validator("question_medium")
    def validate_question_medium(cls, question_medium, **kwargs):
        if not (question_medium is None) and question_medium < 1:
            raise HTTPException(detail=constant.MED_Q_AM_TEST,
                                status_code=422)
        return question_medium

    @field_validator("question_hard")
    def validate_question_hard(cls, question_hard, **kwargs):
        if not (question_hard is None) and question_hard < 1:
            raise HTTPException(detail=constant.HARD_Q_AM_TEST,
                                status_code=422)
        return question_hard


# Класс описывающий входные данные на запрос добавления нового вопроса к тесту
class AddQuizQuestion(BaseModel):
    question_text: str
    question_description: Union[str, None] = None
    question_time: Union[int, None] = None
    question_points: Union[int, None] = None
    question_type: int
    quiz_id: int
    question_number: Union[int, None] = None
    question_difficulty: Union[int, None] = None
    question_hint: Union[str, None] = None

    @field_validator("question_text")
    def validate_question_text(cls, question_text, **kwargs):
        if len(" ".join(question_text.split())) < 3:
            raise HTTPException(detail=constant.SHORT_TEXT_QUESTION,
                                status_code=422)
        return question_text

    @field_validator("question_description")
    def validate_question_description(cls, question_description, **kwargs):
        cond_1 = not (question_description is None)
        cond_2 = len(question_description.strip()) > 0
        cond_3 = len(" ".join(question_description.split())) < 5
        if cond_1 and cond_2 and cond_3:
            raise HTTPException(detail=constant.SHORT_DESC_QUESTION,
                                status_code=422)
        return question_description

    @field_validator("question_time")
    def validate_question_time(cls, question_time, **kwargs):
        if not (question_time is None) and question_time < 10:
            raise HTTPException(detail=constant.SHORT_TIME_QUESTION,
                                status_code=422)
        return question_time

    @field_validator("question_type")
    def validate_question_type(cls, question_type, **kwargs):
        if question_type != 1 and question_type != 2 and question_type != 3:
            raise HTTPException(detail=constant.NO_TYPE_QUESTION,
                                status_code=422)
        return question_type

    @field_validator("quiz_id")
    def validate_quiz_id(cls, quiz_id, **kwargs):
        with SessionLocal() as session:
            cond = session.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
            if not (cond):
                raise HTTPException(detail=f"Тест с {quiz_id} не существует",
                                    status_code=404)
            return quiz_id

    @field_validator("question_hint")
    def validate_question_hint(cls, question_hint, **kwargs):
        if len(" ".join(question_hint.split())) < 5 and question_hint != "":
            raise HTTPException(detail=constant.SHORT_HINT_QUESTION,
                                status_code=422)
        return question_hint


# Класс описывающий входные данные на запрос на изменение вопроса к тесту
class UpdateQuizQuestion(BaseModel):
    question_text: Union[str, None] = None
    question_description: Union[str, None] = None
    question_time: Union[int, None] = None
    question_points: Union[int, None] = None
    question_number: Union[int, None] = None
    question_difficulty: Union[int, None] = None
    question_hint: Union[str, None] = None

    @model_validator(mode="after")
    def validate_ids(self):
        c_1 = self.question_text is None
        c_2 = self.question_description is None
        c_3 = self.question_time is None
        c_4 = self.question_points is None
        c_5 = self.question_number is None
        c_6 = self.question_difficulty is None
        c_7 = self.question_hint is None
        if c_1 and c_2 and c_3 and c_4 and c_5 and c_6 and c_7:
            raise HTTPException(detail=constant.NO_FILLED_QUESTION,
                                status_code=422)
        return self

    @field_validator("question_text")
    def validate_question_text(cls, question_text, **kwargs):
        if len(" ".join(question_text.split())) < 4:
            raise HTTPException(detail=constant.SHORT_TEXT_QUESTION,
                                status_code=422)
        return question_text

    @field_validator("question_description")
    def validate_question_description(cls, question_description, **kwargs):
        cond_1 = not (question_description is None)
        cond_2 = len(" ".join(question_description.split())) < 5
        if cond_1 and cond_2:
            raise HTTPException(detail=constant.SHORT_DESC_QUESTION,
                                status_code=422)
        return question_description

    @field_validator("question_time")
    def validate_question_time(cls, question_time, **kwargs):
        if not (question_time is None) and question_time < 10:
            raise HTTPException(detail=constant.SHORT_TIME_QUESTION,
                                status_code=422)
        return question_time

    @field_validator("question_hint")
    def validate_question_hint(cls, question_hint, **kwargs):
        if len(" ".join(question_hint.split())) < 5 and question_hint != "":
            raise HTTPException(detail=constant.SHORT_HINT_QUESTION,
                                status_code=422)
        return question_hint


# Класс описывающий входные данные на запрос на добавление нового варианта
# ответа на вопрос
class AddQuestionAnswer(BaseModel):
    answer_text: str
    question_id: int
    answer_points: Union[int, None] = None
    answer_number: Union[int, None] = None
    answer_correct: bool

    @field_validator("answer_text")
    def validate_answer_text(cls, answer_text, **kwargs):
        if len(" ".join(answer_text.split())) < 2:
            raise HTTPException(detail=constant.SHORT_TEXT_ANSWER,
                                status_code=422)
        return answer_text

    @field_validator("question_id")
    def validate_question_id_and_type(cls, question_id, **kwargs):
        with SessionLocal() as session:
            question = session.query(QuizQuestion).filter(
                QuizQuestion.id == question_id).first()
            if not (question):
                error = f"Вопрос с id {question_id} не существует"
                raise HTTPException(detail=error, status_code=404)
            if question.question_type == 3:
                raise HTTPException(detail=constant.ADD_OPT_FREE_ANSWER,
                                    status_code=422)
            return question_id


class UserAnswer(BaseModel):
    answers: List[int]
    text_answer: Union[str, None] = None


class Points(BaseModel):
    points: int
# Класс описывающий входные данные на запрос на выбор ответа пользователем


class UserAnswerChoice(BaseModel):
    session_id: int
    question_id: int
    answers: List[int]

    @field_validator("question_id")
    def validate_question_id_and_type(cls, question_id, **kwargs):
        with SessionLocal() as session:
            question = session.query(QuizQuestion).filter(
                QuizQuestion.id == question_id).first()
            if not (question):
                error = f"Вопрос с id {question_id} не существует"
                raise HTTPException(detail=error, status_code=404)
            if question.question_type == 3:
                raise HTTPException(detail=constant.ADD_OPT_FREE_ANSWER,
                                    status_code=422)
            return question_id

    @field_validator("session_id")
    def validate_us_session(cls, session_id, **kwargs):
        with SessionLocal() as session:
            us_session = session.query(QuizSession).filter(
                QuizSession.id == session_id).first()
            if not (us_session):
                error = f"Сессия с id {session_id} не существует"
                raise HTTPException(detail=error, status_code=404)
            return session_id

    @model_validator(mode="after")
    def validate_ids(self):
        with SessionLocal() as session:
            for answer in self.answers:
                quest_id = self.question_id
                question_answers = session.query(QA)
                question = question_answers.filter(QA.question_id == quest_id)
                answer = question.filter(QA.id == answer).first()
                if answer:
                    error = f"Вы дали ответ которого не существует {answer}"
                    raise HTTPException(detail=error, status_code=422)
        return self


# Класс описывающий входные данные на запрос на ввод ответа на свободный
# вопрос пользователем
class UserAnswerText(BaseModel):
    session_id: int
    question_id: int
    answer: str

    @field_validator("question_id")
    def validate_question_id_and_type(cls, question_id, **kwargs):
        with SessionLocal() as session:
            question = session.query(QuizQuestion).filter(
                QuizQuestion.id == question_id).first()
            if not (question):
                error = f"Вопрос с id {question_id} не существует"
                raise HTTPException(detail=error, status_code=404)
            if question.question_type != 3:
                raise HTTPException(detail=constant.NO_ADD_OPT_ANSWER,
                                    status_code=422)
            return question_id

    @field_validator("session_id")
    def validate_us_session(cls, session_id, **kwargs):
        with SessionLocal() as session:
            us_session = session.query(QuizSession).filter(
                QuizSession.id == session_id).first()
            if not (us_session):
                error = f"Сессия с id {session_id} не существует"
                raise HTTPException(detail=error, status_code=404)
            return session_id

    @field_validator("answer")
    def validate_user(cls, answer, **kwargs):
        if len(answer.strip()) == 0:
            raise HTTPException(detail=constant.NO_TEXT_ANSWER,
                                status_code=422)
        return answer


# Класс описывающий входные данные на запрос на изменение ответа на свободный
# вопрос пользователем
class UserUpdateAnswerText(BaseModel):
    answer: str

    @field_validator("answer")
    def validate_user(cls, answer, **kwargs):
        if len(answer.strip()) == 0:
            raise HTTPException(detail=constant.NO_TEXT_ANSWER,
                                status_code=422)
        return answer


# Класс описывающий входные данные на запрос на изменение ответа на вопрос с
# выбором ответа пользователем
class UserUpdateAnswerChoice(BaseModel):
    answers: List[int]


class RefreshSession(BaseModel):
    session_id: int
    disconnect_duration: Union[int, None] = None

    @model_validator(mode="after")
    def validate_session_id(self):
        with SessionLocal() as session:
            us_session = session.query(QuizSession).filter(
                QuizSession.id == self.session_id).first()
            if not (us_session):
                error = f"Сессия с id {self.session_id} не существует"
                raise HTTPException(detail=error, status_code=404)
            if not (us_session.finishing_time is None):
                error = f"Сессия с id {self.session_id} уже завершена"
                raise HTTPException(detail=error, status_code=404)
            time = datetime.datetime.now()
            cond_1 = not (self.disconnect_duration is None)
            cond_2 = self.disconnect_duration < 1
            if cond_1 and cond_2:
                raise HTTPException(
                    detail=constant.MINUS_CONNECT_TIME, status_code=404)
            cond_1 = not (self.disconnect_duration is None)
            cond_2 = self.disconnect_duration < 1
            cond_3_p_1 = (time - us_session.beginning_time).total_seconds()
            cond_3 = cond_3_p_1 < self.disconnect_duration
            if cond_1 and cond_2 and cond_3:
                raise HTTPException(
                    detail=constant.TOO_LONG_DISCONNECT, status_code=404)
            return self
