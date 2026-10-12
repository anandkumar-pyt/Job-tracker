import sqlite3
def get_db_connection():
    connection=sqlite3.connect("jobs.db")
    connection.row_factory=sqlite3.Row
    return connection
def create_table():
    connection=get_db_connection()
    connection.execute("""
    CREATE TABLE IF NOT EXISTS jobs(id Integer Primary Key AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Applied')""")
    connection.commit()
    connection.close()
if __name__=="__main__":
    create_table()
    print("database created")
    