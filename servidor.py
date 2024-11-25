import os
from dotenv import load_dotenv
from flask import Flask, request, Response
import mysql.connector
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

# Cargar las variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin"),
    "database": os.getenv("DB_NAME", "Biblioteca"),
}

# Clase para manejar la base de datos
class BaseDeDatos:
    def __init__(self, config):
        self.config = config

    def ejecutar_consulta(self, consulta, parametros=None):
        conexion = mysql.connector.connect(**self.config)
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(consulta, parametros)
            if consulta.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexion.close()

# Crear instancia de la base de datos
db = BaseDeDatos(db_config)

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta para manejar solicitudes SOAP
@app.route("/soap", methods=["POST"])
def soap_service():
    # Parsear el contenido de la solicitud
    soap_request = request.data.decode("utf-8")
    if "crear_libro" in soap_request:
        return crear_libro_soap(soap_request)
    elif "leer_libro" in soap_request:
        return leer_libro_soap(soap_request)
    elif "actualizar_libro" in soap_request:
        return actualizar_libro_soap(soap_request)
    elif "eliminar_libro" in soap_request:
        return eliminar_libro_soap(soap_request)
    else:
        return Response("Método SOAP no soportado", status=400)

# Métodos SOAP
def crear_libro_soap(soap_request):
    # Extraer parámetros desde el XML
    id_libro, titulo, autor = extraer_parametros_soap(soap_request, ["id_libro", "titulo", "autor"])
    
    consulta = "INSERT INTO Libros (id, titulo, autor) VALUES (%s, %s, %s)"
    try:
        db.ejecutar_consulta(consulta, (id_libro, titulo, autor))
        return generar_respuesta_soap(f"Libro '{titulo}' creado con éxito.")
    except mysql.connector.Error as e:
        return generar_respuesta_soap(f"Error al crear el libro: {str(e)}", error=True)

def leer_libro_soap(soap_request):
    id_libro = extraer_parametros_soap(soap_request, ["id_libro"])[0]
    
    consulta = "SELECT * FROM Libros WHERE id = %s"
    resultado = db.ejecutar_consulta(consulta, (id_libro,))
    if resultado:
        libro = resultado[0]
        return generar_respuesta_soap(f"ID: {libro['id']}, Título: {libro['titulo']}, Autor: {libro['autor']}")
    return generar_respuesta_soap("Libro no encontrado.", error=True)

def actualizar_libro_soap(soap_request):
    id_libro, titulo, autor = extraer_parametros_soap(soap_request, ["id_libro", "titulo", "autor"])
    
    consulta = "UPDATE Libros SET titulo = %s, autor = %s WHERE id = %s"
    try:
        db.ejecutar_consulta(consulta, (titulo, autor, id_libro))
        return generar_respuesta_soap(f"Libro '{id_libro}' actualizado con éxito.")
    except mysql.connector.Error as e:
        return generar_respuesta_soap(f"Error al actualizar el libro: {str(e)}", error=True)

def eliminar_libro_soap(soap_request):
    id_libro = extraer_parametros_soap(soap_request, ["id_libro"])[0]
    
    consulta = "DELETE FROM Libros WHERE id = %s"
    try:
        db.ejecutar_consulta(consulta, (id_libro,))
        return generar_respuesta_soap(f"Libro '{id_libro}' eliminado con éxito.")
    except mysql.connector.Error as e:
        return generar_respuesta_soap(f"Error al eliminar el libro: {str(e)}", error=True)

# Función para extraer parámetros desde un XML
def extraer_parametros_soap(xml, parametros):
    import re
    valores = []
    for parametro in parametros:
        match = re.search(f"<{parametro}>(.*?)</{parametro}>", xml)
        valores.append(match.group(1) if match else None)
    return valores

# Función para generar una respuesta SOAP
def generar_respuesta_soap(mensaje, error=False):
    envelope = Element("soap:Envelope", attrib={"xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/"})
    body = SubElement(envelope, "soap:Body")
    response = SubElement(body, "Response")
    status = SubElement(response, "Status")
    status.text = "Error" if error else "Success"
    message = SubElement(response, "Message")
    message.text = mensaje
    xml_str = tostring(envelope, encoding="unicode")
    pretty_xml = parseString(xml_str).toprettyxml()
    return Response(pretty_xml, content_type="text/xml")

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host="localhost", port=8000)
