FROM python:3.8.1

COPY . /web/app

RUN apt-get update \
    && mkdir static \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    && python -m pip install -r /web/app/requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && ls -la

WORKDIR /web/app/src

CMD ["start_django.sh"]
