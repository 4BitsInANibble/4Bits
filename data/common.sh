#!/bin/bash

# MongoDB connection information
MONGO_HOST=""mongodb+srv://nibble.pcnhctc.mongodb.net/""
MONGO_PORT="your_mongodb_port"
MONGO_USER="nz2065"
MONGO_PASSWORD="Cbf6EvI2pewBj8KM"
MONGO_DB="your_mongodb_database"

# Function to establish a MongoDB connection
connect_to_mongodb() {
  mongo --host $MONGO_HOST --port $MONGO_PORT --username $MONGO_USER --password $MONGO_PASSWORD --authenticationDatabase admin --quiet
}

# Function to disconnect from MongoDB
disconnect_from_mongodb() {
  mongo admin --eval "db.shutdownServer()" --quiet
}
