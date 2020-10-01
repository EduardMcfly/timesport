# pull official base image
FROM python:3.8.5-alpine

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add mariadb-dev \
    && apk del build-deps

# install node and npm
RUN apk add --update nodejs nodejs-npm

# install pillow dependencies
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

# install psql client
RUN apk --update add postgresql-client

# install git
RUN apk add git

# install dependencies
RUN pip install --upgrade pip
RUN python --version
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
RUN pip install tox
RUN npm install

# copy docker-entrypoint.sh
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

# copy project
COPY . .

# run docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]