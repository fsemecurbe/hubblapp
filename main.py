from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

import pandas as pd
import geopandas as gpd
import duckdb 

app = FastAPI()
duckdb.sql('LOAD httpfs ;INSTALL spatial; LOAD spatial;')
url = "http://minio.lab.sspcloud.fr/h529p3/data/Filosofi2017_carreaux_200m_met.parquet"

duckdb.sql(f'''
  CREATE OR REPLACE VIEW carreaux
  AS SELECT * FROM read_parquet("{url}") 
'''
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def read_item(latitude: str="48.853", longitude: str="2.35", rayon: str=1000):
    coordonnees_ctr_hubblo = duckdb.sql(
        f''' 
        select st_x(geo) as x, st_y(geo) as y from
        (select ST_Transform(ST_Point({latitude} , {longitude}),'EPSG:4326', 'EPSG:2154') as geo) ''').df()
    x_hubblo = coordonnees_ctr_hubblo.x[0]
    y_hubblo = coordonnees_ctr_hubblo.y[0]

    res = duckdb.sql(
        f'''
        select sum(Ind*coeff) as Ind,
        sum(Men_1ind*coeff) as Men_1ind, 
        sum(Men_5ind*coeff) as Men_5ind, 
        sum(Men_prop*coeff) as Men_prop, 
        sum(Men_fmp*coeff) as Men_fmp,
        sum(Ind_snv*coeff) as Ind_snv, 
        sum(Men_surf*coeff) as Men_surf, 
        sum(Men_coll*coeff) as Men_coll, 
        sum(Men_mais*coeff) as Men_mais, 
        sum(Log_av45*coeff) as Log_av45, 
        sum(Log_45_70*coeff) as Log_45_70,
        sum(Log_70_90*coeff) as Log_70_90, 
        sum(Log_ap90*coeff) as Log_ap90, 
        sum(Log_inc*coeff) as Log_inc, 
        sum(Log_soc*coeff) as Log_soc, 
        sum(Ind_0_3*coeff) as Ind_0_3, 
        sum(Ind_4_5*coeff) as Ind_4_5,
        sum(Ind_6_10*coeff) as Ind_6_10, 
        sum(Ind_11_17*coeff) as Ind_11_17, 
        sum(Ind_18_24*coeff) as Ind_18_24, 
        sum(Ind_25_39*coeff) as Ind_25_39, 
        sum(Ind_40_54*coeff) as Ind_40_54,
        sum(Ind_55_64*coeff) as Ind_55_64, 
        sum(Ind_65_79*coeff) as Ind_65_79, 
        sum(Ind_80p*coeff) as Ind_80p, 
        sum(Ind_inc*coeff) as Ind_inc,  
        sum(Men_pauv*coeff) as Men_pauv,
        sum(Men*coeff) as Men 
      
        from 
        (
            select *, st_area(st_intersection(ST_GEOMFROMWKB(geometry), 
            (SELECT ST_BUFFER(ST_POINT({x_hubblo},{y_hubblo}),{rayon}))))/st_area(ST_GEOMFROMWKB(geometry)) as coeff  
            from  
            (select * from carreaux
            where carreaux.x > ({x_hubblo}-{rayon}-200) and
            carreaux.x < ({x_hubblo}+{rayon}+200) and
            carreaux.y > ({y_hubblo}-{rayon}-200) and
            carreaux.y < ({y_hubblo}+{rayon}+200)) as temp
            where st_intersects(ST_GEOMFROMWKB(temp.geometry),(SELECT ST_BUFFER(ST_POINT({x_hubblo},{y_hubblo}),{rayon}))))
        ''').df().to_json()

    return(res)
