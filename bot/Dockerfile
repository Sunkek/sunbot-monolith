FROM gorialis/discord.py:minimal

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN apt-get python3-dev musl-dev
RUN pip install -r requirements.txt --upgrade