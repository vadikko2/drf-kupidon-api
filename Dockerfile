FROM python:3.12.2-slim
LABEL maintainer="Vadim Kozyrevskiy" \
      email="vadikko2@mail.ru"

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential libpq-dev libgdal-dev gdal-bin && \
    pip install --no-cache-dir --upgrade pip==24.* && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt --root-user-action=ignore

COPY ./kupidon/ /code/kupidon/

ARG API_ENV
ARG API_SECRET_KEY
ARG API_DOMAIN
ARG DATABASE_NAME
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ARG DATABASE_HOST
ARG DATABASE_PORT

ENV API_ENV=$API_ENV
ENV API_SECRET_KEY=$API_SECRET_KEY
ENV API_DOMAIN=$API_DOMAIN
ENV DATABASE_NAME=$DATABASE_NAME
ENV DATABASE_USER=$DATABASE_USER
ENV DATABASE_PASSWORD=$DATABASE_PASSWORD
ENV DATABASE_HOST=$DATABASE_HOST
ENV DATABASE_PORT=$DATABASE_PORT

# Сбор статики
ENV DJANGO_SETTINGS_MODULE=kupidon.settings
RUN python /code/kupidon/manage.py collectstatic --noinput

EXPOSE 80
CMD ["gunicorn", "--chdir", "/code/kupidon", "kupidon.wsgi:application", "--bind", "0.0.0.0:80"]
