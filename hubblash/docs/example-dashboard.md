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
  ${mapcoord}
  <div class="card" style="padding: 0;">
    ${Inputs.table(hubblo)}
  </div>
</div>


```js
const mapcoord = html`<div class="card" id="map" style='height: 300px'> </div>`;
const coord = Generators.input(mapcoord);
```

```js
const db = DuckDBClient.of({carreaux: FileAttachment("data/Filosofi2017_carreaux_200m_met_Men.parquet")});
```


```js
  const map = new Promise((resolve) => {setTimeout(() => {var map2 = L.map("map").setView([43.596, 1.4419], 10); 
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map2);}, 1000);
});
```


```js
import * as L from "npm:leaflet";
```


```js
var x = 574153.0242929291
var y = 6278679.902778912
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

```js
const coordinates3035 = [3629901.572132665, 2315824.6029212857]
```

```js
const rayon = view(Inputs.range([200, 1000], {step: 100}));
```
