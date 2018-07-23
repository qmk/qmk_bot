FROM python:3.6
MAINTAINER Zach White <skullydazed@gmail.com>

WORKDIR /
RUN git clone https://github.com/qmk/qmk_bot.git
WORKDIR /qmk_bot
RUN pip3 install git+git://github.com/qmk/qmk_compiler.git@master
RUN pip3 install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD gunicorn -w 8 -b 0.0.0.0:5000 --max-requests 1000 --max-requests-jitter 100 -t 60 qmk_bot:app
