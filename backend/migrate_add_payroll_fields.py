"""
Migration script to add payroll_day and payroll_time columns to companies table
"""
import sqlite3
import os

# Path to database
db_path = os.path.join(os.path.dirname(__file__), "bossboard.db")

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    print("The database will be created automatically when you run the backend.")
    exit(0)

print(f"Connecting to database: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if payroll_day column exists
    cursor.execute("PRAGMA table_info(companies)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "payroll_day" not in columns:
        print("Adding payroll_day column...")
        cursor.execute("ALTER TABLE companies ADD COLUMN payroll_day INTEGER")
        print("[OK] Added payroll_day column")
    else:
        print("[OK] payroll_day column already exists")
    
    if "payroll_time" not in columns:
        print("Adding payroll_time column...")
        cursor.execute("ALTER TABLE companies ADD COLUMN payroll_time VARCHAR(5)")
        print("[OK] Added payroll_time column")
    else:
        print("[OK] payroll_time column already exists")
    
    conn.commit()
    print("\n[OK] Migration completed successfully!")
    
except Exception as e:
    conn.rollback()
    print(f"[ERROR] Error during migration: {e}")
    raise
finally:
    conn.close()

