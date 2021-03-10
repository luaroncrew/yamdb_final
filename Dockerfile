FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /code
COPY requirements.txt /code
RUN pip install --upgrade pip && apk update && apk add postgresql-dev gcc python3-dev musl-dev && pip install -r /code/requirements.txt --no-cache-dir

COPY . /code
ENTRYPOINT ["sh", "./entrypoint.sh"]
