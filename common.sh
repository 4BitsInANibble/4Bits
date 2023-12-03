#!/bin/bash

echo "importing from common.sh"


DB=recipeDB
USER=nz2065
CONNECT_STR="mongodb+srv://nibble.pcnhctc.mongodb.net/"
export MONGO_DB_PASSWORD=Cbf6EvI2pewBj8KM


if [ -z $DATA_DIR ]
then
    DATA_DIR=/data
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport
IMP=/usr/local/bin/mongoimport

if [ -z $MONGO_DB_PASSWORD ]
then
    echo "You must set MONGO_DB_PASSWD in your env before running this script."
    exit 1
fi


declare -a UserCollections=("Username" "Name" "Pantry" "Saved_Recipes" "Instacart_User_Info" "Grocery List" "Allergens" "Auth_Type" "Auth_Exp" "Password") 