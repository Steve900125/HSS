from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

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

# Function to query documents in DB_A.db
def Qw(target_keywords):
    database = "DB_A.db"
    conn = create_connection(database)
    
    if conn is not None:
        count = query_documents(conn, target_keywords)
        conn.close()
        return count
    else:
        return "Connection failed."

@app.route("/")
def default():
    return "Server A run successful"

@app.route("/A_receive_keywords", methods=["POST"])
def receive_keywords():
    data = request.get_json()
    encrypted_keywords = data.get("keywords", [])
    print(f"Received encrypted keywords: {encrypted_keywords}")
    
    # 模擬解密過程
    decrypted_keywords = [kw[::-1] for kw in encrypted_keywords]
    print(f"Decrypted keywords: {decrypted_keywords}")
    
    # 查詢包含所有解密後關鍵字的文檔數量
    count = Qw(decrypted_keywords)
    return jsonify({"status": "success", "decrypted_keywords": decrypted_keywords, "document_count": count})

if __name__ == "__main__":
    app.run(debug=True, port=8200)
