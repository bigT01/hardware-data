import json
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from collections import Counter


with open("./tematiche_sedi.json", "r") as f:
    data = json.load(f)

nodes = data['nodi']

# Collect livello1 data
liv1_counts = Counter()
# Collect livello2 data
liv2_counts = Counter()

for node in nodes:
    for l1 in node.get('livello1', []):
        liv1_counts[l1] += 1
    for l2 in node.get('livello2', []):
        liv2_counts[l2] += 1


def geocode_city(city_name, access_token):
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    response = requests.get(f"{base_url}/{city_name}.json?access_token={access_token}")
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            longitude, latitude = data['features'][0]['center']
            return latitude, longitude
    return None, None

access_token = '#'

st.title("Geographical Distribution of Topics")

m = folium.Map(location=[41.8719, 12.5674], zoom_start=6)

for node in data['nodi']:
    city = node['nodo']
    livello1 = ", ".join(node.get('livello1', []))
    livello2 = ", ".join(node.get('livello2', []))
    latitude, longitude = geocode_city(city, access_token)
    if latitude and longitude:
        folium.Marker(
            location=[latitude, longitude],
            popup=f"{city}\nLivello1: {livello1}\nLivello2: {livello2}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

st_folium(m, width=700, height=500)

fig1, ax1 = plt.subplots()
ax1.bar(liv1_counts.keys(), liv1_counts.values())
ax1.set_title("Distribuzione delle macro-categorie (livello1)")

plt.xticks(rotation=90)

st.pyplot(fig1)