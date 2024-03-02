FROM python:3.11.7

ENV PYTHONUNBUFFERED True

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV APP_HOME=/app

WORKDIR $APP_HOME
COPY ./src ./

CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080