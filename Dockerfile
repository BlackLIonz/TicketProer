FROM python:3.7
ENV \
PYTHONUNBUFFERED=1 \
DEBUG=True \
DJANGO_SETTINGS_MODULE=TicketProer.settings \
DB_ENGINE=django.db.backends.postgresql \
DB_NAME=postgres \
DB_USER=postgres \
DB_PASSWORD=admin \
DB_HOST=db \
DB_POST=5432 \
TIME_ZONE=UTC \
STATIC_URL=/static/
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000