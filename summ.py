# from datetime import datetime
# from zoneinfo import ZoneInfo  # Available in Python 3.9+

# ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))
# print("Current IST Date and Time:", ist_now.strftime("%Y-%m-%d %H:%M:%S"))

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
import os

# === CONFIGURATION ===
# Load configuration from environment variables - NEVER hardcode production credentials!
RDS_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'DSR')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_PORT = int(os.getenv('DB_PORT', '3306'))

# Prefer DATABASE_URL from environment if available
DATABASE_URL = os.getenv('DATABASE_URL') or f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{RDS_HOST}:{DB_PORT}/{DB_NAME}'

# === CREATE ENGINE ===
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# === INSPECT AND PRINT TABLES ===
inspector = inspect(engine)
tables = inspector.get_table_names()

print("📦 Available Tables in the Database:")
for i, table in enumerate(tables, start=1):
    print(f"{i}. {table}")

# === PREVIEW A TABLE (Optional) ===
if tables:
    print("\n📊 Previewing first 5 rows from table:", tables[0])
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM `{tables[0]}` LIMIT 5"))
        for row in result:
            print(row)

# Close session
session.close()
