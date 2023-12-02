#!/bin/bash

export FLASK_ENV=development
export PROJ_DIR=$PWD
export DEBUG=1
export MONGO_DB_USERNAME=nz2065
export MONGO_DB_PASSWORD=Cbf6EvI2pewBj8KM
export OPENAI_KEY=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
export JWT_SECRET_KEY=meZzVsL7qhr3epoT
# export CLOUD_MONGO=1

# run our server locally:
PYTHONPATH=$(pwd):$PYTHONPATH
FLASK_APP=server.endpoints flask run --debug --host=127.0.0.1 --port=8000
