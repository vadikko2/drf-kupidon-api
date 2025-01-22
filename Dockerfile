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

EXPOSE 80
CMD ["python", "/code/kupidon/manage.py", "runserver", "0.0.0.0:80"]
