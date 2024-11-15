FROM python:3.12

RUN mkdir app
WORKDIR /app

ENV PYTHONPATH=/app/src

COPY README.md /app
COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "src.main", "--host", "0.0.0.0", "--port", "8000"]
