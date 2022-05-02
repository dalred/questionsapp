FROM python:3.8-slim
WORKDIR /code
COPY . .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  \
    && pip install psycopg2
RUN pip install -r requirements.txt


