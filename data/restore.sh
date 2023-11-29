#!/bin/bash

source common.sh

# Restore MongoDB collections from JSON files
restore_mongodb_collections() {
  connect_to_mongodb
  mongorestore --db $MONGO_DB --drop backup_dir/$MONGO_DB
  disconnect_from_mongodb
}

# Main execution
restore_mongodb_collections
