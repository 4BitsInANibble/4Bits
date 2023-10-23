import pymysql
import random
from flask_socketio import SocketIO
import time

#configuration values

endpoint = 'db-4bits-user-account.c1nbk7rnbxhm.us-east-1.rds.amazonaws.com'
username = 'admin'
password = ''   #enter the password from shared credential here
database_name = 'users'


def execute_queries(host, user, password, database):
    
    # Establish the connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)

    print('Connected to the database')
    
    cursor = connection.cursor()
    
    # List of queries to execute
    queries = [
        
        """
        CREATE TABLE IF NOT EXISTS Users (
            UserID VARCHAR(255) PRIMARY KEY,
            UserName VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Pantry (
            UserID VARCHAR(255),
            ItemName VARCHAR(255),
            Quantity DOUBLE,
            Unit VARCHAR(255),
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS SavedRecipes (
            UserID VARCHAR(255),
            RecipeID INT,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        );
        """,
        """
        INSERT INTO Users (UserID, UserName) VALUES 
        ('cc6956', 'Calvin'),
        ('gt2125', 'Gayatri'),
        ('yh3595', 'Jason'),
        ('nz2065', 'Nashra');
        """,
        """
        INSERT INTO Pantry (UserID, ItemName, Quantity, Unit) VALUES 
        ('cc6956', 'chicken breast', 1, 'lb'),
        ('cc6956', 'soy sauce', 1, 'gal'),
        ('gt2125', 'romaine lettace', 1, 'lb'),
        ('gt2125', 'egg', 24, 'count'),
        ('yh3595', 'steak', 3, 'lb'),
        ('yh3595', 'potatoes', 5, 'count'),
        ('nz2065', 'chicken thigh', 0.25, 'lb'),
        ('nz2065', 'grapes', 5, 'count');
        """,
        "CREATE INDEX idx_pantry_userID ON Pantry (UserID);",
        "CREATE INDEX idx_savedRecipes_userID ON SavedRecipes (UserID);"
    ]
    
    # Execute each query
    for query in queries:
        cursor.execute(query)
    
    # Commit the transactions
    connection.commit()
    
    print('Queries executed successfully')
    cursor.close()
    connection.close()
    print('Connection closed')



execute_queries(endpoint, username, password, database_name)
