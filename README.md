
# Prueba Tecnica
Requerimientos:
+ Mongodb y Mongosh (Mongodb Compass Opcional)
+ Python 3.0 o Superior

Dependencias a instalar (pyton):
+ pymongo
+ argparse
+ jsonschema
+ request

Estrucura de instalación de dependecias en python:
`pip install [dependencia]`

## GUIA DE EJECUCIÓN

__ACLARACIÓN:__ La guía se hace teniendo en cuenta que se ejecutará en entorno de windows, por lo que algunas cosas pueden cambiar si se realiza en una distribución de linux.

### Paso 1: Ejecución de Mongodb
En este punto se realizaran los comandos para ejecutar mongo y así poder realizar acciones dentro de dicho DBMS.

Ejecutaremos 2 ventanas de cmd como administrador.
en uno se ejecutará el siguiente comando:

- `mongod`

y en el otro se ejecutará lo siguiente:

- `mongosh`

mongod es para inicia el servidor de la base de datos MongoDB.
Y mongosh para conectarse a un servidor MongoDB y para interactuar con la base de datos.

### Paso 2: Ejecución del codigo
__ACLARACIÓN__: Como se puede visualizar en el repositorio, contamos con los siguientes documentos:
```
datasale.json
main.py
main2.py 
schema.json
schema2.json
```
En la prueba se me solicitó diseñar y modelar un schema de base de datos para el JSON `datasale.json`, el problema es que cuando se llegó al tercer punto, que es mandar el json a la API, no tenia una idea clara de que estructura debia tener el documento para obtener un resultado `success`, por lo tanto realicé 2 schema:
- El primero corresponde a la estructura tal cual tiene el documento `datasale.json`. Para ejecutar esta opción se usaran los siguientes documentos: `main.py`, `datasale.json`,`schema.json`
- El segundo corresponde a un diseño y modelado propio, donde se reducen los elementos y solo se conservan valores más generales. Para ejecutar esta opción se requieren los siguientes documentos: `main2.py`, `datasale.json`,`schema2.json`
  
__NOTA__: <ins> En el codigo se tiene un campo llamado "token", por lo que se le recuerda modificar dicha variable con el token para que funcioné el codigo. (eliminar los corchetes) </ins>

Para ejecutar el codigo desde la terminal se ejecutará de la siguiente forma:
- Caso 1: `python main.py --file datasale.json --schema schema.json`
- Caso 2: `python main2.py --file datasale.json --schema schema2.json`



### Resultados
Como se mencionó en el punto anterior, no se mencionó y no se conocía la estructura que debia tener el json para ser aceptado por la API. De hecho, realizando una investigación en la [documentación de la API](https://developers.sw.com.mx/knowledge-base/emision-timbrado-json-cfdi/) y en el mismo [Postman](https://www.postman.com/development-swsapien/sw-api-developers/request/qmumlt3/application-json) que viene en la documentación, y usando los datos de ejemplo que se daban en las dos paginas, no se lograba llegar a un resultado `success`, siempre retornando error. Por lo que el punto de realización del timbrado dio el siguiente resultado:
![Resultados de los dos casos](/resultados.png)

