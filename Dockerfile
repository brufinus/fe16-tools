FROM python:slim

#ENV FLASK_APP=tools.py

COPY app app
COPY migrations migrations
COPY app.db boot.sh config.py requirements.txt tools.py ./
RUN pip install -r requirements.txt && \
    pip install gunicorn && \
    chmod a+x tools.py

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]
