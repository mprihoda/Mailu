FROM python:3-alpine

RUN mkdir -p /app
WORKDIR /app

COPY requirements-prod.txt requirements.txt
RUN apk add --no-cache libressl \
 && apk add --no-cache --virtual build-dep libressl-dev libffi-dev python-dev build-base musl-dev mariadb-dev \
 && pip install -r requirements.txt \
 && apk del build-dep
RUN apk --update add mariadb-client-libs

COPY drupal_auth ./drupal_auth
COPY mailu ./mailu
COPY migrations ./migrations
COPY manage.py .
COPY start.sh /start.sh

RUN pybabel compile -d mailu/translations

EXPOSE 80/tcp

CMD ["/start.sh"]
