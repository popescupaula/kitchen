#Dockerfile, Image, Container
FROM python:3.9

COPY imports.txt .

RUN pip install -r imports.txt

ADD kitchen.py .

ADD menu.py .

CMD ["python", "./kitchen.py"]