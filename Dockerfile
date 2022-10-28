FROM python:3.10-slim as builder

RUN apt-get -y update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y git && \
    apt-get install wget

ENV APP_HOME /app
WORKDIR ${APP_HOME}
ADD requirements.txt .
RUN pip3 install -r requirements.txt
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
