from bs4 import BeautifulSoup
import requests
import os
import urllib3
import json

# Deshabilitar las advertencias de solicitud HTTPS no verificada
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL de la página a raspar
url = 'https://www.hacktonic.net:23666/'

try:
    # Realizar la solicitud HTTP con verificación de certificado SSL
    response = requests.get(url, verify=False)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Crear el objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los enlaces (<a> tags)
        links = soup.find_all('a')

        # Nombre del archivo que deseas buscar
        file_to_find = 'https://urllib3.readthedocs.io/en/latest/_static/dark-logo.svg'

        # Iterar sobre los enlaces para encontrar el enlace al archivo deseado
        for link in links:
            href = link.get('href')
            # Verificar si el enlace contiene el nombre del archivo deseado
            if file_to_find in href:
                # Construir la URL completa del archivo
                file_url = url + href
                # Realizar la solicitud HTTP para descargar el archivo
                file_response = requests.get(file_url, verify=False)
                # Verificar si la solicitud fue exitosa
                if file_response.status_code == 200:
                    # Especificar la ruta donde guardar el archivo descargado
                    save_path = os.path.join(os.path.expanduser("~"), "Desktop", file_to_find)
                    # Escribir el contenido del archivo en el disco
                    with open(save_path, 'wb') as f:
                        f.write(file_response.content)
                    print(f"Archivo '{file_to_find}' descargado con éxito en el escritorio.")
                    break  # Terminar el bucle una vez que se haya encontrado y descargado el archivo
        else:
            print(f"No se encontró el archivo '{file_to_find}'.")
    else:
        print('La solicitud HTTP no fue exitosa. Código de estado:', response.status_code)

except requests.exceptions.SSLError as e:
    print("Error de SSL:", e)
