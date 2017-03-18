FROM python:3

EXPOSE 8000

ADD . /app/
WORKDIR /app
RUN mkdir data
RUN pip install -r requirements.txt
VOLUME data
ENTRYPOINT hug -f urlo.py
