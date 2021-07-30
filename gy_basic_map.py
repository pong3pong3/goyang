import geopandas as gpd
import folium
import pandas as pd
import numpy as np
with open('gy_avg_acq_area.txt','r') as file:
    gy_stat = file.read().split('\n')
gy_stat = pd.DataFrame(list(map(eval, gy_stat)), 
         columns=['district','village','avg_acq_area'])
gy_stat['avg_acq_area'] = gy_stat['avg_acq_area'].apply(lambda x: np.log10(x))

gy_gpkg = gpd.read_file('gy_jurisdiction.gpkg')
gy_gpkg = gy_gpkg.merge(gy_stat, 'left', left_on = 'EMD_NM', right_on  = 'village')

gy_gpkg.loc[pd.isna(gy_gpkg['village']),'district'] = ['일산서구']+\
        ['덕양구']*4
gy_gpkg = gy_gpkg.drop(columns = ['village','avg_acq_area'])
gy_district = gy_gpkg.dissolve('district').drop(columns=['EMD_CD','EMD_NM'])

gy_tidy = pd.read_csv('gy_tidy.csv')
gy_time = gy_tidy.groupby(['구','연도']).count()
gy_time['district'] = list(zip(*gy_time.index))[0]
gy_time = gy_time[['면적','district']]
gy_district = gy_district.merge(gy_time.iloc[::2], 'left', on='district')
gy_district.columns = list(gy_district.columns[:-1])+['2019']
gy_district = gy_district.merge(gy_time.iloc[1::2], 'left', on='district')
gy_district.columns = list(gy_district.columns[:-1])+['2020']
gy_district['centroid']=gy_district['geometry'].centroid

gy_json = gy_gpkg.to_json()
#gy_json = eval(gy_json)
gy_centre = gy_gpkg.to_crs('epsg:5186').dissolve()\
        .geometry.buffer(.1).centroid.to_crs('epsg:4326')
gy_map = folium.Map(location = [gy_centre.y[0], gy_centre.x[0]],
        zoom_start = 11, tiles = 'Stamen Terrain')
folium.TileLayer(tiles = 'OpenStreetMap').add_to(gy_map)
folium.Choropleth(geo_data = gy_json,
        data = gy_stat,
        columns = ['village','avg_acq_area'],
        key_on = 'properties.EMD_NM',
        fill_color = 'YlGn', 
        name = 'average area of acquisition by foreigner (m2)',
        legend_name = 'log (average area of acquisition)',
        show = False,
        ).add_to(gy_map)

style_func = lambda x: {'color':'black',
        'fillOpacity':0}
folium.GeoJson(gy_json,
        style_function = style_func,
        name = 'jurisdiction',
        tooltip = folium.features.GeoJsonTooltip(
            fields=('EMD_NM',),
            aliases=('Name',)),
            ).add_to(gy_map)

for i in gy_district.index:
    lat = gy_district.loc[i, 'centroid'].y
    lon = gy_district.loc[i, 'centroid'].x
    count = gy_district.loc[i, '2020'] - gy_district.loc[i, '2019']
    if count > 0:
        color = 'red'
    else: 
        color = 'blue'
    folium.CircleMarker([lat,lon],
            fill_color = color,
            radius = abs(float(count)),
            weight = 0).add_to(gy_map)

folium.LayerControl(position = 'bottomleft').add_to(gy_map)
gy_map.save('index.html')

