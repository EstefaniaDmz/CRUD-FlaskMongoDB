from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://estefania:tec123@cluster0.j3b0jds.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

def dbCnn():
    try: 
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["tarea_db"]
    except ConnectionError:
        print("Error de conexión")
    return db