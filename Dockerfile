#Download base image python 3.5
FROM python:3.5

WORKDIR /world_cup_bot
COPY . /world_cup_bot

RUN pip install -r requirements.txt

RUN echo "Asia/Tehran" > /etc/timezone

CMD ["python3.5", "world_cup_bot2.py"]

