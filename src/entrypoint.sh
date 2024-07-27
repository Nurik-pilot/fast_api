#!/bin/bash

wait_for () {
    while ! nc -z "$1" "$2"; do sleep 1; done;
    echo "$1:$2 accepts connections!^_^"
}

wait_backing_services () {
  wait_for "${POSTGRESQL_HOST}" "${POSTGRESQL_PORT}"
  wait_for "${REDIS_HOST}" "${REDIS_PORT}"
  wait_for "${RABBITMQ_HOST}" "${RABBITMQ_PORT}"
  wait_for "${MINIO_HOST}" "${MINIO_PORT}"
}

export $(xargs < /src/core/.env)
echo "env variables are populated!^_^"

case "$PROCESS" in
"TEST")
    wait_backing_services
    doit migrate && doit test \
    --number_of_processes 2 \
    --coverage_report_path \
    "$CI_PROJECT_DIR"/coverage.xml
    ;;
"LINT")
    doit lint
    ;;
"SCAN")
    base_url=https://raw.githubusercontent.com
    suffix=anchore/grype/main/install.sh
    url=${base_url}/${suffix}
    doit safety \
    && apt install -y curl \
    && curl -sSfL $url | sh \
    -s -- -b /usr/local/bin \
    && grype --fail-on CRITICAL .
    ;;
"DEV_FASTAPI")
    wait_backing_services
    poetry install --no-root \
    && doit migrate \
    && uvicorn core.main:app \
    --reload \
    --host 0.0.0.0 \
    --port 8000
    ;;
"DEV_CELERY")
    wait_backing_services
    celery \
    -A core worker \
    --concurrency 1 \
    -B --schedule \
    /tmp/celerybeat-schedule \
    --loglevel INFO
    ;;
"FASTAPI")
    alembic --config \
    /src/db/alembic.ini \
    upgrade head
    uvicorn core.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --proxy-headers \
    --workers 4
    ;;
"CELERY_SCHEDULER")
    celery -A core \
    beat --schedule \
    /tmp/celerybeat-schedule \
    --loglevel INFO
    ;;
"CELERY_CONSUMER")
    celery -A core worker \
    --loglevel INFO \
    --concurrency 4 \
    --max-tasks-per-child 16
    ;;
*)
    echo "NO PROCESS SPECIFIED!>_<"
    exit 1
    ;;
esac
