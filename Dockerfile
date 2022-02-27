# base image  
FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .

RUN pip install -r requirements.txt