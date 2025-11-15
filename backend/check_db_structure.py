"""
Check database structure
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "bossboard.db")

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(0)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking companies table structure:")
print("-" * 50)
cursor.execute("PRAGMA table_info(companies)")
columns = cursor.fetchall()

for col in columns:
    print(f"Column: {col[1]}, Type: {col[2]}, Nullable: {not col[3]}")

print("-" * 50)
print(f"Total columns: {len(columns)}")

conn.close()

