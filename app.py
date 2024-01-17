import re
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import folium
import requests

def obter_correspondencias(url, padrao):
    response = requests.get(url)
    if response.status_code == 200:
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        resultado = soup.get_text()
        correspondencias = [correspondencia for correspondencia in padrao.findall(resultado)]
        return correspondencias
    else:
        print(f"Falha ao obter correspondências para {url}")
        return []

def obter_lat_long_por_nome_cidade(nome_local, cidade, estado):
    endereco = f"{nome_local}, {cidade}, {estado}"
    api_key = "AIzaSyDvBbVgBsUxNaGO6qBmG5zvc1sOea0soS0" 
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "results" in data and data["results"]:
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        print(f"Coordenadas não encontradas para {nome_local}")
        return None

def criar_mapa(coordenadas_escolas):
    mapa = folium.Map(location=[-3.7327, -38.5277], zoom_start=12)
    folium.TileLayer(
        tiles='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name="OpenStreetMap.Mapnik"
    ).add_to(mapa)
    folium.LayerControl().add_to(mapa)

    for escola, lat, lon in coordenadas_escolas:
        folium.Marker([lat, lon], popup=escola).add_to(mapa)

    return mapa

def main():
    sefor01 = 'https://drive.google.com/drive/folders/19zivhrk7UCqy-WbA6oLbKAKIpBa2Mr_xS2LwcI6j_zcbp110jJRFM1MCNMIyyMEdH2mNj_0x?usp=sharing'
    sefor02 = 'https://drive.google.com/drive/folders/1mOi949Y_UeOpVQUkDClSCOA2-bHKaLiQn32cAl0ux2GsKG6gboTq0K3XuaJOO8CYIpagZTjH?usp=sharing'
    sefor03 = 'https://drive.google.com/drive/folders/1X5ij7FXCY0HPIjqgyL0jjY5gz-Dydk4INHIamLxw7ZZa84GzhMNlzvJyq5G0r_O20tmzlYd_?usp=sharing'

    padrao1 = re.compile(r"SEFOR 01_[^_]+")
    padrao2 = re.compile(r"SEFOR 2[^_]+")
    padrao3 = re.compile(r"SEFOR 03_[^_]+")

    lista_escolas_01 = obter_correspondencias(sefor01, padrao1)
    lista_escolas_02 = obter_correspondencias(sefor02, padrao2)
    lista_escolas_03 = obter_correspondencias(sefor03, padrao3)

    lista_escolas = lista_escolas_01 + lista_escolas_02 + lista_escolas_03

    cidade = "Fortaleza"
    estado = "Ceará"

    coordenadas_escolas = []

    for escola in lista_escolas:
        coordenadas = obter_lat_long_por_nome_cidade(escola, cidade, estado)
        if coordenadas:
            coordenadas_escolas.append((escola, coordenadas[0], coordenadas[1]))

    for escola, latitude, longitude in coordenadas_escolas:
        print(f"{escola}: Latitude {latitude}, Longitude {longitude}")

    mapa = criar_mapa(coordenadas_escolas)
    mapa.save("mapa_escolas_sefor.html")

if __name__ == "__main__":
    main()
