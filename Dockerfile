FROM python:3.10.5-alpine

ENV FLASK_APP chatbot.py
ENV FLASK_DEBUG=1

RUN adduser -D chatty
USER chatty

WORKDIR /home/chatty

COPY requirements.txt requirements.txt
COPY ./ChatterBot-spacy_fixed ./
RUN python -m venv venv
RUN venv/bin/pip install ./ChatterBot-spacy_fixed
RUN venv/bin/pip install chatterbot-corpus
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY chatbot.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]



