FROM python:3

WORKDIR /running

COPY ./requirements.txt /running/

RUN pip install -r /running/requirements.txt

COPY . .
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1