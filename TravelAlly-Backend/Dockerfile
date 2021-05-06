FROM python:3.7-alpine
MAINTAINER SHUBHAM KUMAR

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip3 install --upgrade pip
RUN pip3 --default-timeout=10000 install -r /requirements.txt
RUN pip install --upgrade google-auth
RUN pip install requests
RUN pip install django-phonenumber-field
RUN pip install phonenumbers
RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
