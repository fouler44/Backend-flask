from flask import Blueprint, request, jsonify
from  flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from flask_bcrypt import Bcrypt
import datetime

from config.db import get_db_connection

import os
from dotenv import load_dotenv

#Cargamos las variables de entorno
load_dotenv()

#crear el blueprint
usuarios_bp = Blueprint('usuarios', __name__)

#Inicializar Bcrypt
bcrypt = Bcrypt()

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    
    #Obtener datos del body
    data = request.get_json()
    
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    #Validacion
    if not nombre or not email or not password:
        return jsonify({"error":"Faltan datos"}), 400
    
    #Obtener cursor de la base de datos
    cursor = get_db_connection()
    
    try:
        #Verificar que el usuario no exista
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return jsonify({"error":"ese usuario ya existe"}), 400
        
        #Hacemos hash al password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        #Insertar el registro del nuevo usario en la base de datos
        cursor.execute('''INSERT INTO usuarios (nombre, email, password) values (%s,%s,%s)''',
                       (nombre,email,hashed_password))
        
        #Guardar el nuevo registro
        cursor.connection.commit()
        
        return jsonify({"mensaje":"El usuario ha sido creado"}), 201
        
    except Exception as e:
        return jsonify({"error":f"Error al registrar al usuario: {str(e)}"}),500
        
    finally:
        #Cerrar el cursor
        cursor.close
                        
@usuarios_bp.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error":"Faltan datos"}), 400
    
    cursor = get_db_connection()
    
    query = "SELECT password, id_usuario FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    
    usuario = cursor.fetchone()
    
    if usuario and bcrypt.check_password_hash(usuario[0], password):
        #Generar el jasonwebtoken
        expires = datetime.timedelta(minutes=60)
        
        access_token = create_access_token(
            identity = str(usuario[1]), 
            expires_delta = expires
        )
        cursor.close()
        return jsonify({"access_token":access_token}), 200
    else:
        return jsonify({"error":"Credenciales Incorrectas"}), 401

@usuarios_bp.route('/datos', methods= ['GET'])
@jwt_required()
def datos():
    
    current_user = get_jwt_identity()
    
    cursor = get_db_connection()
    
    query = "SELECT id_usuario, nombre, email FROM USUARIOS where id_usuario = %s"
    cursor.execute(query, (current_user,))
    usuario = cursor.fetchone()
    
    cursor.close()
    
    if usuario :
        user_info = {
            "id_usuario":usuario[0],
            "nombre":usuario[1],
            "email":usuario[2],
        }
        return jsonify({"Datos":user_info}), 200
    else:
        return jsonify({"Error":"Usuario no encontrado"}), 404