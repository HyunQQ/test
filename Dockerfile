FROM python:3.7

WORKDIR /app
RUN apt -y update
RUN apt -y install sqlite3

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .  ./

# wsgi 서버는 평가에 필요한 요소가 아니라서 따로 설정하지 않으셔도 됩니다.
# 단, 수정한다고 해도 포트는 유지해주세요
CMD python manage.py makemigrations --noinput
CMD python manage.py migrate --noinput
CMD python manage.py runserver 0.0.0.0:28172

EXPOSE 28172
