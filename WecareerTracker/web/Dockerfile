FROM python:3.6-alpine

#create username otherwise container image user will be root, which is not good practice
# RUN adduser -D tracker

# RUN apk update && \
#     apk add --virtual build-deps gcc python-dev musl-dev && \
#     apk add postgresql-dev && \
#     apk add netcat-openbsd

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev


WORKDIR /home/tracker/web

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY webapp ./webapp
COPY instance ./instance

COPY . .

#make boot.sh an executable file
RUN chmod +x docker-entrypoint.sh

#set the environment inside the container, FLASK_APP is required for flask app
 ENV FLASK_APP webapp

#initialize and migrate the flask migrations
# RUN flask db init
# RUN flask db migrate
# COPY ./migrations migrations/

#dont run the app as root user
# RUN chown -R tracker:tracker ./
# USER tracker

#expose the 8000 port for webserver in the container
EXPOSE 8000
#this is the entry point to startup the webserver. is used instead of CMD
ENTRYPOINT ["./docker-entrypoint.sh"]
