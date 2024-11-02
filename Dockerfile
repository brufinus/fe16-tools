FROM python:slim AS build-prod

COPY app app
COPY migrations migrations
COPY boot.sh config.py requirements.txt tools.py ./
RUN pip install -r requirements.txt && \
    pip install gunicorn && \
    chmod a+x tools.py boot.sh

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]

FROM build-prod AS build-dev

COPY app.db ./

FROM build-dev AS build-test

COPY boot_test.sh boot.sh
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    chmod a+x boot.sh
