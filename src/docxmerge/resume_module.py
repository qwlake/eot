import sys, os, zipfile, base64, hashlib, subprocess, re
from datetime import datetime, time
from threading import Thread

from django.conf import settings
from Crypto import Random
from Crypto.Cipher import AES
from pdf2image import convert_from_path

from .models import Resume, ResumeMerged
from . import resume_config

class AESCipher():
    
    def __init__(self):
        key = resume_config.SECRET_KEY[:32] # AES-256
        self.bs = 32
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def docx_to_pdf(source, timeout=None):
    class LibreOfficeError(Exception):
        def __init__(self, output):
            self.output = output

    source = os.path.abspath(source)
    folder = source[:source.rfind("/")]
    args = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', folder, source]

    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)

def libreoffice_exec():
    if sys.platform == 'darwin':
        return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    return 'libreoffice'

# Main
def merge(info, resume_info):

    aes = AESCipher()
    date = datetime.now().strftime("%Y. %m. %d.")
    replace_text = resume_config.requests(date, info)

    try:
        # 작업 실행 시간
        create_time = datetime.today().strftime("%Y%m%d%H%M%S")

        user_enc = aes.encrypt(resume_info.user.username + '-' + create_time)
        user_enc = user_enc.replace('/', '_')
        user_path = 'media/resume_users/' + user_enc

        # User 폴더가 없으면(신규 유저이면) User의 폴더 생성
        if not os.path.isdir('media/resume_users/'):
            os.mkdir('media/resume_users/')
        if not os.path.isdir(user_path):
            os.mkdir(user_path)

        template_name_list = []
        new_name_list = []
        pdf_name_list = []
        img_name_list = []
        resume_merged_list = []

        # docx 파일 템플릿 리스트
        # media/resume_templates/template.docx
        template_url_list = []
        for res in Resume.objects.all():
            template_url_list.append(res.file.url[1:])
            resume_merged = ResumeMerged()
            resume_merged.user = resume_info.user
            resume_merged.resume = res
            resume_merged.resume_info = resume_info
            resume_merged_list.append(resume_merged)

        for template_url in template_url_list:
            template_name_list.append(template_url[template_url.rfind("/")+1:])

        for template_name, template_url, resume_merged in zip(template_name_list, template_url_list, resume_merged_list):

            # 생성될 파일 경로 및 이름
            # user_path = media/resume_users/{user_enc}
            # new_name = {resume_info.user}-{template_name}
            new_name = f"{resume_info.user.username}-{template_name}"
            pdf_name = f"{resume_info.user.username}-{template_name[:template_name.rfind('.')]}.pdf"
            img_name = f"{resume_info.user.username}-{template_name[:template_name.rfind('.')]}.png"
            new_name_list.append(new_name)
            pdf_name_list.append(pdf_name)
            img_name_list.append(img_name)

            user_path_without_media = user_path[user_path.find('/')+1:]
            resume_merged.docx_file = f"{user_path_without_media}/{new_name}"
            resume_merged.pdf_file = f"{user_path_without_media}/{pdf_name}"
            resume_merged.img_file = f"{user_path_without_media}/{img_name}"
            resume_merged.save()

            # 병합될 파일
            new_docx = zipfile.ZipFile(f"{user_path}/{new_name}", 'a')

            # docx 파일 템플릿
            template_docx = zipfile.ZipFile(template_url)

            # 템플릿 파일을 xml 포맷으로 압축 해제
            with open(template_docx.extract("word/document.xml"), encoding='UTF8') as temp_xml_file:
                temp_xml_str = temp_xml_file.read()

            # 템플릿의 변수들을 user의 정보로 교체
            for key in replace_text.keys():
                temp_xml_str = temp_xml_str.replace(str(key), str(replace_text.get(key)))

            # 병합된 정보를 xml 파일로 임시 저장
            with open("word/temp.xml", "w+", encoding='UTF8') as temp_xml_file:
                temp_xml_file.write(temp_xml_str)

            # 임시저장된 병합정보를 파일에 쓰기
            for file in template_docx.filelist:
                if not file.filename == "word/document.xml":
                    new_docx.writestr(file.filename, template_docx.read(file))
            new_docx.write("word/temp.xml", "word/document.xml")
            template_docx.close()
            new_docx.close()
        print("-----------------------------Merge complete------------------------------------")

        # convert docx to pdf with thread
        starttime = datetime.now()
        threads = []
        for new_name in new_name_list:
            t = Thread(target=docx_to_pdf, args=(f"{user_path}/{new_name}",))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print("convert end", datetime.now() - starttime)

        # convert pdf to image
        for pdf_name, img_name in zip(pdf_name_list, img_name_list):
            pdf_name = os.path.abspath(f"{user_path}/{pdf_name}")
            img_name = os.path.abspath(f"{user_path}/{img_name}")
            pages = convert_from_path(pdf_name, 300)
            for page in pages:
                page.save(img_name, 'PNG')

        ## convert docx to pdf with non-thread
        # starttime = datetime.now()
        # for new_name, pdf_name in zip(new_name_list, pdf_name_list):
        #     # pdf로 변환 및 static 경로 저장
        #     docx_to_pdf(new_name, pdf_name)
        # print(datetime.now() - starttime)
        print("-------------------------Convert to pdf complete-------------------------------")

    except Exception as ex:
        raise ex
    return resume_merged_list
