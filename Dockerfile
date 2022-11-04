FROM python:3.7-slim as builder

RUN apt-get -y update && \
    apt-get install -y git && \
    apt-get install wget

ENV APP_HOME /app
WORKDIR ${APP_HOME}
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN git clone https://github.com/tensorflow/models.git tensorflow_models
ENV PYTHONPATH=${APP_HOME}:${APP_HOME}/tensorflow_models/research:${APP_HOME}/tensorflow_models/research/slim:${APP_HOME}/tensorflow_models/research/object_detection
ADD src/main .

WORKDIR /app
ENTRYPOINT ["python3", "/app/run.py"]

# Add test, building on
FROM builder as testrunner
RUN pip3 install nose==1.3.7
ADD src/test /test
COPY data/annotations /data/annotations
COPY data/imgs /data/imgs
RUN nosetests /test/test.py || true
