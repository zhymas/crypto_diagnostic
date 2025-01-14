FROM python:3.13

WORKDIR /backend

COPY backend .

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver"]

