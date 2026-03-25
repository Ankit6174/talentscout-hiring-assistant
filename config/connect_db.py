import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Get Client
def get_client():
    try:
        client = MongoClient(os.environ["MONGO_CONNECTION_STRING"])

        print("Connected to cloud database.")
    except Exception as e:
        print("Cloud DB failed:", e)
        
        client = MongoClient("mongodb://localhost:27017")  
        print("Connected to local database.")

    return client

# Get database
def get_database(client, database_name: str):
    try:
        database = client[database_name]
        return database
    except Exception as e:
        print("Failed to get database:", e)
        return None

# Get collection
def get_collection(database_name: str, collection_name: str):
    client = get_client()
    database = get_database(client=client, database_name=database_name)
    
    try:
        collection = database[collection_name]
        return collection
    except Exception as e:
        print(f"failed to get collection: {e}")
        return None