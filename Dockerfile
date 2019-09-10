FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ARG TEST
ENV DOCKERIZE_VERSION v0.6.1
COPY test/requirements.txt requirements-test.txt
RUN [ "x$TEST" = "x" ] && true || pip install -r requirements-test.txt
RUN [ "x$TEST" = "x" ] && true || curl -L -s -o dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN [ "x$TEST" = "x" ] && true || tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN [ "x$TEST" = "x" ] && true || rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY . /code/

EXPOSE 8000
