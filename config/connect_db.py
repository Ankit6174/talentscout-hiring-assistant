import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Get Client
def get_client():
    """
    Create a MongoDB client.

    Try to connect to the cloud MongoDB instance using the connection string
    from environment variables. If the connection fails, return the local MongoDB instance.

    Returns:
        MongoClient: A connected MongoDB client instance.
    """
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
    """
    Get a MongoDB database from the client.

    Args:
        client: MongoClient = The MongoDB client.
        database_name: str = Name of the database.

    Returns:
        Database: The MongoDB database object, or None if retrieval fails.
    """
    try:
        database = client[database_name]
        return database
    except Exception as e:
        print("Failed to get database:", e)
        return None

# Get collection
def get_collection(database_name: str, collection_name: str):
    """
    Retrieve a MongoDB collection.

    Args:
        database_name: str = Name of the database.
        collection_name: str = Name of the collection.

    Returns:
        Collection: The MongoDB collection object, or None if retrieval fails.
    """
    client = get_client()
    database = get_database(client=client, database_name=database_name)
    
    try:
        collection = database[collection_name]
        return collection
    except Exception as e:
        print(f"failed to get collection: {e}")
        return None