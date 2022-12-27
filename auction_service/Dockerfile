FROM python:3.10.7-slim-buster

WORKDIR app/auction

ADD requirements.txt app/auction/requirements.txt

RUN pip3 install -r app/auction/requirements.txt

COPY . /app/auction

EXPOSE 5001

CMD ["flask","run", "--host=0.0.0.0","-p 5001"]
