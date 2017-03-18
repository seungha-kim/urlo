FROM python:3
EXPOSE 8000
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app/
RUN mkdir -p data
VOLUME data
ENTRYPOINT hug -f urlo.py
