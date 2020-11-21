FROM python:3.7-buster

RUN apt-get update && apt-get upgrade -y && apt-get install -y locales nodejs npm && \
    localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8
ENV LANG fr_FR.utf8

WORKDIR /app

COPY . /app

RUN cd ./app/static && npm install 
RUN pip3 install -r requirements.txt

VOLUME /app/app/config

EXPOSE 5001

RUN rm -rf /var/lib/apt/lists/* 


CMD ["gunicorn", "--access-logfile","-" ,"-b", "0.0.0.0:5001", "server:app"]
