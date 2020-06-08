# 우분투 초기 설정
FROM ubuntu:18.04
RUN sed -i 's@archive.ubuntu.com@mirror.kakao.com@g' /etc/apt/sources.list
RUN apt-get -y update && apt-get -y dist-upgrade
RUN apt-get install -y apt-utils dialog libpq-dev
RUN apt-get install -y libreoffice
RUN apt-get install -y language-selector-gnome fonts-noto-cjk
RUN apt-get install poppler-utils

# python 설치
RUN apt-get install -y python3-pip python3-dev
ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

# 실행 환경 구축
RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip3 install -r /config/requirements.txt

# 작업 디렉토리
RUN mkdir /src;
WORKDIR /src