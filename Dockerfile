FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN chown -R www-data:www-data /app

STOPSIGNAL SIGTERM

ENTRYPOINT ["sh", "./start.sh"]

#CMD [ "./start.sh" ]