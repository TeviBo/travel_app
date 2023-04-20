FROM python:3.11-alpine3.17

ENV PYTHONUNBUFFERED 1

COPY ./requirements/requirements.txt /tmp/requirements.txt
COPY ./requirements/local.txt /tmp/local.txt
COPY ./app /app

WORKDIR /app

EXPOSE 8000

ARG DEV=false

RUN python -m venv /travel_venv && \
        /travel_venv/bin/pip install --upgrade pip && \
        apk add --update --no-cache postgresql-client jpeg-dev && \
        apk add --update --no-cache --virtual .tmp-build-deps \
                build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
        /travel_venv/bin/pip install -r /tmp/requirements.txt && \
        if [ $DEV = "true" ]; \
                then /travel_venv/bin/pip install -r /tmp/local.txt; \
        fi && \
        rm -rf /tmp && \
        apk del .tmp-build-deps && \
        adduser \
                --disabled-password \
                --no-create-home \
                travel-user && \
        mkdir -p /vol/web/media && \
        mkdir -p /vol/web/static && \
        chown -R travel-user:travel-user /vol && \
        chmod -R 755 /vol

ENV PATH="/travel_venv/bin:$PATH"

USER travel-user

CMD ["run.sh"]