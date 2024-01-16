# hubblapp

Les données sont disponibles ici : https://minio.lab.sspcloud.fr/h529p3/data/Filosofi2017_carreaux_200m_met.parquet

Pour l'api, je propose un requêtage du type 
hubblapp.fr x,y,r 
avec x,y, et y respectivement les coordonnées du centre et le rayon. Pour l'instant la projection est en lambert 93. On peut rajouter un paramètre epsg. A mon avis, on pourrait également proposer dans un deuxième temps de faire les calculs sur des geojsons à façon.
