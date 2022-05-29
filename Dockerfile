FROM python:3.9
MAINTAINER Zach White <skullydazed@gmail.com>

WORKDIR /qmk_bot
COPY . /qmk_bot
RUN pip3 install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD ./run
