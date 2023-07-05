# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt
import sqlite3

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    hashed_password = sha256_crypt.hash(password)

    with sqlite3.connect('ET.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()

    return jsonify({"message": "Usuario registrado con éxito."}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    with sqlite3.connect('ET.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

    if result and sha256_crypt.verify(password, result[0]):
        return jsonify({"message": "Inicio de sesión exitoso."}), 200
    else:
        return jsonify({"message": "Nombre de usuario o contraseña incorrectos."}), 401

@app.route('/')
def home():
    return "¡Bienvenido al sitio web de gestión de claves!"

@app.errorhandler(404)
def page_not_found(e):
    return "Página no encontrada", 404

if __name__ == '__main__':
    with sqlite3.connect('ET.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
        conn.commit()
    
    app.run(host='0.0.0.0', port=9500)
