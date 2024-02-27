---
theme: dashboard
title: Mon Hubblo
toc: false
---

### Mon Hubblo


<div class="grid grid-cols-4">
  <div class="card">
    <h2>👪 Ménages</h2>
    <span class="big">${hubblo[0].Men}</span>
  </div>
  <div class="card">
    <h2>🧑 Individus</h2>
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


```js
const rayon_input = Inputs.range([200, 1000], {step: 100});
const rayon = Generators.input(rayon_input); 
```

<div class="grid grid-cols-2">
  <div class="card" >
  <div>${rayon_input} </div>
  <div id="map" style="height: 300px"></div>
  </div> 
  <div class="card" id='barhousehold'>
    
  </div>
</div>



```js
var data = [
  {
    x: ['une personne', 'nombreuses', 'monoparentales', 'en maison', 'propriétaires'],
    y: [hubblo[0].Men_1ind / hubblo[0].Men*100, 
        hubblo[0].Men_5ind / hubblo[0].Men*100,
        hubblo[0].Men_fmp	/ hubblo[0].Men*100,
        hubblo[0].Men_mais / hubblo[0].Men*100,
        hubblo[0].Men_prop	/hubblo[0].Men*100
        ],
    type: 'bar'
  }
];

Plotly.newPlot('barhousehold', data);
```


```js
const map = L.map("map").setView([43.596, 1.4419], 10);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: '© OpenStreetMap' }).addTo(map);
```

```js
const db = DuckDBClient.of({carreaux: FileAttachment("data/Filosofi2017_carreaux_200m_met_Men.parquet")});
```

```js
const coordonnees = Mutable([1.4419,43.596]);
const increment = (store) => coordonnees.value = store;
```


```js
  function onMapClick(e) {
    console.log('test',e.latlng)    
    
    
    increment([e.latlng.lng, e.latlng.lat])
    
    circle.remove()
    
    
    }
  map.on('click', onMapClick);
```

```js
var circle = L.circle([coordonnees[1],coordonnees[0]], {
      color: 'red',
          fillColor: '#f03',
              fillOpacity: 0.5,
                  radius: rayon
                  }).addTo(map);
```


```js
import * as L from "npm:leaflet";
import proj4 from "npm:proj4";
import Plotly from 'npm:plotly.js-dist';
```


```js
var coordinates3035 = proj4('+proj=longlat +datum=WGS84 +no_defs +type=crs',
                        '+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs',coordonnees);
```

```js
var hubblo = db.sql`select 
        sum(Men_1ind) as Men_1ind, 
        sum(Men_5ind) as Men_5ind, 
        sum(Men_prop) as Men_prop, 
        sum(Men_fmp) as Men_fmp,
        sum(Men_surf) as Men_surf, 
        sum(Men_coll) as Men_coll, 
        sum(Men_mais) as Men_mais, 
        sum(Men_pauv) as Men_pauv,
        sum(Men) as Men 
from 
carreaux
where ((x*100+3210500)>${coordinates3035[0]}-${rayon})
and ((x*100+3210500)<${coordinates3035[0]}+${rayon})
and ((y*100+2029900)>(${coordinates3035[1]}-${rayon})) 
and ((y*100+2029900)<${coordinates3035[1]}+${rayon});`
```

