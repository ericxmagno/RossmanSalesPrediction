FROM python:3.8.6-slim-buster

LABEL key="Eric" key="ericxmagno@gmail.com"

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT [ "python main.py" ]