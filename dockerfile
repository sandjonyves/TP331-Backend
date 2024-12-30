

FROM python:3.8

RUN apt-get update -qq && apt-get install -y postgresql-client

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 8000  

CMD python manage.py runserver  