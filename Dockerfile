# 우분투 초기 설정
FROM ubuntu:18.04
RUN sed -i 's@archive.ubuntu.com@kr.archive.ubuntu.com@g' /etc/apt/sources.list
RUN apt-get -y update && apt-get -y dist-upgrade
RUN apt-get install -y apt-utils dialog libpq-dev  

# python 설치
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

# python에서 필요한 패키지 설치
RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip3 install -r /config/requirements.txt
RUN mkdir /src;
WORKDIR /src