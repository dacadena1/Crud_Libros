import requests

# Dirección del servidor SOAP
SOAP_URL = "http://localhost:8000/soap"

def menu():
    print("\n=== Cliente SOAP ===")
    print("1. Crear un libro")
    print("2. Leer un libro")
    print("3. Actualizar un libro")
    print("4. Eliminar un libro")
    print("5. Salir")
    opcion = input("Selecciona una opción: ")
    return opcion

def enviar_peticion(xml):
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    try:
        response = requests.post(SOAP_URL, data=xml, headers=headers)
        if response.status_code == 200:
            print("Respuesta del servidor:")
            print(response.text)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print("Error al enviar la petición:", str(e))

def crear_libro():
    print("\n--- Crear Libro ---")
    id_libro = input("ID del libro: ")
    titulo = input("Título del libro: ")
    autor = input("Autor del libro: ")
    
    xml = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <crear_libro>
          <id_libro>{id_libro}</id_libro>
          <titulo>{titulo}</titulo>
          <autor>{autor}</autor>
        </crear_libro>
      </soap:Body>
    </soap:Envelope>
    """
    enviar_peticion(xml)

def leer_libro():
    print("\n--- Leer Libro ---")
    id_libro = input("ID del libro: ")
    
    xml = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <leer_libro>
          <id_libro>{id_libro}</id_libro>
        </leer_libro>
      </soap:Body>
    </soap:Envelope>
    """
    enviar_peticion(xml)

def actualizar_libro():
    print("\n--- Actualizar Libro ---")
    id_libro = input("ID del libro: ")
    titulo = input("Nuevo título del libro: ")
    autor = input("Nuevo autor del libro: ")
    
    xml = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <actualizar_libro>
          <id_libro>{id_libro}</id_libro>
          <titulo>{titulo}</titulo>
          <autor>{autor}</autor>
        </actualizar_libro>
      </soap:Body>
    </soap:Envelope>
    """
    enviar_peticion(xml)

def eliminar_libro():
    print("\n--- Eliminar Libro ---")
    id_libro = input("ID del libro: ")
    
    xml = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <eliminar_libro>
          <id_libro>{id_libro}</id_libro>
        </eliminar_libro>
      </soap:Body>
    </soap:Envelope>
    """
    enviar_peticion(xml)

def main():
    while True:
        opcion = menu()
        if opcion == "1":
            crear_libro()
        elif opcion == "2":
            leer_libro()
        elif opcion == "3":
            actualizar_libro()
        elif opcion == "4":
            eliminar_libro()
        elif opcion == "5":
            print("Saliendo del cliente SOAP.")
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
