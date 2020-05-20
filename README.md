# LikeLion_Center_Hackerthon

멋쟁이 사자처럼 7기 중앙 해커톤

서비스명: 이옷 (이력서 옷입히기)<br>
사이트 주소: http://resume-make.shop/<br>
Docker 배포에 관한 자세한 가이드 정리: <br>
[윈도우 장고(Django) 프로젝트 AWS(Ubuntu)에 배포하기 (+gunicorn,Nginx,PostgreSQL,Docker,Docker-compose)](https://newprog.blog.me/221854045564)

![image](https://user-images.githubusercontent.com/41278416/82416379-e41b3300-9ab4-11ea-932e-7f7804bb92a8.png)

## Environment:

```
Ubuntu 18.04
python 3.7.6
Django 2.2.3
gunicorn 20.0.4
psycopg2 2.8.4
nginx latest ver.
postgres latest ver.
```


## Quitck start

먼저 `Docker`와 `docker-compose`의 설치가 필요하다.

* Windows

설치 링크: [Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)

* Ubuntu

```
sudo apt-get install docker docker-compose
```

설치 후 `docker-compose.yml` 파일이 있는 위치로 이동해 아래 명령어로 빌드와 동시에 실행

```
docker-compose up --build
```

#### Note
* 사이트를 사용하기 위해서는 관리자로 로그인 한 후에 `이력서 템플릿 업로드` 버튼을 통해 템플릿을 업로드 하여야 한다. 이력서 템플릿 샘플 양식 : https://drive.google.com/open?id=1xBq-Ji-HjcOYOY61SFWuUuQKj0p_mdoK



## Apps informations

project : 프로젝트의 기본 메인 App, Settings 등의 정보 포함.

indexapp : 메인 화면(index) 담당 하는 App.

users : 유저 로그인 및 정보 관리.

docxmerge : 이력서 템플릿과 사용자 정보를 합쳐서 보여주는 App.

 

## Apps other informations

`media/resume_templates` : 이력서 템플릿이 들어 있는 폴더

`media/resume_users` : 이력서 템플릿에 사용자 정보를 입힌 파일들이 저장된다.

`word` : docx > xml or xml to docx 과정에서 생성되는 임시 파일들이 저장되는 장소.
> 즉, word는 신경 쓰지 않아도 된다.

