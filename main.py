from pymongo import MongoClient
import json
import argparse
from jsonschema import validate, ValidationError
import requests

'''
Este codigo es para el caso 1: Diseño en base al json.
Donde realizo realizo un schema en base a lo contenido en el JSON, sin modificar nada de su estructura.
'''

# Conexión al cliente de MongoDB
client = MongoClient('localhost')

# Selección de la base de datos y colección
db = client['Sales']
col = db['History_Sales']

#Variables API
url = "https://services.test.sw.com.mx/v3/cfdi33/issue/json/v4"
token = "T2lYQ0t4L0RHVkR4dHZ5Nkk1VHNEakZ3Y0J4Nk9GODZuRyt4cE1wVm5tbXB3YVZxTHdOdHAwVXY2NTdJb1hkREtXTzE3dk9pMmdMdkFDR2xFWFVPUXpTUm9mTG1ySXdZbFNja3FRa0RlYURqbzdzdlI2UUx1WGJiKzViUWY2dnZGbFloUDJ6RjhFTGF4M1BySnJ4cHF0YjUvbmRyWWpjTkVLN3ppd3RxL0dJPQ.T2lYQ0t4L0RHVkR4dHZ5Nkk1VHNEakZ3Y0J4Nk9GODZuRyt4cE1wVm5tbFlVcU92YUJTZWlHU3pER1kySnlXRTF4alNUS0ZWcUlVS0NhelhqaXdnWTRncklVSWVvZlFZMWNyUjVxYUFxMWFxcStUL1IzdGpHRTJqdS9Zakw2UGQrNzJ3UWh4TVVxb0g3TU5KV0Q2Um5rb2VpQlZibFk2b3JLeURxQmU5TGhudldsdjExeGpvaDBEQVZYWUhWTE5nKzh5MENnVm9MRjNwRE5MU0xuOWtRdTNGMktEajgrSlVtcVNPbWpLSE9hajJCZC9zOFBEOVp3VG9BbFRaMkFsSHl4ZkoxSWlQYnRERi9kTCtaMkhWeHROSmlUemxHbEhHbDBIMEdueTh0ZmtSOHUwMVNaempVNnlDNTRLRzhxNmU5VlpIdlhJVDMyZ2V2aDVvQzNjRW1YUFVJeXdHcmdvUmhBdVhCS0xyYi9aRThYR2s2emhjRHRaa1RKUEd0akdvRHZBVDkxa2lwYU5qOTN5aCtlazdIRGNUNzdraWNkdE0xZ3JJYURPRkp5SGk4MGNvZUNqM2lJWFh0WmtCYkc4QUVpa0dTcEZIWVB0ajdnTDFtSThMMkdDY0VIOWJEQUg2d3FBdVNWaGxJWXgxOTVJQXZwSis5OE1BMTR1ZDJzYXI.CQ3rWTEmazC1V426bZlBWWIkzCKOJWP3QeWNaAo7Bfs"
# Cabeceras 
headers_API = {
    "Authorization": "Bearer "+token, 
    "Content-Type": "application/jsontoxml"
}

# Función para leer un archivo JSON
def read(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return None

# Función para cargar el esquema de validación desde un archivo externo
def load_schema(schema_path):
    try:
        with open(schema_path, "r") as f:
            schema = json.load(f)
            return schema
    except Exception as e:
        print(f"Error al cargar el esquema: {e}")
        return None

# Función para validar un documento JSON
def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"Error de validación: {e.message}")
        return False

# Bloque principal
if __name__ == "__main__":
    # Configuración de argparse
    parser = argparse.ArgumentParser(description="Insertar datos JSON en MongoDB.")
    parser.add_argument("--file", required=True, help="Ruta al archivo JSON.")
    parser.add_argument("--schema", required=True, help="Ruta al archivo del esquema JSON.")
    
    args = parser.parse_args()
    
    # Cargar el esquema de validación
    schema = load_schema(args.schema)
    if not schema:
        print("No se pudo cargar el esquema. Revisa el archivo y vuelve a intentarlo.")
        exit(1)
    
    # Leer y guardar el JSON
    json_data = read(args.file)
    # Hacer el POST a la API
    #Almacenar en base de datos Mongodb
    if json_data:
        if isinstance(json_data, list):  # Si el JSON contiene una lista de documentos
            valid_data = [doc for doc in json_data if validate_json(doc, schema)]
            if valid_data:
                result = col.insert_many(valid_data) 
                print(f"Datos guardados correctamente con IDs: {result.inserted_ids}")
                json_data.pop('_id', None)
            else:
                print("Ningún documento pasó la validación.")
        else:  # Si el JSON contiene un solo documento
            if validate_json(json_data, schema):
                result = col.insert_one(json_data)
                print(f"Datos guardados correctamente con ID: {result.inserted_id}")
                json_data.pop('_id', None)
            else:
                print("El documento no pasó la validación.")
    #Realizar POST
    try:
        response = requests.post(url, json=json_data, headers=headers_API)
        # Manejo del response
        if response.status_code == 200 or response.status_code == 201:
            print("Éxito en la solicitud:")
            print(response.json())  # Asume que la respuesta es un JSON
        else:
            print(f"Error en la solicitud: {response.status_code}")
            print(response.text)  # Imprime el cuerpo de la respuesta en caso de error
    except Exception as e:
        print(f"Error al hacer la solicitud POST: {e}")