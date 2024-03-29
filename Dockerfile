FROM python:3.11.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org/ | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

ADD poetry.lock pyproject.toml /
RUN poetry install --no-dev

WORKDIR /app

ADD . /app/

CMD ["sh", "run.sh"]