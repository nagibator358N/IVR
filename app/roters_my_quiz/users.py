from fastapi import APIRouter, Response
import json
from database.entities import *
from usermodels.models import *
router = APIRouter()

#Добавление пользователя
@router.post("/user/add/",status_code=201)
async def add_user(response: Response, body:AddUserRequest):
    with SessionLocal() as session:
        user = User()
        user.email = body.mail
        user.password = body.password
        session.add(user)
        session.commit()
        response.set_cookie(key="user_email",value=user.email)
        response.set_cookie(key="user_id", value=user.id)
        return {"success":1,"data":user.id}

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
                return {"success": 0, "error": "Неверный пароль"}
        else:
            return {"success": 0, "error": "Пользователь не найден"}

#Получение всех пользователей
@router.get("/user/all")
async def get_user_list():
    with SessionLocal() as session:
        list_user = session.query(User).all()
        result = []
        for user in list_user:
            result.append({
                "id":user.id,
                "email":user.email,
                "password":user.password
            })
        return {"succes":1,"data":result}

#Получение пользователя по id
@router.get("/user/{index}",status_code=200)
async def get_user_by_id(response: Response, index: int):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id==index).first()
        if user:
            return {"success":1,"data":{"id":user.id,"email":user.email}}
        else:
            response.status_code = 404
            return {"success":0,"error":f"Пользователь с id {index} не существует"}

#Получение поьзователя по email
@router.get("/user/mail/{mail}",status_code=200)
async def get_user_by_id(response: Response, mail: EmailStr):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email==mail).first()
        if user:
            return {"success":1,"data":{"id":user.id,"email":user.email}}
        else:
            response.status_code = 404
            return {"success":0,"error":f"Пользователь с почтой {mail} не существует"}

#Изменение пользователя
@router.put("/user/update/{index}",status_code=200)
async def update_user(response: Response, body:UpdateUserRequest, index:int):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id==index).first()
        if user:
            if body.mail!=None:
                user.email=body.mail
            if body.new_password!=None:
                if body.old_password==None:
                    response.status_code = 403
                    return {"success":0,"error":"Для изменения пароля передайте текущий пароль"}
                if user.password!=body.old_password:
                    response.status_code = 403
                    return {"success":0,"error":"Вы передали неверный пароль"}
                user.password=body.new_password
            session.commit()
            response.set_cookie(key="user_email",value=user.email)
            return {"success":1,"data":{"id":user.id,"email":user.email}}
        else:
            response.status_code = 404
            return {"success":0,"error":f"Пользователь с id {index} не существует"}