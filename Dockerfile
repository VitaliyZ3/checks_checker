FROM python:3.10.12-slim
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["bash", "./local-runner.sh"]