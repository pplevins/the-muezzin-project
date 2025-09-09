import os

import pymongo
from gridfs import AsyncGridFS
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi


class Database:
    """
    A class that holds the database connection and client,
    implementing a singleton design pattern with lazy initialization.
    """
    _client = None
    _db = None
    _fs = None

    @classmethod
    def get_client(cls):
        """A class method that returns a singleton database client."""
        if cls._client is None:
            mongodb_url = os.environ["MONGODB_URL"]
            cls._client = AsyncMongoClient(
                mongodb_url,
                server_api=pymongo.server_api.ServerApi(version="1", strict=True, deprecation_errors=True))
            cls._db = cls._client[os.environ["MONGODB_DATABASE"]]
            cls._fs = AsyncGridFS(database=cls._db)  # TODO: Add collection parameters.
        return cls._client

    @classmethod
    def get_db_collection(cls, collection_name):
        """A class method that returns a singleton database collection."""
        if cls._db is None:
            cls.get_client()
        return cls._db.get_collection(collection_name)

    @classmethod
    def get_fs(cls):
        """A class method that returns a singleton database GridFS client."""
        if cls._fs is None:
            cls.get_client()
        return cls._fs
