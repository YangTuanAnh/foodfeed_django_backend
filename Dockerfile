FROM python:3.9

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip cmake wget llvm

WORKDIR /foodfeed_django_backend

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN pip install python-dotenv supabase psycopg2-binary django-cors-headers geopy redis

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "makemigrtions"]

CMD ["python", "manage.py", "migrate"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]