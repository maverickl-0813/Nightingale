#!/usr/bin/env bash

DATA_DIR=med_data

# docker run -p 27017:27017 --name mongo -v $(pwd)/${DATA_DIR}:/data/db -d mongodb/mongodb-community-server:latest
docker start mongo
