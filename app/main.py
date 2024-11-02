import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from database.entities import *
from usermodels.models import *
from roters_my_quiz import users,tests,questions,questionanswers,useranswers,session
app = FastAPI()
app.include_router(users.router)
app.include_router(tests.router)
app.include_router(questions.router)
app.include_router(questionanswers.router)
app.include_router(useranswers.router)
app.include_router(session.router)

@app.get("/")
def index():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)