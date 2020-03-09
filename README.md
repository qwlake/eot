# LikeLion_Center_Hackerthon

멋쟁이 사자처럼 7기 중앙 해커톤

서비스명 : 이옷 (이력서 옷입히기)

## Environment:

```
win10 64bit
python 3.7.6
Django 2.2.2
```


## Quitck start:

```python
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

* 사이트를 사용하기 위해서는 관리자로 로그인 한 후에 `이력서 템플릿 업로드` 버튼을 통해 템플릿을 업로드 하여야 한다. 이력서 템플릿 샘플 양식 : https://drive.google.com/open?id=1xBq-Ji-HjcOYOY61SFWuUuQKj0p_mdoK
* PDF to Image 기능을 사용하기 위해서는 다음의 작업을 해야한다.
```
http://blog.alivate.com.au/wp-content/uploads/2018/10/poppler-0.68.0_x86.7z
1. 위 링크에서 압축 파일 다운 후 `C:\Program Files`에 압축 해제
2. `C:\Program Files\poppler-0.68.0\bin`를 `환경 변수`의 `Path`에 추가
3. 재부팅
```


#### Errors
에러 메세지:
```
...
import win32api, sys, os
ImportError: DLL load failed: 지정된 프로시저를 찾을 수 없습니다.
```
조치 방법:
```
pip uninstall pypiwin32 pywin32
pip install pywin32
```


## Apps informations

project : 프로젝트의 기본 메인 App, Settings 등의 정보 포함.

indexapp : 메인 화면(index) 담당 하는 App.

users : 유저 로그인 및 정보 관리.

docxmerge : 이력서 템플릿과 사용자 정보를 합쳐서 보여주는 App.

 

## Others

`media/resume_templates` : 이력서 템플릿이 들어 있는 폴더

`media/resume_users` : 이력서 템플릿에 사용자 정보를 입힌 파일들이 저장된다.

`word` : docx > xml or xml to docx 과정에서 생성되는 임시 파일들이 저장되는 장소.
> 즉, word는 신경 쓰지 않아도 된다.

