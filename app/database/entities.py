from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy import String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


# Создаём структуру пользователя в базе данных
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    creator = relationship("QuizCreator", back_populates="user")


# Создаём структуру создателя теста в базе данных
class QuizCreator(Base):
    __tablename__ = "quiz_creators"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")


# Создаём структуру теста в базе данных
class Quiz(Base):
    __tablename__ = "quizes"
    quiz_id = Column(Integer, primary_key=True)
    created_date = Column(String)
    creator_id = Column(Integer, ForeignKey('quiz_creators.id'))
    creator = relationship("QuizCreator")
    duration = Column(Integer, nullable=True)
    questions_amount = Column(Integer, default=0)
    questions_amount_to_complete = Column(Integer)
    quiz_name = Column(String)
    quiz_description = Column(String, nullable=True)
    quiz_tries = Column(Integer, nullable=True)
    show_ans_res = Column(Boolean, default=False)
    quiz_mark_type = Column(Integer, CheckConstraint(
        "quiz_mark_type IN (1, 2, 3, 4)"), nullable=True)
    question_switch = Column(Boolean, default=False)
    question_easy = Column(Integer, nullable=True, default=None)
    question_medium = Column(Integer, nullable=True, default=None)
    question_hard = Column(Integer, nullable=True, default=None)
    reanswer = Column(Boolean, default=False)


# Создаём структуру вопроса теста в базе данных
class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True)
    question_text = Column(String)
    question_description = Column(String, nullable=True)
    question_time = Column(Integer, nullable=True)
    question_points = Column(Integer, nullable=True)
    question_type = Column(Integer, CheckConstraint(
        "question_type IN (1, 2, 3)"))
    quiz_id = Column(Integer, ForeignKey('quizes.quiz_id'))
    quiz = relationship("Quiz")
    question_number = Column(Integer, nullable=True)
    question_difficulty = Column(Integer, CheckConstraint(
        "question_difficulty IN (1, 2, 3)"), default=1)
    question_hint = Column(String, nullable=True)


# Создаём структуру ответа на вопрос теста в базе данных
class QuestionAnswer(Base):
    __tablename__ = "question_answers"
    id = Column(Integer, primary_key=True)
    answer_text = Column(String)
    question_id = Column(Integer, ForeignKey('quiz_questions.id'))
    question = relationship("QuizQuestion")
    answer_points = Column(Integer, nullable=True)
    answer_number = Column(Integer, nullable=True)
    answer_correct = Column(Boolean)


# Создаём структуру ответа на вопрос с выбором ответа в базе данных
class QuestionUserAnswerChoice(Base):
    __tablename__ = "user_choice_answers"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('user_quiz_session.id'))
    question_id = Column(Integer, ForeignKey('quiz_questions.id'))
    answer_id = Column(Integer, ForeignKey('question_answers.id'))
    answer_time = Column(DateTime)
    answer_points = Column(Integer, default=0)
    answer_correct = Column(Boolean)


# Создаём структуру ответа на вопрос с свободным ответом в базе данных
class QuestionUserAnswerText(Base):
    __tablename__ = "user_text_answer"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('user_quiz_session.id'))
    question_id = Column(Integer, ForeignKey('quiz_questions.id'))
    answer_time = Column(DateTime)
    answer_points = Column(Integer, default=0)
    answer = Column(String)
    answer_correct = Column(Boolean, nullable=True)


# Создаём структуру запрос на прохождение теста сверх лимита попыток
class ExtraTry(Base):
    __tablename__ = "user_extra_try"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    quiz_id = Column(Integer, ForeignKey('quizes.quiz_id'))
    created_time = Column(DateTime)
    approved = Column(Boolean, default=None, nullable=True)
    amount_tries = Column(Integer, default=1)


# Создаём структуру сессии пользователя в базе данных
class QuizSession(Base):
    __tablename__ = "user_quiz_session"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    quiz_id = Column(Integer, ForeignKey('quizes.quiz_id'))
    questions_ids = Column(String)
    beginning_time = Column(DateTime)
    finishing_time = Column(DateTime, nullable=True)
    total_time = Column(Integer)
    refresh_time = Column(DateTime, nullable=True)
    result = Column(Integer, nullable=True)
    extra_try = Column(Integer, ForeignKey('user_extra_try.id'), nullable=True)
    question_index = Column(Integer)
    questions_completed = Column(Integer, default=0)


# Создаём структуру сохранения вопроса на котором остановился пользователь,
# ответил ли на него в сессии пользователь в базе данных
class UserQuizQuestion(Base):
    __tablename__ = 'user_quiz_questions'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('quiz_questions.id'))
    is_answered = Column(Boolean, default=False)


class Reconnect(Base):
    __tablename__ = 'session_reconnect'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('user_quiz_session.id'))
    question_id = Column(Integer, ForeignKey(
        'quiz_questions.id'), nullable=True)
    duration = Column(Integer)
    reconnect_time = Column(DateTime)
