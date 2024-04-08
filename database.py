import psycopg2
from psycopg2.extras import RealDictCursor
import time
from config import settings


def get_db_connection():
    count = 0
    while count < 5:
        try:
            conn = psycopg2.connect(
                host=settings.database_hostname,
                database=settings.database_name,
                user=settings.database_username,
                password=settings.database_password,
                cursor_factory=RealDictCursor
            )
            print("Connected to Database successfully")
            return conn
        except Exception as error:
            print(f"Connection failed {error}")
            time.sleep(2)
            count += 1
