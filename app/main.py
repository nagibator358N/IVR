import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from app.roters_my_quiz import users, tests, questions
from app.roters_my_quiz import questionanswers
from app.roters_my_quiz import useranswers, session
from app.db.database import engine, Base
from app.config import get_config

cfg = get_config()
app = FastAPI()

app.include_router(users.router, tags=["users"])
app.include_router(tests.router, tags=["quizes"])
app.include_router(questions.router, tags=["quiz_questions"])
app.include_router(questionanswers.router, tags=["question_answers"])
app.include_router(useranswers.router, tags=["user_answers"])
app.include_router(session.router, tags=["quiz_session"])

if not os.environ.get('TESTING', None):
    Base.metadata.create_all(bind=engine)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def read_index():
        file_path = os.path.join("app/static", "index.html")
        return FileResponse(file_path)

    @app.get("/style.css")
    async def get_css():
        file_path = os.path.join("app/static", "style.css")
        return FileResponse(file_path)

    @app.get("/script.js")
    async def get_js():
        file_path = os.path.join("app/static", "script.js")
        return FileResponse(file_path)

if __name__ == "__main__":
    log.info(f"Current working directory: {os.getcwd()}")
    log.info(f"Python path: {os.environ.get('PYTHONPATH')}")

    try:
        if cfg.run_type == "local":
            # !!! Запустить gunicorn на винде не получится (ибо нет fcntl)
            # но можно запустить в docker контейнере для теста
            uvicorn.run(
                'main:app',
                workers=2,
            )
        elif cfg.run_type == "dev" or cfg.run_type == "prod":
            from core.gunicorn.app_options import get_app_options
            from core.gunicorn.application import Application

            Application(
                application=app,
                options=get_app_options(
                    host=cfg.host,
                    port=cfg.port,
                    timeout=900,
                    workers=cfg.workers,
                    log_level=cfg.log_level,
                ),
            ).run()
    except KeyboardInterrupt:
        print("Приложение было остановлено.")
