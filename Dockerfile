FROM tensorflow/tensorflow:1.5.0  as builder

RUN apt-get -y update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y python-opencv && \
    apt-get install -y git && \
    apt-get install wget

ENV APP_HOME /app
WORKDIR ${APP_HOME}

# Install needed proto binary and clean
WORKDIR /tmp/protoc3
RUN wget https://github.com/google/protobuf/releases/download/v3.4.0/protoc-3.4.0-linux-x86_64.zip
RUN unzip /tmp/protoc3/protoc-3.4.0-linux-x86_64.zip
RUN mv /tmp/protoc3/bin/* /usr/local/bin/
RUN mv /tmp/protoc3/include/* /usr/local/include/
RUN rm -Rf /tmp/protoc3

WORKDIR ${APP_HOME}
RUN git clone https://github.com/tensorflow/models.git tensorflow_models
ENV PYTHONPATH=${APP_HOME}:${APP_HOME}/tensorflow_models/research:${APP_HOME}/tensorflow_models/research/slim:${APP_HOME}/tensorflow_models/research/object_detection

WORKDIR ${APP_HOME}
RUN pip3 install --upgrade pip
RUN pip3 install opencv-python==3.4.0.12
RUN pip3 install scipy==1.0.1
RUN pip3 install numpy==1.14.2
RUN pip3 install lxml==4.2.1
RUN pip3 install tensorflow==1.5.0
RUN pip3 install pillow==5.1.0
ADD src/main .

ARG DOCKER_GID
ARG DOCKER_UID

# Add non-root user and fix permissions
RUN groupadd --gid $DOCKER_GID docker && adduser --uid $DOCKER_UID --gid $DOCKER_GID --disabled-password --quiet --gecos "" docker_user
RUN chown -Rf docker_user:docker /app

USER docker_user
WORKDIR /app
RUN chown -Rf docker_user:docker /app
ENTRYPOINT ["python3", "/app/run.py"]

# Add test, building on
FROM builder as testrunner
USER root
RUN pip3 install nose==1.3.7
ADD src/test /test
COPY data/annotations /data/annotations
COPY data/imgs /data/imgs
RUN nosetests /test/test.py || true
