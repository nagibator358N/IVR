import datetime
from fastapi import HTTPException, status
from pydantic import EmailStr, field_validator, ValidationError, model_validator
from typing import Union, List
from pydantic import BaseModel
import re
from database.entities import *



#Создаём функцию для валидации пароля
def validate_password(password):
    if len(password)<8:
        raise HTTPException(detail="Пароль слишком короткий",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    pattern = re.compile(r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})")
    if not(pattern.match(password)):
        raise HTTPException(detail="Пароль должен содержать минимум одну цифру,заглавную букву или спец символ",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return password




#Класс описывающий входные данные на запрос на добавление нового пользователя
class AddUserRequest(BaseModel):
    mail:EmailStr
    password:str
    @field_validator("mail")
    def validate_mail(cls,mail, **kwargs):
        with SessionLocal() as session:
            if session.query(User).filter(User.email==mail).first():
                raise HTTPException(detail="Данный email уже используется",status_code=status.HTTP_400_BAD_REQUEST)
            return mail
    @field_validator("password")
    def validate_password(cls, password, **kwargs):
        return validate_password(password)

class LogInUserRequest(BaseModel):
    mail:EmailStr
    password:str
    @field_validator("password")
    def validate_password(cls, password, **kwargs):
        return validate_password(password)


#Класс описывающий входные данные на запрос на изменения данных пользователя
class UpdateUserRequest(BaseModel):
    mail:Union[EmailStr, None] = None
    new_password:Union[str, None] = None
    old_password:Union[str, None] = None
    @field_validator("new_password")
    def validate_password(cls, password, **kwargs):
        if password==None:
            return None
        return validate_password(password)




#Класс описывающий входные данные на запрос на добавление нового теста
class AddQuizRequest(BaseModel):
    quiz_name:str 
    duration:Union[int, None] = None
    user_id:Union[int, None] = None
    creator_id:Union[int, None] = None
    questions_amount_to_complete:int 
    quiz_description:Union[str, None] = None
    quiz_tries:Union[int, None] = None
    show_ans_res:bool
    quiz_mark_type:int
    question_switch:bool
    reanswer:bool
    question_easy:Union[int, None] = None
    question_medium:Union[int, None] = None
    question_hard:Union[int, None] = None
    @field_validator("quiz_name")
    def validate_quiz_name(cls,quiz_name, **kwargs):
        if len(" ".join(quiz_name.split()))<4:
            raise HTTPException(detail="Название теста должно быть не короче 4 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return quiz_name
    @field_validator("duration")
    def validate_duration(cls,duration, **kwargs):
        if duration<300:
            raise HTTPException(detail="Время на тест должно быть не менее 5 минут (300 секунд)",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return duration
    @model_validator(mode="after")
    def validate_ids(self):
        if self.creator_id==None and self.user_id==None:
            print("Gg")
            raise HTTPException(detail="Должно быть заполнено поле creator_id или user_id",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return self
    @field_validator("quiz_description")
    def validate_quiz_description(cls,quiz_description, **kwargs):
        if len(" ".join(quiz_description.split()))<5:
            raise HTTPException(detail="Описание теста должно быть более 5 символов, если вы не можете придумать более длинное описание, просто не указывайте его",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return quiz_description
    @field_validator("questions_amount_to_complete")
    def validate_questions_amount_to_complete(cls,questions_amount_to_complete, **kwargs):
        if questions_amount_to_complete<1:
            raise HTTPException(detail="Количество вопросов для завершения теста должно быть больше 0",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return questions_amount_to_complete
    @field_validator("question_easy")
    def validate_question_easy(cls,question_easy, **kwargs):
        if question_easy!= None and question_easy<1:
            raise HTTPException(detail="Количество вопросов с легкой сложностью для завершения теста должно быть больше 0 или можете просто не заполнять данное поле",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_easy
    @field_validator("question_medium")
    def validate_question_medium(cls,question_medium, **kwargs):
        if question_medium!= None and question_medium<1:
            raise HTTPException(detail="Количество вопросов с среденей сложностью для завершения теста должно быть больше 0 или можете просто не заполнять данное поле",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_medium
    @field_validator("question_hard")
    def validate_question_hard(cls,question_hard, **kwargs):
        if question_hard!= None and question_hard<1:
            raise HTTPException(detail="Количество вопросов с высокой сложностью для завершения теста должно быть больше 0 или можете просто не заполнять данное поле",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_hard
    @model_validator(mode="after")
    def validate_ids(self):
        if self.question_easy!=None and self.question_medium!=None and self.question_hard!=None:
                if self.question_easy+self.question_medium+self.question_hard > self.questions_amount_to_complete:
                    raise HTTPException(detail="Количество вопросов легких, нормальных и сложных суммарно должно быть меньше либо равно количеству вопросов для завершения теста",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return self




#Класс описывающий входные данные на запрос на изменение теста
class UpdateQuizRequest(BaseModel):
    quiz_name:Union[str, None] = None
    duration:Union[int, None] = None
    quiz_description:Union[str, None] = None
    quiz_tries:Union[int, None] = None
    show_ans_res:bool
    questions_amount_to_complete:int
    quiz_mark_type:int
    question_switch:bool
    reanswer:bool
    question_easy:Union[int, None] = None
    question_medium:Union[int, None] = None
    question_hard:Union[int, None] = None
    @model_validator(mode="after")
    def validate_ids(self):
        if self.quiz_name==None and self.duration==None and self.quiz_description==None:
            raise HTTPException(detail="Одно из полей: quiz_name, duration, quiz_description должно обязательно быть заполнено",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return self
    @field_validator("duration")
    def validate_duration(cls,duration, **kwargs):
        if duration<300:
            print("duration")
            raise HTTPException(detail="Время на тест должно быть не менее 5 минут (300 секунд)",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return duration
    @field_validator("quiz_description")
    def validate_quiz_description(cls,quiz_description, **kwargs):
        if len(" ".join(quiz_description.split()))<5:
            raise HTTPException(detail="Описание теста должно быть более 5 символов, если вы не можете придумать более длинное описание, просто не указывайте его",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return quiz_description
    @field_validator("quiz_name")
    def validate_quiz_name(cls,quiz_name, **kwargs):
        if len(" ".join(quiz_name.split()))<4:
            raise HTTPException(detail="Название теста должно быть не короче 4 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return quiz_name
    @field_validator("quiz_mark_type")
    def validate_quiz_mark_type(cls,quiz_mark_type, **kwargs):
        if quiz_mark_type!=1 and quiz_mark_type!=2 and quiz_mark_type!=3 and quiz_mark_type!=4:
            raise HTTPException(detail="Способ оценивания результатов теста который вы выбрали не существует выберите 1(максимальная оценка),2(минимальная оценка),3(среднее значение),4(последний результат)",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return quiz_mark_type
    @field_validator("questions_amount_to_complete")
    def validate_questions_amount_to_complete(cls,questions_amount_to_complete, **kwargs):
        if questions_amount_to_complete<1:
            raise HTTPException(detail="Количество вопросов для завершения теста должно быть больше 0",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return questions_amount_to_complete
    @field_validator("question_easy")
    def validate_question_easy(cls,question_easy, **kwargs):
        if question_easy!= None and question_easy<1:
            raise HTTPException(detail="Количество вопросов с легкой сложностью для завершения теста должно быть больше 0 или можете просто не заполнять данное поле",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_easy
    @field_validator("question_medium")
    def validate_question_medium(cls,question_medium, **kwargs):
        if question_medium!= None and question_medium<1:
            raise HTTPException(detail="Количество вопросов с среденей сложностью для завершения теста должно быть больше 0 или можете просто не заполнять данное поле",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_medium
    @field_validator("question_hard")
    def validate_question_hard(cls,question_hard, **kwargs):
        if question_hard!= None and question_hard<1:
            raise HTTPException(detail="Количество вопросов с высокой сложностью для завершения теста должно быть больше 0 или можете просто не заполнять данное поле",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_hard
    @model_validator(mode="after")
    def validate_ids(self):
        if self.question_easy!=None and self.question_medium!=None and self.question_hard!=None:
                if self.question_easy+self.question_medium+self.question_hard > self.questions_amount_to_complete:
                    raise HTTPException(detail="Количество вопросов легких, нормальных и сложных суммарно должно быть меньше либо равно количеству вопросов для завершения теста",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return self





#Класс описывающий входные данные на запрос на добавление нового вопроса к тесту
class AddQuizQuestion(BaseModel):
    question_text:str 
    question_description:Union[str, None] = None
    question_time:Union[int, None] = None
    question_points:Union[int, None] = None
    question_type:int
    quiz_id:int 
    question_number:Union[int, None] = None
    question_difficulty:Union[int, None] = None
    question_hint:Union[str, None] = None
    @field_validator("question_text")
    def validate_question_text(cls,question_text, **kwargs):
        if len(" ".join(question_text.split()))<3:
            raise HTTPException(detail="Вопрос должен быть не короче 3 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_text
    @field_validator("question_description")
    def validate_question_description(cls,question_description, **kwargs):

        if question_description!=None and len(question_description.strip())>0 and len(" ".join(question_description.split()))<20:
            raise HTTPException(detail="Описание вопроса должно быть не короче 20 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_description
    @field_validator("question_time")
    def validate_question_time(cls,question_time, **kwargs):
        if question_time!=None and question_time<10:
            raise HTTPException(detail="Время на вопрос должно быть более 10 секунд",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_time
    @field_validator("question_type")
    def validate_question_type(cls,question_type, **kwargs):
        if question_type!=1 and question_type!=2 and question_type!=3:
            raise HTTPException(detail="Тип вопроса который вы выбрали не существует выберите 1(выбор одного вырианта ответа),2(выбор нескольких вариантов ответа),3(открытый ответ)",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_type
    @field_validator("quiz_id")
    def validate_quiz_id(cls,quiz_id, **kwargs):
        with SessionLocal() as session:
            if not(session.query(Quiz).filter(Quiz.quiz_id==quiz_id).first()):
                raise HTTPException(detail=f"Тест с {quiz_id} не существует",status_code=status.HTTP_404_NOT_FOUND)
            return quiz_id
    @field_validator("question_hint")
    def validate_question_hint(cls,question_hint, **kwargs):
        if len(" ".join(question_hint.split()))<5 and question_hint!="":
            raise HTTPException(detail="Подсказка на вопрос должна быть не короче 5 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_hint




#Класс описывающий входные данные на запрос на изменение вопроса к тесту
class UpdateQuizQuestion(BaseModel):
    question_text:Union[str, None] = None
    question_description:Union[str, None] = None
    question_time:Union[int, None] = None
    question_points:Union[int, None] = None
    question_number:Union[int, None] = None
    question_difficulty:Union[int, None] = None
    question_hint:Union[str, None] = None
    @model_validator(mode="after")
    def validate_ids(self):
        if self.question_text==None and self.question_description==None and self.question_time==None and self.question_points==None and self.question_number==None and self.question_difficulty==None and self.question_hint==None:
            raise HTTPException(detail="Одно из полей: question_text, question_description, question_time, question_points, question_number, question_difficulty, question_hint должно обязательно быть заполнено",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return self    
    @field_validator("question_text")
    def validate_question_text(cls,question_text, **kwargs):
        if len(" ".join(question_text.split()))<4:
            raise HTTPException(detail="Вопрос должен быть не короче 4 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_text
    @field_validator("question_description")
    def validate_question_description(cls,question_description, **kwargs):
        if question_description!=None and len(" ".join(question_description.split()))<20:
            raise HTTPException(detail="Описание вопроса должно быть не короче 20 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_description
    @field_validator("question_time")
    def validate_question_time(cls,question_time, **kwargs):
        if question_time!=None and question_time<10:
            raise HTTPException(detail="Время на вопрос должно быть более 10 секунд",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_time
    @field_validator("question_hint")
    def validate_question_hint(cls,question_hint, **kwargs):
        if len(" ".join(question_hint.split()))<5 and question_hint!="":
            raise HTTPException(detail="Подсказка на вопрос должна быть не короче 5 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return question_hint




#Класс описывающий входные данные на запрос на добавление нового варианта ответа на вопрос
class AddQuestionAnswer(BaseModel):
    answer_text:str
    question_id:int 
    answer_points:Union[int, None] = None
    answer_number:Union[int, None] = None
    answer_correct:bool
    @field_validator("answer_text")
    def validate_answer_text(cls,answer_text, **kwargs):
        if len(" ".join(answer_text.split()))<2:
            raise HTTPException(detail="Ответ должен быть не короче 2 символов",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return answer_text
    @field_validator("question_id")
    def validate_question_id_and_type(cls,question_id, **kwargs):
        with SessionLocal() as session:
            question = session.query(QuizQuestion).filter(QuizQuestion.id==question_id).first()
            if not(question):
                raise HTTPException(detail=f"Вопрос с id {question_id} не существует",status_code=status.HTTP_404_NOT_FOUND)
            if question.question_type==3:
                raise HTTPException(detail=f"К вопросу со свободным ответом нельзя добавить варианты ответа",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return question_id

class UserAnswer(BaseModel):
    answers:List[int]
    text_answer:Union[str,None] = None

class Points(BaseModel):
    points:int
#Класс описывающий входные данные на запрос на выбор ответа пользователем
class UserAnswerChoice(BaseModel):
    session_id:int
    question_id:int
    answers:List[int]
    @field_validator("question_id")
    def validate_question_id_and_type(cls,question_id, **kwargs):
        with SessionLocal() as session:
            question = session.query(QuizQuestion).filter(QuizQuestion.id==question_id).first()
            if not(question):
                raise HTTPException(detail=f"Вопрос с id {question_id} не существует",status_code=status.HTTP_404_NOT_FOUND)
            if question.question_type==3:
                raise HTTPException(detail=f"К вопросу со свободным ответом нельзя добавить варианты ответа",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return question_id
    @field_validator("session_id")
    def validate_us_session(cls,session_id, **kwargs):
        with SessionLocal() as session:
            us_session = session.query(QuizSession).filter(QuizSession.id==session_id).first()
            if not(us_session):
                raise HTTPException(detail=f"Сессия с id {session_id} не существует",status_code=status.HTTP_404_NOT_FOUND)
            return session_id
    @model_validator(mode="after")
    def validate_ids(self):
        with SessionLocal() as session:
            for answer in self.answers:
                if session.query(QuestionAnswer).filter(QuestionAnswer.question_id==self.question_id).filter(QuestionAnswer.id==answer).first():
                    raise HTTPException(detail=f"Вы дали ответ которого не существует {answer}",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return self




#Класс описывающий входные данные на запрос на ввод ответа на свободный вопрос пользователем    
class UserAnswerText(BaseModel):
    session_id:int
    question_id:int
    answer:str
    @field_validator("question_id")
    def validate_question_id_and_type(cls,question_id, **kwargs):
        with SessionLocal() as session:
            question = session.query(QuizQuestion).filter(QuizQuestion.id==question_id).first()
            if not(question):
                raise HTTPException(detail=f"Вопрос с id {question_id} не существует",status_code=status.HTTP_404_NOT_FOUND)
            if question.question_type!=3:
                raise HTTPException(detail=f"К вопросу с выбором ответа нельзя добавить варианты ответа",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return question_id
    @field_validator("session_id")
    def validate_us_session(cls,session_id, **kwargs):
        with SessionLocal() as session:
            us_session = session.query(QuizSession).filter(QuizSession.id==session_id).first()
            if not(us_session):
                raise HTTPException(detail=f"Сессия с id {session_id} не существует",status_code=status.HTTP_404_NOT_FOUND)
            return session_id
    @field_validator("answer")
    def validate_user(cls,answer, **kwargs):
        if len(answer.strip())==0:
            raise HTTPException(detail="Текстовый ответ должен быть не пустым",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return answer




#Класс описывающий входные данные на запрос на изменение ответа на свободный вопрос пользователем    
class UserUpdateAnswerText(BaseModel):
    answer:str
    @field_validator("answer")
    def validate_user(cls,answer, **kwargs):
        if len(answer.strip())==0:
            raise HTTPException(detail="Текстовый ответ должен быть не пустым",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return answer




#Класс описывающий входные данные на запрос на изменение ответа на вопрос с выбором ответа пользователем    
class UserUpdateAnswerChoice(BaseModel):
    answers:List[int] 



class RefreshSession(BaseModel):
    session_id:int 
    disconnect_duration:Union[int,None] = None 
    @model_validator(mode="after")
    def validate_session_id(self):
        with SessionLocal() as session:
            us_session = session.query(QuizSession).filter(QuizSession.id==self.session_id).first()
            if not(us_session):
                raise HTTPException(detail=f"Сессия с id {self.session_id} не существует",status_code=status.HTTP_404_NOT_FOUND)
            if us_session.finishing_time!=None:
                raise HTTPException(detail=f"Сессия с id {self.session_id} уже завершена",status_code=status.HTTP_404_NOT_FOUND)
            time = datetime.datetime.now()
            if self.disconnect_duration!=None and self.disconnect_duration<1:
                raise HTTPException(detail=f"Продолжительность отключения должна быть положительной",status_code=status.HTTP_404_NOT_FOUND)
            if self.disconnect_duration!=None and self.disconnect_duration<1 and (time - us_session.beginning_time).total_seconds()<self.disconnect_duration:
                raise HTTPException(detail=f"Продолжительность отключения не может быть длиннее сессии",status_code=status.HTTP_404_NOT_FOUND)
            return self