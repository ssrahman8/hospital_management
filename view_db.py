import sqlite3

def view_database_structure():
    conn = sqlite3.connect('instance/hospital.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Database Tables:")
    print("-" * 20)
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == '__main__':
    view_database_structure()
