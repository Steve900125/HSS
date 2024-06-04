from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def default():
    return "Sever A run successful"

if __name__ == "__main__":
    app.run(debug=True, port=8100)

