#!/bin/bash

source common.sh

# Backup MongoDB collections to JSON files
backup_mongodb_collections() {
  connect_to_mongodb
  mongodump --db $MONGO_DB --out backup_dir
  disconnect_from_mongodb
}

# Main execution
backup_mongodb_collections
