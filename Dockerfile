FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip cmake wget llvm

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN pip install python-dotenv supabase psycopg2-binary django-cors-headers

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]