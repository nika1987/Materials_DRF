FROM python:3

WORKDIR /running

COPY ./requirements.txt /running/

RUN pip install -r /running/requirements.txt

COPY . .
