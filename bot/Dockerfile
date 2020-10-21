FROM gorialis/discord.py:minimal

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN sudo apt update
RUN sudo apt-get install gcc musl-dev
RUN pip install -r requirements.txt --upgrade