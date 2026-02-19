from pymongo import MongoClient
from app.config.config import (
    HOTEL_MONGO_URI
)

database_client = MongoClient(HOTEL_MONGO_URI)
