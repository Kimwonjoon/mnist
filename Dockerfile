FROM python:3.11

WORKDIR /code

COPY src/mnist/main.py /code/
COPY run.sh /code/run.sh

RUN apt update
RUN apt install -y cron
RUN apt install -y vim
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade git+https://github.com/Kimwonjoon/mnist.git@0.3/mnist

CMD ["sh", "run.sh"]
