FROM python:3.8.2-alpine

WORKDIR /usr/src/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/project/requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/project/entrypoint.sh
RUN ["chmod", "+x", "/usr/src/project/entrypoint.sh"]

COPY . /usr/src/project/

ENTRYPOINT ["sh", "/usr/src/project/entrypoint.sh"]