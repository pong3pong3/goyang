import geopandas as gpd
import pandas as pd
import numpy as np
import folium
gy = gpd.read_file('gy_us_cn.gpkg',layer='village')
def china_vs_us(df, year):
    year = str(year)
    denominator = df[year+'중국']+df[year+'미국']
    if denominator==0: 
        return np.nan
    else:
        return df[year+'중국']/denominator*100
gy['19uscn'] = gy.apply(lambda x: china_vs_us(x,19), axis=1)
gy['20uscn'] = gy.apply(lambda x: china_vs_us(x,20), axis=1)
def others(df):
    denominator = df.sum()
    if denominator == 0:
        return np.nan
    else:
        return df[['19기타','20기타']].sum()/denominator
gy['other'] = gy.loc[:,gy.columns.str.contains('(19|20)[가-힣]')]\
        .apply(others,axis=1)
gy['total'] = gy.loc[:,gy.columns.str.contains('(19|20)[가-힣]')]\
        .sum(axis=1)
gy_json = gy.to_json()

gy_map = folium.Map(location = [37.65, 126.8],
        zoom_start = 11, tiles = 'Stamen Terrain')
folium.TileLayer(tiles = 'OpenStreetMap').add_to(gy_map)
folium.Choropleth(geo_data = gy_json,
        data = gy,
        columns = ['EMD_NM','19uscn'],
        key_on = 'properties.EMD_NM',
        fill_color = 'RdBu_r',
        nan_fill_opacity = 0,
        name = '2019 미국인vs중국인 취득건수',
        legend_name = 'China / (US+China) (%)',
        ).add_to(gy_map)

duplicate = folium.Choropleth(geo_data = gy_json,
                  data = gy,
                  columns = ['EMD_NM','20uscn'],
                  key_on = 'properties.EMD_NM',
                  fill_color = 'RdBu_r',
                  nan_fill_opacity = 0,
                  name = '2020 미국인vs중국인 취득건수',
                  show = False
                  )
def remove_legend(choropleth):
    death_note = []
    for child in choropleth._children:
        if child.startswith('color_map'):
            death_note.append(child)
    for element in death_note:
        choropleth._children.pop(element)
    return choropleth
remove_legend(duplicate).add_to(gy_map)

layer = folium.FeatureGroup(name = '취득건수(2019~2020)')
for i in range(len(gy)):
    total = gy.loc[i,'total']
    if total == 0:
        continue
    folium.CircleMarker(
            [gy.loc[i,'centerlat'],gy.loc[i,'centerlon']],
            radius = total/10, fill_opacity = 1,
            weight = 0, fill_color = 'black',
            popup = folium.Popup('총 취득수: '+str(total)[:-2],
                min_width=100, max_width=100),
            ).add_to(layer)

folium.GeoJson(gy_json,
        style_function = lambda x: {'weight':1,'color':'black',
            'fillColor':'black','fillOpacity': 
            x['properties']['other']/2 if x['properties']['total']!=0
            else 0},
        name = '기타국가의 비중(탁도)',
        tooltip = folium.GeoJsonTooltip(
            fields=('EMD_NM',),
            aliases=('이름:',),
            ),
        ).add_to(gy_map)

layer.add_to(gy_map)
folium.LayerControl(position = 'bottomleft', collapsed = False).add_to(gy_map)
gy_map.save('index.html')
