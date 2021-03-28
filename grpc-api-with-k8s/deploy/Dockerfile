FROM arm32v7/python:3.8-alpine:latest AS base
RUN mkdir /app
WORKDIR /app

COPY ../app /app

ENV PORT='localhost:5001' \
    LANG='C.UTF-8'

RUN apt-get update && apt-get -y install \
    gcc \
    g++

RUN pip install --no-cache-dir --upgrade \
    absl-py~=0.12.0 \
    certifi==2020.12.5 \
    grpc-interceptor==0.13.0

# minimal deployment image
FROM base AS deploy
CMD ["python3 main.py"]

# image for debugging and dev work
FROM base AS dev
ENV JUPYTER_ENABLE_LAB=yes

RUN apt update && apt install -y \
    build-essential \
    curl \
    wget

RUN pip install --no-cache-dir --upgrade \
    jupyter==1.0.0 \
    jupyterlab==3.0.12

CMD ["python3 main.py"]