FROM python:3.11.7

ENV PYTHONUNBUFFERED True

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV APP_HOME=/app

WORKDIR $APP_HOME
COPY ./src ./

CMD uvicorn main:app --workers 2 --host 0.0.0.0 --port 8080