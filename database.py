import pymongo
from pymongo.collection import Collection
from typing import Any, Dict


class DBConnection:
    URI: str = "mongodb://localhost:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(DBConnection.URI)
        DBConnection.DATABASE = client["calendar_app"]

    @staticmethod
    def insert(collection: str, data: Dict[str, Any]):
        return DBConnection.DATABASE[collection].insert_one(data)

    @staticmethod
    def find_one(collection: str, query: Dict[str, Any]):
        return DBConnection.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection: str, query: Dict[str, Any]):
        return DBConnection.DATABASE[collection].find(query)

    @staticmethod
    def update_one(collection: str, query: Dict[str, Any], data: Dict[str, Any]):
        return DBConnection.DATABASE[collection].update_one(query, data)

    @staticmethod
    def update_many(collection: str, query: Dict[str, Any], data: Dict[str, Any]):
        return DBConnection.DATABASE[collection].update_many(query, data)

    @staticmethod
    def delete(collection: str, query: Dict[str, Any]):
        return DBConnection.DATABASE[collection].delete_one(query)
