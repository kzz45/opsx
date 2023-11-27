FROM python:3.11.3

LABEL maintainer="kzz45@qq.com"

WORKDIR /code

COPY . .

RUN pip install -r ./requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

EXPOSE 8080