import geopandas as gpd
gg=gpd.read_file('../eupmyeondong/LSMD_ADM_SECT_UMD_41.shp',encoding='cp949')\
    .to_crs('epsg:4326')
gg[gg['EMD_CD'].str.startswith('4128')]\
    [['EMD_CD','EMD_NM','geometry']]\
    .to_file('gy_jurisdiction.gpkg',encoding='utf-8',driver='GPKG')
