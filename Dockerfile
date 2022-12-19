FROM python:3.11.0

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python /app/main.py 
