import sys
import os

# Add the project root to sys.path to allow imports from database and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_db_client
from pymongo.errors import ConnectionFailure

def test_connection():
    client = get_db_client()
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("MongoDB connection: SUCCESS")
    except ConnectionFailure:
        print("MongoDB connection: FAILED")

if __name__ == "__main__":
    test_connection()
