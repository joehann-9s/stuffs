import requests
from bs4 import BeautifulSoup
import json

def obtener_contenido_pagina(url):
    response = requests.get(url)
    response.raise_for_status()  # Lanza una excepción si hay un error al hacer la solicitud
    return response.content

def obtener_enlaces_y_contenido(html):
    soup = BeautifulSoup(html, 'html.parser')
    enlaces = []

    # Busca el elemento con el ID 'search_resultsRows' y extrae todas las etiquetas <a> dentro de él
    resultados = soup.find(id='search_resultsRows')
    if resultados:
        enlaces = resultados.find_all('a')

    # Extrae el contenido de cada enlace y lo guarda en una lista de diccionarios
    contenido_enlaces = []
    for enlace in enlaces:
        contenido_enlaces.append({'texto': enlace.get_text().strip(), 'enlace': enlace.get('href')})

    return contenido_enlaces

if __name__ == "__main__":
    url = 'https://store.steampowered.com/search/?specials=1'
    html = obtener_contenido_pagina(url)

    # Obtiene los enlaces y su contenido
    contenido_enlaces = obtener_enlaces_y_contenido(html)

    # Guarda la información en un archivo JSON
    with open('contenido_pagina_steam.json', 'w') as archivo:
        json.dump(contenido_enlaces, archivo, indent=4)

    print("El contenido de la página de Steam ha sido guardado en 'contenido_pagina_steam.json'")
