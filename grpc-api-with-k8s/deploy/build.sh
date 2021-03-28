#!/usr/bin/env bash

# build docker image for development and deployment
echo 'Building dev image...'
docker build \
  --target dev
  --build-arg REG=localhost:5000 \
  -t ${REGISTRY}/simple-app-dev:latest \
  .

echo 'Building deployment image...'
docker build \
  --target deployment
  --build-arg REG=localhost:5000 \
  -t ${REGISTRY}/simple-app-deploy:latest \
  .

echo 'END'