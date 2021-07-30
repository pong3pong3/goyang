import geopandas as gpd
import pandas as pd
import numpy as np
gy_gpkg = gpd.read_file('gy_jurisdiction.gpkg')
def districts(emd_cd):
    if emd_cd[4]=='7':
        return '일산서구'
    elif emd_cd[4]=='1':
        return '덕양구'
    return '일산동구'
gy_gpkg['district'] = gy_gpkg['EMD_CD'].apply(districts)
def centers(df):
    coords = df.to_crs('epsg:5186').centroid.to_crs('epsg:4326')
    return (coords.x, coords.y)
gy_district = gy_gpkg.dissolve('district').drop(columns = ['EMD_CD','EMD_NM'])
gy_gpkg['centerlon'],gy_gpkg['centerlat'] = centers(gy_gpkg)
gy_district['centerlon'],gy_district['centerlat'] = centers(gy_district)

gy_tidy = pd.read_csv('gy_tidy.csv')
gy_dcmps = gy_tidy.groupby(['동','연도'])['국적'].value_counts()
us_cn = filter(lambda x: x[-1] in ('미국','중국'), gy_dcmps.index)
gy_us_cn = gy_dcmps[us_cn]
others = filter(lambda x: x[-1] not in ('미국','중국'), gy_dcmps.index)
gy_others = gy_dcmps[others].groupby(['동','연도']).sum()
gy_nation = pd.concat([gy_us_cn,gy_others])

def nations(gy_gpkg, year, nation):
    if nation==None:
        gy_select = gy_nation[filter(lambda x: x[-1]==year,
                    gy_nation.index)]
        nation = '기타'
    else:
        gy_select = gy_nation[filter(lambda x: x[1]==year and x[-1]==nation,
                    gy_nation.index)]
    gy_select = pd.DataFrame(gy_select)
    gy_select['EMD_NM'] = list(zip(*gy_select.index))[0]
    gy_gpkg = gy_gpkg.merge(gy_select, 'left', 'EMD_NM') 
    gy_gpkg.columns = list(gy_gpkg.columns[:-1]) + [str(year)+nation]
    return gy_gpkg
for i in (19,20):
    for j in ('미국','중국',None):
        gy_gpkg = nations(gy_gpkg,i,j)
gy_gpkg = gy_gpkg.fillna(0)
gy_gpkg.to_file('gy_us_cn.gpkg', driver='GPKG', encoding='utf-8',
        layer='village')
gy_district = pd.concat([gy_district, gy_gpkg.groupby('district').sum()],
        axis=1)
gy_district.to_file('gy_us_cn.gpkg', driver='GPKG', encoding='utf-8',
        layer='district')
