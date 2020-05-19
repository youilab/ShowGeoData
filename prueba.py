import mapGeoData as mp
import pandas as pd

mapa = mp.set_data('SLP_mancha.shp')
slp = mp.read_shapefile(mapa)

y_lim = (22.00, 22.25)#latitude
x_lim = (-101.1, -100.83)#longitude



#Grafica el polígono 30 del mapa
#mp.plot_shape(30, mapa)



#Grafica el mapa dados los limites en X y Y
#mp.plot_map(mapa, x_lim, y_lim)



#Muestra los polígonos del 100 al 150 en el mapa en color verde
#ids = range(100, 150)
#mp.fill_multiples_shapes(ids, mapa, x_lim, y_lim, color='g')



#Muestra el polígono 30 con un relleno color rojo
#mp.fill_shape_into_map(30, mapa, x_lim, y_lim, color='r')



#Muestra los polígonos del 100 al 150 rellenos en rojo dentro del mapa
#ids = range(100, 150)
#mp.fill_multiples_shapes(ids, mapa, x_lim, y_lim, color='r')



#Muestra un mapa de calor dados los datos de nivel de riesgo
cds_data = pd.read_csv('cds_ssslp.data.csv')
cds_data_risk = cds_data[['Riesgo','lat','long']]
dat, ids = mp.get_heat_data(slp, cds_data_risk)
mp.fill_multiples_ids_tone(mapa, dat, ids, 8, x_lim, y_lim)




