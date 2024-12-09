from pymongo import MongoClient
import json
import argparse
from jsonschema import validate, ValidationError
import requests
'''
Este codigo es para el caso 2: Diseño propio.
Donde realizo un diseño de la base de datos a mi consideración en base a lo contenido en el json.
'''

# Conexión al cliente de MongoDB
client = MongoClient('localhost')

# Selección de la base de datos y colección
db = client['Sales']
col = db['History_Sales']

#Variables API
url = "https://services.test.sw.com.mx/v3/cfdi33/issue/json/v4"
token = "[AGREGAR TOKEN]"
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
    
# Función para cargar el esquema
def load_schema(schema_path):
    try:
        with open(schema_path,"r") as f:
            schema_doc = json.load(f)
            return schema_doc
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
    
def clean_data(data):
    if isinstance(data, list):
        # Limpiar cada documento en la lista
        return [clean_document(doc) for doc in data]
    elif isinstance(data, dict):
        # Limpiar un único documento
        return clean_document(data)
    return data

def clean_document(doc):
    # Campos que quieres conservar
    allowed_fields = {
      "products",
      "id", "product", "price_sale", "quantity", "subtotal", "total",
      "client_id",
      "salebox_id",
      "cash_cut_id",
      "discount_percent",
      "discount_money",
      "total",
      "document_type",
      "date_sale",
      "status",
      "currency",
      }
    return {key: value for key, value in doc.items() if key in allowed_fields}

# Bloque principal
if __name__ == "__main__":
    # Configuración de argparse
    parser = argparse.ArgumentParser(description="Insertar datos JSON en MongoDB")
    parser.add_argument("--file", required=True, help="Ruta al archivo JSON")
    parser.add_argument("--schema", required=True, help="Ruta al archivo del esquema JSON")
    
    args = parser.parse_args()

    schema = load_schema(args.schema)
    if not schema:
        print("No se pudo cargar el esquema. Revisa el archivo y vuelve a intentarlo.")
        exit(1)
    
    # Leer y procesar el archivo JSON
    json_data = read(args.file)
    if json_data:
        # Limpieza de datos
        cleaned_data = clean_data(json_data)
        
        # Validación
        if isinstance(cleaned_data, list):  # Lista de documentos
            valid_data = [doc for doc in cleaned_data if validate_json(doc, schema)]
            if valid_data:
                result = col.insert_many(valid_data)
                print(f"Datos guardados correctamente con IDs: {result.inserted_ids}")
                json_data.pop('_id', None)
            else:
                print("Ningún documento pasó la validación.")
        else:  # Documento único
            if validate_json(cleaned_data, schema):
                result = col.insert_one(cleaned_data)
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