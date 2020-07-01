import pandas as pd
import mapGeoData as mp
import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from haversine import haversine, Unit


def get_heat_data(map, app_data):

    k = 0

    data = np.zeros(len(map))
    for i in range(len(app_data)):
        coords = Point(app_data['long'].iloc[i], app_data['lat'].iloc[i])
        for j in range(len(map)):
            poly = Polygon(map['coords'].iloc[j])
            if coords.within(poly):
                k += 1
                if app_data['Riesgo'].iloc[i] != 'VERDE':
                    data[j] += 1

    dat = []
    ids = []
    for i in range(len(data)):
        if data[i] > 0:
            dat.append(int(data[i]))
            ids.append(i)

    return dat, ids


def calc_color(data, nom, color=None):

    """
        Set the color scales for a heating map
    """
    nom = nom + '_paleta.png'

    if color == 1:
        color_sq = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0', '#807dbaF0', '#6a51a3F0', '#54278fF0']
        #Purples
    elif color == 2:
        color_sq = ['#ccffe5', '#84ffe0', '#2db7b7', '#3399CC', '#3366CC', '#000099']
        #Blues
    elif color == 3:
        color_sq = ['#e4bfbf', '#c97f7f', '#ae3f3f', '#942525', '#631919', '#310c0c']
        #Brouns
    elif color == 4:
        color_sq = ['#ffffcc', '#ffff99', '#ffff66', '#ffff00', '#cccc00', '#7f7f00']
        #Yellows
    elif color == 5:
        color_sq = ['#ffcccc', '#ff7f7f', '#ff4c4c', '#ff0000', '#7f0000', '#4c0000']
        #Reds
    elif color == 6:
        color_sq = ['#ffe4b2', '#ffc966', '#ffae19', '#ffa500', '#cc8400', '#7f5200']
        #Oranges
    elif color == 7:
        color_sq = ['#b2d8b2', '#66b266', '#329932', '#008000', '#005900', '#003300']
        #Geens
    elif color == 9:
        color_sq = ['#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000']
    else:
        color_sq = ['#ffffd4', '#fee391', '#fec44f', '#fe9929', '#d95f0e', '#993404']
        #Heat


    dat = set(data)
    if max(dat) >= 6:
        n = 6
    elif max(dat) < 6:
            n = max(dat)

    dat = list(dat)

    try:
        new_data, bins = pd.qcut(dat, n, retbins=True, labels=list(range(n)))
    except:
        new_data, bins = pd.qcut(dat, 6, retbins=True, labels=False)

    color_ton = []


    for val in new_data:
        color_ton.append(color_sq[val])

    tonos = []

    if max(dat) > 6:
        for i in range(len(data)):
            if data[i] > 0 and data[i] < int(bins[1]):
                tonos.append(color_sq[0])
            if data[i] > int(bins[1])-1 and data[i] < int(bins[2]):
                tonos.append(color_sq[1])
            if data[i] > int(bins[2])-1 and data[i] < int(bins[3]):
                tonos.append(color_sq[2])
            if data[i] > int(bins[3])-1 and data[i] < int(bins[4]):
                tonos.append(color_sq[3])
            if data[i] > int(bins[4])-1 and data[i] < int(bins[5]):
                tonos.append(color_sq[4])
            if data[i] > int(bins[5])-1 :
                tonos.append(color_sq[5])
    elif max(dat) < 7:
        #try:
        #for i in range(len(data)):
        #    print("hola2")
        #    tonos.append(color_sq[new_data[i]-1])
        f = 0
        #except:
        for i in range(len(data)):

            if data[i] > 0 and data[i] < bins[1]:
                tonos.append(color_sq[0])
                f += 1
            elif data[i] >= bins[1] and data[i] < bins[2]:
                tonos.append(color_sq[1])
                f += 1
            elif data[i] >= bins[2] and data[i] < bins[3]:
                tonos.append(color_sq[2])
                f += 1
            elif data[i] >= bins[3] and data[i] < bins[4]:
                tonos.append(color_sq[3])
                f += 1
            elif data[i] >= bins[4] and data[i] < bins[5]:
                tonos.append(color_sq[4])
                f += 1
            elif data[i] >= bins[5] - 1:
                tonos.append(color_sq[5])
                f += 1


    return tonos, bins, color_sq


def fill_multiples_ids_tone(Lat, Long, mapa, data, ids, color, nom, ids_slp, x_lim=None, y_lim=None, figsize=(19.37, 17.86)):
    '''
    Plot map with lim coordinates
    '''

    ids_no = [801, 815, 814, 802, 806, 798, 774, 727, 762, 547, 612, 493, 364, 390, 402, 492, 794,
              473, 399, 406, 382, 378, 304, 371, 370, 476, 779, 403, 387, 745, 770, 800, 809, 803,
              805, 808, 797, 807, 816, 804, 365, 363, 375, 376, 813, 811, 810, 791, 817, 799, 812]

    color_ton, bins, color_sq = calc_color(data, nom, color)

    labels = []

    print(bins)

    #if max(data) < 7:
    for i in range(6):
        if i == 0:
            labels.append('0 - ' + str(round(bins[1],3)))
        else:
            labels.append(str(round(bins[i], 1)) + ' - ' + str(round(bins[i+1], 1)))
    """
    elif max(data) > 6:
        for i in range(6):
            labels.append(bins[i+1]/max(data))
            labels[i] *= 100
            if i == 0:
                labels[i] = round(labels[i], 2)
                labels[i] = '0% - ' + str(labels[i]) + '%'
            else:
                labels[i] = round(labels[i], 2)
                lbl1 = bins[i]/max(data)
                lbl1 *= 100
                lbl1 = round(lbl1 + 0.01,2)
                labels[i] = str(lbl1) + '% - ' + str(round(labels[i],1)) + '%'
    """

    plt.figure(figsize=figsize)
    #fig, ax = plt.subplots(figsize=figsize)
    d = 0
    for shape in mapa.shapeRecords():
        d += 1
        if d not in ids_no:
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            #x0 = np.mean(x)
            #y0 = np.mean(y)
            #plt.text(x0, y0, d, fontsize=8)
            plt.plot(x, y, 'k')


    #print(len(color_ton))
    #print(ids)

    notfill = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 29, 32, 99, 102, 173, 395, 384, 368, 351, 412,
               400, 415, 417, 418, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 32]

    for i in range(len(ids)):
        if i not in notfill:
            """if i > 412 and i < 416:#390
                shape_ex = mapa.shape(ids[i])
                x_lon = np.zeros((len(shape_ex.points), 1))
                y_lat = np.zeros((len(shape_ex.points), 1))
                for ip in range(len(shape_ex.points)):
                    x_lon[ip] = shape_ex.points[ip][0]
                    y_lat[ip] = shape_ex.points[ip][1]

                plt.fill(x_lon, y_lat, "#ff0000")
            else:"""
            shape_ex = mapa.shape(ids[i])
            x_lon = np.zeros((len(shape_ex.points), 1))
            y_lat = np.zeros((len(shape_ex.points), 1))
            for ip in range(len(shape_ex.points)):
                x_lon[ip] = shape_ex.points[ip][0]
                y_lat[ip] = shape_ex.points[ip][1]

            plt.fill(x_lon, y_lat, color_ton[i])

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    lgnd = []
    for k in range(len(color_sq)):
        lgnd.append(mpatches.Patch(color=color_sq[k]))


    plt.legend(lgnd, labels, loc="best", prop={'size': 12})
    plt.axis('off')
    plt.tight_layout()
    plt.scatter(Long, Lat, marker='o', color='red', s=80, zorder=3)
    #plt.savefig(nom)
    plt.savefig("test_densidad.svg", format="svg")





d_pob = mp.set_data('Poblacion_Densidad_secc_mun.shp')
slp_dp = mp.read_shapefile(d_pob)

#estado
# y_lim = (21.07, 24.53)#latitude
#x_lim = (-102.33, -98.3)#longitude

#capital
y_lim = (22.0684, 22.229)#latitude
x_lim = (-101.057, -100.869)#longitude

H = haversine([y_lim[0], x_lim[0]], [y_lim[0], x_lim[1]])
W = haversine([y_lim[0], x_lim[0]], [y_lim[1], x_lim[0]])


#Muestra un mapa de calor dados los datos de nivel de riesgo
cds_data = pd.read_csv('cds_ssslp.data.csv')

#ids_not = [801, 815, 814, 802, 806, 798, 774, 727, 762, 547, 612, 493, 364,
#           390, 402, 492, 473, 399, 406, 382, 378, 304, 371, 370, 476, 779,
#           403, 387, 745, 770, 800, 809, 805, 808, 797, 807, 816, 804]

slp_top_left = [22.219247, -101.053618]
slp_bottom_right = [22.023170, -100.817158]
lat = cds_data['lat']
long = cds_data['long']
inslp = []

count = 0;
for i in range(len(lat)):
    inslp.append(False);
    if lat[i] < slp_top_left[0] and lat[i] > slp_bottom_right[0] and long[i] > slp_top_left[1] and long[i] < slp_bottom_right[1]:
        inslp[i] = True;
        count = count +1;

indices = []
for i in range(len(cds_data)):
    if not inslp[i]:
        indices.append(i)

csv = cds_data.drop(indices)


Lat = []
Long = []

for i in range(len(csv)):
    if csv['Riesgo'].iloc[i] != 'VERDE':
        Lat.append(float(csv['lat'].iloc[i]))
        Long.append(float(csv['long'].iloc[i]))


#plt.scatter(Long, Lat, marker='o', color='red', s=20)
#plt.show()


ids_not = []
ids_slp = []

for i in range(len(slp_dp)):
    if slp_dp.MUNICIPIO[i] == 28.0 or slp_dp.MUNICIPIO[i] == 35.0:
        ids_slp.append(i)

for i in range(len(slp_dp)):
    if slp_dp.MUNICIPIO[i] != 28.0 and slp_dp.MUNICIPIO[i] != 35.0:
        ids_not.append(i)

dp = slp_dp.drop(ids_not)


cds_data_risk = csv[['Riesgo','lat','long']]


#dat, ids = get_heat_data(slp_dp, cds_data_risk)


#Calculo de densidad
casos_densidad = []
"""
for i in range(len(dat)):
    casos_densidad.append(dat[i]/slp_dp['densidad'].iloc[ids[i]]*100)
    casos_densidad[i] = round(casos_densidad[i],3)
"""

for i in range(len(ids_slp)):
    casos_densidad.append(slp_dp['densidad'].iloc[ids_slp[i]])
    casos_densidad[i] = round(casos_densidad[i], 1)

print(len(ids_slp))
#print(len(casos_densidad))


fill_multiples_ids_tone(Lat, Long, d_pob, casos_densidad, ids_slp, 2, 'densidad_pob',ids_slp , x_lim, y_lim, figsize=(H, W))

plt.show()


