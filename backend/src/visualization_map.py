import warnings
import webbrowser
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
from shapely.geometry import Polygon
from pathlib import Path
import matplotlib.pyplot as plt
import wradlib as wrl
import numpy as np
from datetime import datetime, timedelta

# Reading and transforming Alerta Rio data
df_estacoes = pd.read_csv('./src/static/estacoes_pluviometricas.csv')
df_estacoes = df_estacoes.drop(columns=['Unnamed: 0'])

rio_map = folium.Map([-22.925778948753702, -43.489029909370046], zoom_start=10, tiles='cartodbpositron')
colormap = ['magenta', 'red', 'orange', 'yellow']
folium.LatLngPopup().add_to(rio_map)

import warnings
warnings.filterwarnings('ignore')

lat_list = [-23.1339033365138, 
             -23.0647349667651, 
             -22.9955665970164, 
             -22.9263982272677, 
             -22.857229857519, 
             -22.7880614877703, 
             -22.7188931180216, -22.649724748272934]
lon_list = [-43.8906028271505, 
              -43.7697438637654, 
              -43.6488849003802,
              -43.5280259369951, 
              -43.4071669736099,
              -43.2863080102248,
              -43.1654490468397, -43.04835145732227]
              
grid_cells = {}

cell_idx = 1
for j, _ in enumerate(lon_list):
  if j + 1 == len(lon_list):
    break
  for i, _ in enumerate(lat_list):
    if i + 1 == len(lat_list):
      break

    lon_ul, lat_ul = lon_list[j], lat_list[i]
    lon_ur, lat_ur = lon_list[j+1], lat_list[i]
    lon_lr, lat_lr = lon_list[j+1], lat_list[i+1]
    lon_ll, lat_ll = lon_list[j], lat_list[i+1]
    ul = (lon_ul, lat_ul)
    ur = (lon_ur, lat_ur)
    lr = (lon_lr, lat_lr)
    ll = (lon_ll, lat_ll)

    polygon_geom = Polygon([ul, ur, lr, ll])
    grid_cells[cell_idx] = polygon_geom
    cell_idx += 1

    crs = {'init': 'epsg:4326'}
    polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])    
    folium.GeoJson(polygon).add_to(rio_map)

assert(49==len(grid_cells))

lat = list(df_estacoes.Latitude)
lon = list(df_estacoes.Longitude)
bairro = list(df_estacoes.Estação)
i=0

for loc in zip(lat, lon):
    folium.Circle(
        location=loc,
        radius=10,
        fill=True,
        tooltip=bairro[i],
        color='red',
        fill_opacity=0.7
    ).add_to(rio_map)


np.random.seed(3141592)
initial_data = np.random.normal(size=(100, 2)) * np.array([[0.1, 0.11]]) + np.array([[-22.99, -43.59]])
move_data = np.random.normal(size=(100, 2)) * 0.01
data = [(initial_data + move_data * i).tolist() for i in range(100)]

time_ = 0
N = len(data)
itensify_factor = 30
for time_entry in data:
    time_ = time_+1
    for row in time_entry:
        weight = min(np.random.uniform()*(time_/(N))*itensify_factor, 1)
        row.append(weight)

time_index = [(datetime.now() + k * timedelta(1)).strftime("%d-%m-%Y") for k in range(len(data))]

hm = plugins.HeatMapWithTime(data, index=time_index, auto_play=True, max_opacity=0.6)
hm.add_to(rio_map)

rio_map.save('map.html')
webbrowser.open('map.html')