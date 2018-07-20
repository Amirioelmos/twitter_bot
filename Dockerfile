#Download base image python 3.5
FROM python:3.5

WORKDIR /twitter_bot

COPY requirements.txt /twitter_bot

RUN pip install -r requirements.txt

COPY . /twitter_bot

RUN echo "Asia/Tehran" > /etc/timezone

CMD ["python3.5", "bot.py"]

