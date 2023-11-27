from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # 允许跨域请求

def get_db_connection():
    return mysql.connector.connect(
        host="userinfo.c1i9vodwe6ec.us-east-2.rds.amazonaws.com",
        user="admin",
        password="Wyd200164?",
        database="userinfo"
    )


@app.route('/login', methods=['POST'])  #与前端login交互，查询登陆信息，返回给前端
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        if not username or not password:
            return jsonify({"message": "Both username and password are required!"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if username and password match
        cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Incorrect username or password!"}), 400
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/register', methods=['POST'])       #将前端的注册信息上传到userinfo database
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        if not username or not password:
            return jsonify({"message": "Both username and password are required!"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if username exists
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({"message": "Username already exists!"}), 400
        
        # Insert user
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "User registered successfully!"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)   #避免与chatbot接口5000撞上，这里使用8000port
