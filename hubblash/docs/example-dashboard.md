---
theme: dashboard
title: Description de mon Territoire
toc: false
---

# Description de mon Territoire

<!-- Load and transform the data -->

<div class="grid grid-cols-4">
  <div class="card">
    <h2>Ménages</h2>
    <span class="big">${hubblo[0].Men}</span>
  </div>
  <div class="card">
    <h2>Individus</h2>
    <span class="big">${hubblo[0].Ind}</span>
  </div>
    <div class="card">
    <h2>Taille des Ménages</h2>
    <span class="big">${Math.round(hubblo[0].Ind/hubblo[0].Men * 100) / 100}</span>
  </div>
     <div class="card">
    <h2>% des Ménages pauvres</h2>
    <span class="big">${Math.round(hubblo[0].Men_pauv/hubblo[0].Men * 100) }</span>
  </div>
</div>



<div class="grid grid-cols-2" style="grid-auto-rows: 30fr;">
  <div class="card" id="map" style='height: 300px'  >
  </div>
  <div class="card" style="padding: 0;">
    ${Inputs.table(hubblo)}
  </div>
</div>



```js
var db = DuckDBClient.of()
```


```js

  const map = L.map("map").setView([43.596, 1.4419], 10);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: '© OpenStreetMap' }).addTo(map);
 
```



```js
import * as L from "npm:leaflet";
```


```js
var x = 574153.0242929291
var y = 6278679.902778912
var rayon=1000 
```






















```js
var hubblo = db.sql`select sum(Ind) as Ind,
        sum(Men_1ind) as Men_1ind, 
        sum(Men_5ind) as Men_5ind, 
        sum(Men_prop) as Men_prop, 
        sum(Men_fmp) as Men_fmp,
        sum(Ind_snv) as Ind_snv, 
        sum(Men_surf) as Men_surf, 
        sum(Men_coll) as Men_coll, 
        sum(Men_mais) as Men_mais, 
        sum(Log_av45) as Log_av45, 
        sum(Log_45_70) as Log_45_70,
        sum(Log_70_90) as Log_70_90, 
        sum(Log_ap90) as Log_ap90, 
        sum(Log_inc) as Log_inc, 
        sum(Log_soc) as Log_soc, 
        sum(Ind_0_3) as Ind_0_3, 
        sum(Ind_4_5) as Ind_4_5,
        sum(Ind_6_10) as Ind_6_10, 
        sum(Ind_11_17) as Ind_11_17, 
        sum(Ind_18_24) as Ind_18_24, 
        sum(Ind_25_39) as Ind_25_39, 
        sum(Ind_40_54) as Ind_40_54,
        sum(Ind_55_64) as Ind_55_64, 
        sum(Ind_65_79) as Ind_65_79, 
        sum(Ind_80p) as Ind_80p, 
        sum(Ind_inc) as Ind_inc,  
        sum(Men_pauv) as Men_pauv,
        sum(Men) as Men 


from 
read_parquet("https://minio.lab.sspcloud.fr/h529p3/data/Filosofi2017_carreaux_200m_met.parquet") 
where (x>${x}-${rayon})
and (x<${x}+${rayon})
and (y>(${y}-${rayon})) 
and (y<${y}+${rayon});`
```





