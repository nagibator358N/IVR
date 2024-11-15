FROM python:3.12

RUN mkdir app
WORKDIR /app

ENV PYTHONPATH=/app/app

COPY README.md /app
COPY pyproject.toml /app
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.in-project false
#RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "-m", "app.main", "--host", "0.0.0.0", "--port", "8000"]
