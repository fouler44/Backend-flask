from flask  import Flask
import os
from dotenv import load_dotenv
from config.db import init_db, mysql

#Importar la ruta del blueprint
from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp

#Cargar variables de entorno
load_dotenv()


def create_app():   #<-Funcion para crear la app
    
    #Instancia de la App
    app=Flask(__name__)
    
    #Configurar la base de datos
    init_db(app)

    #Registrar blueprint/ruta
    app.register_blueprint(tareas_bp, url_prefix='/tareas')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    
    return app


#Crear app
app = create_app()

if __name__ == "__main__":
    
    #Obtener el puerto
    port=int(os.getenv("PORT",8080))
    
    #Correr app
    app.run(host="0.0.0.0",port=port, debug=True)