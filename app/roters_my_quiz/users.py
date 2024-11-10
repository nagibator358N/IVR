from fastapi import APIRouter, Response
from pydantic import EmailStr
from app.database.entities import User
from app.usermodels.models import AddUserRequest
from app.usermodels.models import LogInUserRequest
from app.usermodels.models import UpdateUserRequest
from app.db.database import SessionLocal
import app.constants.users_constants as constant
router = APIRouter()

# Добавление пользователя


@router.post("/user/add/", status_code=201)
async def add_user(response: Response, body: AddUserRequest):
    with SessionLocal() as session:
        user = User()
        user.email = body.mail
        user.password = body.password
        session.add(user)
        session.commit()
        response.set_cookie(key="user_email", value=user.email)
        response.set_cookie(key="user_id", value=user.id)
        return {"success": 1, "data": {"id": user.id, "email": body.mail}}

# Вход пользователя


@router.post("/user/login/", status_code=200)
async def login_user(response: Response, body: LogInUserRequest):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == body.mail).first()
        if user:
            if user.password == body.password:
                response.set_cookie(key="user_email", value=user.email)
                response.set_cookie(key="user_id", value=user.id)
                return {"success": 1, "data": user.id}
            else:
                return {"success": 0, "error": constant.WRONG_PASSWORD}
        else:
            return {"success": 0, "error": constant.USER_NOT_FOUND}

# Получение всех пользователей


@router.get("/user/all")
async def get_user_list():
    with SessionLocal() as session:
        list_user = session.query(User).all()
        result = []
        for user in list_user:
            result.append({
                "id": user.id,
                "email": user.email,
                "password": user.password
            })
        return {"succes": 1, "data": result}

# Получение пользователя по id


@router.get("/user/{index}", status_code=200)
async def get_user_by_id(response: Response, index: int):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == index).first()
        if user:
            return {"success": 1, "data": {"id": user.id, "email": user.email}}
        else:
            response.status_code = 404
            return {
                "success": 0,
                "error": f"Пользователь с id {index} не существует"}

# Получение поьзователя по email


@router.get("/user/mail/{mail}", status_code=200)
async def get_user_by_email(response: Response, mail: EmailStr):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == mail).first()
        if user:
            return {"success": 1, "data": {"id": user.id, "email": user.email}}
        else:
            response.status_code = 404
            return {
                "success": 0,
                "error": f"Пользователь с почтой {mail} не существует"}

# Изменение пользователя


@router.put("/user/update/{index}", status_code=200)
async def update_user(response: Response, body: UpdateUserRequest, index: int):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == index).first()
        if user:
            if body.mail is None and body.new_password is None:
                response.status_code = 403
                return {
                        "success": 0,
                        "error": constant.NO_NEW_PAS_AND_MAIL}
            if body.mail is not None:
                user.email = body.mail
            if body.new_password is not None:
                if body.old_password is None:
                    response.status_code = 403
                    return {
                        "success": 0,
                        "error": constant.GIVE_NOW_PASSWORD}
                if user.password != body.old_password:
                    response.status_code = 403
                    return {"success": 0,
                            "error": constant.WRONG_PASSWORD}
                user.password = body.new_password
            session.commit()
            response.set_cookie(key="user_email", value=user.email)
            return {"success": 1, "data": {"id": user.id, "email": user.email}}
        else:
            response.status_code = 404
            return {
                "success": 0,
                "error": f"Пользователь с id {index} не существует"}
