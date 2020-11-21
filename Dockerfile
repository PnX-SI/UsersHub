FROM node:12-alpine3.11 AS node-builder

COPY app/static /app/static

WORKDIR /app/static 

RUN npm ci

FROM python:3.7-buster

RUN apt-get update && apt-get upgrade -y && apt-get install -y locales && \
    localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8
ENV LANG fr_FR.utf8

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

COPY --from=node-builder /app/static/node_modules /app/app/static/node_modules

VOLUME /app/app/config

EXPOSE 5001

RUN rm -rf /var/lib/apt/lists/* 

CMD ["gunicorn", "--access-logfile","-" ,"-b", "0.0.0.0:5001", "server:app"]
