FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED=1 COLUMNS=200 \
    PYTHONPATH="${PYTHONPATH}:/src" \
    TZ=UTC PIP_CONFIG_FILE=/src/pip.conf

WORKDIR /src

ADD \
    ./src/poetry.toml \
    ./src/poetry.lock \
    ./src/pyproject.toml \
    ./src/pip.conf \
    /src/

RUN apt update \
    && apt install --yes \
    --no-install-recommends \
    apt-utils g++ \
# convenience tools
    netcat-traditional \
# set timezone
    && echo "UTC" > /etc/timezone \
# upgrade pip
    && pip install --upgrade pip \
# add project dependencies
    && pip install poetry==1.7.1 \
    && poetry install --no-root \
# remove build dependencies
    && apt purge --yes g++ apt-utils \
    && apt clean autoremove --yes

COPY ./src /src

CMD ["./entrypoint.sh"]
