from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

#Cargar de .env las variables de entorno
load_dotenv()

#Crear instancia de mysql 
mysql = MySQL()

#Funcion para conectarme a la base de datos
def init_db(app):
    #Configuramos la BD con la instancia de Flask
    app.config['MYSQL_HOST']= os.getenv("DB_HOST")
    app.config['MYSQL_USER']= os.getenv("DB_USER")
    app.config['MYSQL_PASSWORD']= os.getenv("DB_PASSWORD")
    app.config['MYSQL_DB']= os.getenv("DB_NAME")
    app.config['MYSQL_PORT']= int(os.getenv("DB_PORT"))
    
    #Iniciar conexion
    mysql.init_app(app)

#Definimos cursor
def get_db_connection():
    #Nos devuelve un cursor para interactuar con la BD
    try:
        connection= mysql.connection
        return connection.cursor()
    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")