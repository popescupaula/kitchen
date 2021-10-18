#Dockerfile, Image, Container
FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD main.py .

ADD config.py .

EXPOSE 5000

CMD ["python", "./main.py"]
