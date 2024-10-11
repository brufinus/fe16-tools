FROM python:slim

COPY app app
COPY migrations migrations
COPY app.db boot.sh config.py requirements.txt tools.py ./
RUN pip install -r requirements.txt && \
    pip install gunicorn && \
    chmod a+x tools.py boot.sh

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]
