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
from datetime import datetime, timedelta
from src.processing_data import Observacao
import time



class RioMap(Observacao):

  # Class constructor
  def __init__(self, data_inicio="", data_fim="", hora_inicio="", hora_fim="", data_path="./src/static/data/satelite_data") -> None:
    super().__init__(data_inicio, data_fim, hora_inicio, hora_fim)
    self.map_visualization = self.generate_rio_map(
      data_path,
      start_date="08/04/2019",
      end_date="08/04/2019",
      st_hour="18:00",
      ed_hour = "18:30")
      
  
  # Reading and transforming Alerta Rio data
  def generate_rio_map(self, data_path, start_date, end_date, st_hour, ed_hour):
    print(data_path, start_date, end_date, st_hour, ed_hour)
    # Converting from string to datetime
    #st_date = isoparse(start_date)
    #ed_date = isoparse(end_date)

    # Generating rio map without data
    (rio_map, grid_cells) = self._generate_base_map()

    try:
      rio_map = self._generate_map_with_pluviometric(rio_map, grid_cells)
      return self._generate_map_with_real_data(data_path, start_date, end_date, st_hour, ed_hour, rio_map)
    
    except Exception as e:
      print(e)
      print("Exception while getting data, changing the date might solve.")
      print("Getting mocked data instead.")

      return True

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

  def _generate_map_with_real_data(self, data_path, st_date, ed_date, st_hour, ed_hour, rio_map: folium.Map):

    # Getting real data for generating map
    df_estacoes = self._get_data(data_path, st_date, ed_date, st_hour, ed_hour)
   
    i_data = st_date + " " + st_hour + ":00"
    st_date = datetime.strptime(i_data, "%d/%m/%Y %H:%M:%S")

    event_coordinates = []
    coord_list = []
    file_count = 1
    for datetime_index in df_estacoes.keys():
     
      dataframe = df_estacoes[datetime_index]
      # datetime_i = datetime_index

      # while datetime_i < (datetime_index + timedelta(0, 20)):
        # print(dataframe['event_time_offset'])
        # print(datetime_i)
      event_lat = dataframe.loc[:, 'event_lat'].to_list()
      event_lon = dataframe.loc[:, 'event_lon'].to_list()
    
      while (len(event_lat) + len(event_lon)) > 0:
      
        lat = event_lat.pop()
        lon = event_lon.pop()

        coord_list.append([lat, lon])

      if file_count == 45:
        event_coordinates.append(coord_list)
        coord_list = []
        file_count = 1
      else:
        file_count += 1
      # datetime_i = datetime_i + timedelta(0, 1)
    #event_coordinates = [[[-23.0395461 , -43.66783523], [-23.13337764, -43.79131174], [-22.86242478, -43.74579799]], 
    #[[-23.08989626, -43.44800784], [-22.92912784, -43.62462281], [-23.04879054, -43.55850286]], 
    #[[-23.16814332, -43.5245129], [-22.8843296 , -43.48284038], [-22.97770164, -43.5040954]]]
    time_index = [(st_date + k * timedelta(0, 0, 0, 0, 15)).strftime("%d-%m-%Y, %H:%M:%S") for k in range(len(event_coordinates))]
    hm = plugins.HeatMapWithTime(event_coordinates, index=time_index, auto_play=True, max_opacity=0.6)
    hm.add_to(rio_map)
    return rio_map
  
  # Used to generate data for main view
  def _get_data(self, data_path, st_date, ed_date, st_hour, ed_hour) -> dict[datetime, pd.DataFrame]:
    DATA_DIR = "./src/static/data/satelite_data"

    i_data = st_date + " " + st_hour + ":00"
    e_data = ed_date + " " + ed_hour + ":00"
    id = time.mktime(datetime.strptime(i_data, "%d/%m/%Y %H:%M:%S").timetuple())
    ed = time.mktime(datetime.strptime(e_data, "%d/%m/%Y %H:%M:%S").timetuple())
    id2 = datetime.strptime(i_data, "%d/%m/%Y %H:%M:%S")
    # Each file records 20 seconds of obeservation
    seconds_dif = ed-id
    total_files = int(seconds_dif/20)

    #if (seconds_dif / 900) < 1:
      # To take at least 15 minutes of prediction
      #total_files = 45
    #else:
    #  total_files = math.ceil(seconds_dif / 900) * 45
    
    # total_files = math.ceil(seconds_dif / 20)
    hourC = st_hour
    st_year = st_date[6:10]
    st_day = st_date[0:2]
    st_month = st_date[3:5]
    st_hour = st_hour[0:2]
    st_minutes = hourC[3:5]
    st_seconds = "00"

    day_of_year = datetime(int(st_year),int(st_month),int(st_day)).timetuple().tm_yday 
    #day_of_year = str(day_of_year)
    #print("hora:", st_hour)
    #print("horas:", day_of_year, st_year, st_day, st_month, st_hour, st_minutes)

    # Calculating the number of the file to start getting data
    begin_file_number = round((int(st_minutes) * 60) / 20) + 1

    # Adding 0 for the pattern '001', '002'...
    if day_of_year < 10:
      day_of_year = f"00{day_of_year}"
    elif day_of_year >= 10 and day_of_year <= 99:
      day_of_year = f"0{day_of_year}"
    
    #if st_hour < 10:
    #    st_hour = f"0{st_hour}"

    file_path = f"{DATA_DIR}/{st_year}/{day_of_year}/{st_hour}"
    #print("filepath:",file_path)
    dic_date = id2
    dataframe_dic = dict()
    total_count, count = (1,1)
    for file in os.listdir(file_path):
      
      if total_count < begin_file_number:
        total_count += 1
        continue
      
      ds = xr.open_dataset(f"{file_path}/{file}",engine="netcdf4")

      try:
        ds = self._filter_coordinates(ds)
        #print("abriu o dataset")
      except ValueError:
        print('ValueError')

      df = ds.to_dataframe()
      ds.close()
      dataframe_dic[dic_date] = df

      if count == total_files:
        break
      else:
        count += 1
        dic_date = dic_date + timedelta(0, 20)
        #print("passou")
    
    return dataframe_dic

  def _generate_map_with_pluviometric(self, rio_map, grid_cells):

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
        i+=1

    return rio_map

  def _filter_coordinates(self, ds: xr.Dataset):
    return ds['event_energy'].where(
        (ds['event_lat'] >= -24.0) & (ds['event_lat'] <= -22.5) & 
        (ds['event_lon'] >= -43.8) & (ds['event_lon'] <= -43.0),
         drop=True)

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