import sqlite3
import os

# Create database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Create table
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        document TEXT NOT NULL,
        keywords TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# Check if table is empty
def is_table_empty(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM documents")
        count = cur.fetchone()[0]
        return count == 0
    except sqlite3.Error as e:
        print(e)
        return True

# Insert data
def insert_document(conn, document, keywords):
    sql = """
    INSERT INTO documents(document, keywords)
    VALUES(?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, (document, ",".join(keywords)))
    conn.commit()
    return cur.lastrowid

# Query the number of documents containing all target keywords
def query_documents(conn, target_keywords):
    cur = conn.cursor()
    sql = f"""
    SELECT COUNT(*)
    FROM documents
    WHERE {' AND '.join([f'keywords LIKE ?' for _ in target_keywords])}
    """
    query_params = [f'%{keyword}%' for keyword in target_keywords]
    cur.execute(sql, query_params)
    count = cur.fetchone()[0]
    return count

# Initialize database and insert sample data
def main(database):
    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn)
        
        if is_table_empty(conn):
            # Insert sample data
            documents = [
                ("Document 1", ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5", "keyword6", "keyword7", "keyword8", "keyword9", "keyword10"]),
                ("Document 2", ["keyword1", "keyword2", "keyword3", "keyword4", "keyword11", "keyword12", "keyword13", "keyword14", "keyword15", "keyword16"]),
                # More document data can be inserted here
            ]
            
            for doc, kws in documents:
                insert_document(conn, doc, kws)
            
            # Query the number of documents containing all target keywords
            target_keywords = ["keyword1", "keyword2", "keyword3", "keyword4"]
            count = query_documents(conn, target_keywords)
            print(f"Number of documents containing all target keywords: {count}")
        
        conn.close()

if __name__ == '__main__':
    server_a = "DB_A.db"
    server_b = "DB_B.db"
    main(server_a )
    main(server_b )
