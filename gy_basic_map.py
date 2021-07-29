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
gy_json = gy_gpkg.to_json()
gy_json = eval(gy_json)
gy_gpkg = gy_gpkg.to_crs('epsg:5186').dissolve()\
        .geometry.buffer(.1).centroid.to_crs('epsg:4326')
gy_map = folium.Map(location = [gy_gpkg.y[0], gy_gpkg.x[0]],
        zoom_start = 11, tiles = 'Stamen Terrain')
folium.Choropleth(geo_data = gy_json,
        data = gy_stat,
        columns = ['village','avg_acq_area'],
        key_on = 'properties.EMD_NM',
        fill_color = 'YlGn', 
        legend_name = 'log (average area of acquisition)',
        ).add_to(gy_map)
style_func = lambda x: {'color':None,
        'fillOpacity':0}
folium.GeoJson(gy_json,
        style_function = style_func,
        tooltip = folium.features.GeoJsonTooltip(
            fields=('EMD_NM',),
            aliases=('Name',)),
            ).add_to(gy_map)
gy_map.save('index.html')
