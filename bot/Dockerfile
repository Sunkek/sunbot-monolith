FROM gorialis/discord.py:minimal

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt

RUN apk add gcc python3-dev musl-dev
RUN pip install -r requirements.txt --upgrade