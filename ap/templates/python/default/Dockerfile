FROM python:alpine3.6

ENV APP_PATH /usr/src/app

RUN mkdir -p $APP_PATH

COPY app $APP_PATH
COPY run.sh /

WORKDIR $APP_PATH

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/run.sh"]

CMD ["python", "app.py"]