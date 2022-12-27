FROM python:3.10.7-slim-buster

WORKDIR app/auth

ADD requirements.txt app/auth/requirements.txt

RUN pip3 install -r app/auth/requirements.txt

COPY . /app/auth

EXPOSE 5000

CMD ["flask","run", "--host=0.0.0.0","-p 5000"]


