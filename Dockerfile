FROM python:3.8-slim-buster

LABEL key="Eric" key="ericxmagno@gmail.com"

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "/app/main.py" ]