# -*- coding: utf-8 -*-

import hashlib
import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    password = request.form['password']
    hash_pass = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('ET.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (nombre TEXT, hash_pass TEXT)''')

    c.execute("INSERT INTO usuarios VALUES (?, ?)", (nombre, hash_pass))
    conn.commit()
    conn.close()

    return 'Usuario registrado correctamente'

@app.route('/login', methods=['POST'])
def login():
    nombre = request.form['nombre']
    password = request.form['password']
    hash_pass = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('ET.db')
    c = conn.cursor()

    c.execute("SELECT hash_pass FROM usuarios WHERE nombre=?", (nombre,))
    result = c.fetchone()
    conn.close()

    if result is not None and result[0] == hash_pass:
        return 'Inicio de sesión exitoso'
    else:
        return 'Inicio de sesión fallido'

if __name__ == '__main__':
    app.run(port=9500)
