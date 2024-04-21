#!/bin/bash

source common.sh

# Backup MongoDB collections to JSON files
MONGO_DB_PASSWORD = 
for collection in ${UserCollections[@]}; do
    echo "Backing up $collection"
    $EXP --collection=$collection --db=$DB --out=$BKUP_DIR/$collection.json $CONNECT_STR --username $USER --password $MONGO_DB_PASSWORD
done

git add $BKUP_DIR/*.json
git add $BKUP_DIR/*.json
git commit $BKUP_DIR/*.json -m "Mongo DB backup"
git pull origin master
git push origin master