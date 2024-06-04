from flask import Flask, request
import requests
import json

app = Flask(__name__)

def encrypt(keyword):
    # 模擬加密過程，這裡簡單地將字符串倒序
    return keyword[::-1]

@app.route("/")
def default():
    return "Client run successful"

@app.route("/send_keywords")
def send_keywords():
    # 要發送的關鍵字
    keywords = ["keyword1", "keyword2", "keyword3", "keyword4"]
    
    # 加密關鍵字
    encrypted_keywords = [encrypt(kw) for kw in keywords]
    
    # 發送POST請求到Server A
    data = {"keywords": encrypted_keywords}
    response_a = requests.post("http://localhost:8200/A_receive_keywords", json=data)
    response_b = requests.post("http://localhost:8100/B_receive_keywords", json=data)
    
    result_a = json.loads(response_a.text)
    result_b = json.loads(response_b.text)

    result = 'Server A count : %d Server B count : %d '%(result_a["document_count"], result_b["document_count"]) 

    return result

if __name__ == "__main__":
    app.run(debug=True, port=8300)
