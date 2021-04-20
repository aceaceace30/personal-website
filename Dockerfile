# base image  
FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt

#RUN apk add --update --no-cache postgresl-client
# Install individual dependencies
# so that we could avoid installing extra packages to the container
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

# Remove dependencies
RUN apk del .tmp-build-deps

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN adduser -D app_user
USER app_user

CMD ["entrypoint.sh"]
