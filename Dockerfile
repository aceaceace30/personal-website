# base image  
FROM python:3.9-alpine3.13
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY . .

RUN pip install -r requirements.txt