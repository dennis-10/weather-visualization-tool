import math
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
from shapely.geometry import Polygon
from dateutil.parser import isoparse
import xarray as xr
import os
import numpy as np
from datetime import datetime, timedelta

class RioMap():

  # Class constructor
  def __init__(self, data_path="./src/static/satelite_data") -> None:
    self.map_visualization = self.generate_rio_map(
      data_path,
      start_date="2022-01-01 00:00:00",
      end_date="2022-01-01 00:00:20")
  
  # Reading and transforming Alerta Rio data
  def generate_rio_map(self, data_path, start_date, end_date):
    
    # Converting from string to datetime
    st_date = isoparse(start_date)
    ed_date = isoparse(end_date)
    
    # Generating rio map without data
    (rio_map, grid_cells) = self._generate_base_map()

    try:
      return self._generate_map_with_real_data(data_path, st_date, ed_date, rio_map)
      
    except Exception as e:
      print(e)
      print("Exception while getting data, changing the date might solve.")
      print("Getting mocked data instead.")

      return self._generate_map_with_mock(rio_map, grid_cells)
          

  def _generate_base_map(self):
    rio_map = folium.Map([-22.925778948753702, -43.489029909370046], zoom_start=10, tiles='cartodbpositron')
    folium.LatLngPopup().add_to(rio_map)

    import warnings
    warnings.filterwarnings('ignore')

    lat_list = [-23.1339033365138, 
                -23.0647349667651, 
                -22.9955665970164, 
                -22.9263982272677, 
                -22.857229857519, 
                -22.7880614877703, 
                -22.7188931180216, 
                -22.649724748272934]

    lon_list = [-43.8906028271505, 
                -43.7697438637654, 
                -43.6488849003802,
                -43.5280259369951, 
                -43.4071669736099,
                -43.2863080102248,
                -43.1654490468397, 
                -43.04835145732227]
                  
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

    return (rio_map, grid_cells)
  
  # Used to generate data for main view
  def _get_data(self, data_path : str, st_date : datetime, ed_date : datetime) -> dict[datetime, pd.DataFrame]:
    DATA_DIR = data_path

    # Each file records 20 seconds of obeservation
    seconds_dif = (ed_date - st_date).total_seconds()
    total_files = math.ceil(seconds_dif / 20)
    
    st_year = st_date.year
    st_day = st_date.day
    st_hour = st_date.hour
    st_minutes = st_date.minute
    st_seconds = st_date.second

    # Calculating the number of the file to start getting data
    begin_file_number = round(((st_minutes * 60) + st_seconds) / 20) + 1

    # Adding 0 for the pattern '001', '002'...
    if st_day < 10:
      st_day = f"00{st_day}"
    elif st_day >= 10 and st_day <= 99:
      st_day = f"0{st_day}"
    
    if st_hour < 10:
        st_hour = f"0{st_hour}"

    file_path = f"{DATA_DIR}/{st_year}/{st_day}/{st_hour}"
    
    dic_date = st_date
    dataframe_dic = dict()
    total_count, count = (1,1)
    for file in os.listdir(file_path):

      if total_count < begin_file_number:
        total_count += 1
        continue
      
      ds = xr.open_dataset(f"{file_path}/{file}")

      try:
        ds = self._filter_coordinates(ds)
      except ValueError:
        print('ValueError')

      df = ds.to_dataframe()
      dataframe_dic[dic_date] = df

      if count == total_files:
        break
      else:
        count += 1
        dic_date = dic_date + timedelta(0, 20)
  
    return dataframe_dic
  

  def _generate_map_with_real_data(self, data_path: str, st_date: datetime, ed_date: datetime, rio_map: folium.Map):

    # Getting real data for generating map
    df_estacoes = self._get_data(data_path, st_date, ed_date)

    event_coordinates = []
    for datetime_index in df_estacoes.keys():

      dataframe = df_estacoes[datetime_index]
      datetime_index = datetime_index + timedelta(0, 40, 0, 0, 3)
      datetime_i = datetime_index
      coord_list = []
      while datetime_i < (datetime_index + timedelta(0, 20)):
        
        event_lat = dataframe.loc[(dataframe['event_time_offset'] >= datetime_i) & (dataframe['event_time_offset'] < (datetime_i + timedelta(0, 1))), 'event_lat'].to_list()
        event_lon = dataframe.loc[(dataframe['event_time_offset'] >= datetime_i) & (dataframe['event_time_offset'] < (datetime_i + timedelta(0, 1))), 'event_lon'].to_list()
      
        while (len(event_lat) + len(event_lon)) > 0:
        
          lat = event_lat.pop()          
          lon = event_lon.pop() 

          coord_list.append([lat, lon])

        event_coordinates.append(coord_list)
        coord_list = []
        datetime_i = datetime_i + timedelta(0, 1)
    
    time_index = [(st_date + k * timedelta(0, 1)).strftime("%d-%m-%Y, %H:%M:%S") for k in range(len(event_coordinates))]
    hm = plugins.HeatMapWithTime(event_coordinates, index=time_index, auto_play=True, max_opacity=0.6)
    hm.add_to(rio_map)
    return rio_map
  

  def _generate_map_with_mock(self, rio_map, grid_cells):

    df_estacoes = pd.read_csv(f'./{"src/static/estacoes_pluviometricas.csv"}')
    df_estacoes = df_estacoes.drop(columns=['Unnamed: 0'])

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

    return rio_map


  def _filter_coordinates(self, ds: xr.Dataset):
    return ds['event_energy'].where(
        (ds['event_lat'] >= -24.0) & (ds['event_lat'] <= -22.5) & 
        (ds['event_lon'] >= -43.8) & (ds['event_lon'] <= -43.0))

  def _preparing_data(self, df):
    df.drop(df.columns[4:-1],
                axis=1,
                inplace=True)
    
    df.drop(df.columns[0],
            axis=1,
            inplace=True)

    df.rename(columns={'event_time_offset': 'time',
                    'event_lat': 'lat',
                    'event_lon': 'lon',
                    'event_energy': 'energy'},
            inplace=True)

    df.set_index('time', inplace=True)
    return df