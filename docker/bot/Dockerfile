FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/RustROOMBot

RUN adduser --disabled-password --force-badname --gecos "" RustROOMBot 
RUN usermod -a -G RustROOMBot RustROOMBot

ENV PROJECT_HOME=/home/RustROOMBot/vk_bot
RUN mkdir -p ${PROJECT_HOME}
WORKDIR ${PROJECT_HOME}

COPY ./docker/ ./docker/
COPY ./utils/ ./utils/
COPY ./app/ ./app/
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./Makefile .

RUN chmod +x ${PROJECT_HOME}/docker/bot/entrypoint.sh

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir poetry
RUN python -m poetry config virtualenvs.create false
RUN python -m poetry install --no-dev

RUN chown -R RustROOMBot:RustROOMBot ${PROJECT_HOME}

USER RustROOMBot

ENTRYPOINT ["/bin/sh", "/home/RustROOMBot/vk_bot/docker/bot/entrypoint.sh"]