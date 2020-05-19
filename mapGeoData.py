import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shapefile as shp
import seaborn as sns
from shapely.geometry import Point, Polygon


def set_data(path):
    '''
    Returns a shapefile object
    '''
    return shp.Reader(path)


def read_shapefile(mapa):
    """
    Read a shapefile into a Pandas dataframe with a 'coords'
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in mapa.fields][1:]
    records = mapa.records()
    shps = [s.points for s in mapa.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df


def plot_shape(id, mapa):
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = mapa.shape(id)
    df = read_shapefile(mapa)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon,y_lat)
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, df.iloc[id]['Name'], fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    plt.show()
    #return x0, y0


def plot_map(mapa, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Requires the set_data shapefile object.
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    id = 0
    for shape in mapa.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')


        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=10)
        id = id + 1

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)

        plt.show()


def plot_shape_into_map(id, mapa, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Highlight a single shape within a map
    '''

    plt.figure(figsize=figsize)
    for shape in mapa.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

    shape_ex = mapa.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon, y_lat, 'r', linewidth=2)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.show()


def fill_shape_into_map(id, mapa, x_lim=None, y_lim=None, figsize=(11, 9), color = 'r'):
    '''
    Fill a single shape within a map
    '''

    plt.figure(figsize=figsize)
    for shape in mapa.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

    shape_ex = mapa.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.fill(x_lon,y_lat, color)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.show()


def fill_multiples_shapes(ids, mapa, x_lim=None, y_lim=None, figsize=(11, 9), color='r'):
    '''
    Fill multiple shapes by id within a map
    '''

    plt.figure(figsize=figsize)
    for shape in mapa.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

    for id in ids:
        shape_ex = mapa.shape(id)
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        plt.fill(x_lon, y_lat, color)

        #x0 = np.mean(x_lon)
        #y0 = np.mean(y_lat)
        #plt.text(x0, y0, id, fontsize=10)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.show()


def calc_color(data, color=None):

    """
        Set the color scales for a heating map
    """

    if color == 1:
        color_sq = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0', '#807dbaF0', '#6a51a3F0', '#54278fF0']
        colors = 'Purples'

    elif color == 2:
        color_sq = ['#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#253494']
        colors = 'YlGnBu'

    elif color == 3:
        color_sq = ['#f7f7f7', '#d9d9d9', '#bdbdbd', '#969696', '#636363', '#252525']
        colors = 'Greys'
    elif color == 9:
        color_sq = ['#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000']
    else:
        color_sq = ['#ffffd4', '#fee391', '#fec44f', '#fe9929', '#d95f0e', '#993404']
        colors = 'YlOrBr'

    dat = set(data)
    dat = list(dat)

    new_data, bins = pd.qcut(dat, 6, retbins=True, labels=list(range(6)))
    color_ton = []
    for val in new_data:
        color_ton.append(color_sq[val])

    tonos = []

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
        if data[i] > int(bins[5])-1:
            tonos.append(color_sq[5])

    if color != 9:
        colors = sns.color_palette(colors, n_colors=6)
        sns.palplot(colors, 0.6)
        #for i in range(6):
        #    print("\n" + str(i + 1) + ': ' + str(int(bins[i])) + " => " + str(int(bins[i + 1]) - 1), end=" ")
        #print("\n\n   1   2   3   4   5   6")

    return tonos, bins


def plot_ids_data(mapa, ids, data=None, color=None):
    '''
    Plot map with selected comunes, using specific color
    '''

    color_ton, bins = calc_color(data, color)
    df = read_shapefile(mapa)
    comuna_id = []
    for i in ids:
        i = conv_comuna(i).upper()
        comuna_id.append(df[df.NOM_COMUNA == i.upper()].index.get_values()[0])
    fill_multiples_ids_tone(mapa, ids, color_ton, bins, x_lim=None, y_lim=None, figsize=(11, 9))


def fill_multiples_ids_tone(mapa, data, ids, color, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''

    color_ton, bins = calc_color(data, color)

    plt.figure(figsize=figsize)
    #fig, ax = plt.subplots(figsize=figsize)

    for shape in mapa.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

    for id in range(len(ids)):
        shape_ex = mapa.shape(ids[id])
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        plt.fill(x_lon, y_lat, color_ton[id])
    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.show()


def get_heat_data(map, app_data):

    """
    Requires a pandas dataFrame containing the fields: Riesgo, lat, long
    Returns the ids and the given risk value for each id
    """

    k = 0

    data = np.zeros(len(map))

    for i in range(len(app_data)):
        coords = Point(app_data['long'].iloc[i], app_data['lat'].iloc[i])
        for j in range(len(map)):
            poly = Polygon(map['coords'].iloc[j])
            if coords.within(poly):
                k += 1
                if app_data['Riesgo'].iloc[i] == 'AMARILLO':
                    data[j] += 1
                if app_data['Riesgo'].iloc[i] == 'NARANJA':
                    data[j] += 2
                if app_data['Riesgo'].iloc[i] == 'ROJO':
                    data[j] += 3
                if app_data['Riesgo'].iloc[i] == 'MARRON':
                    data[j] += 4
                if app_data['Riesgo'].iloc[i] == 'MORADO':
                    data[j] += 5

    dat = []
    ids = []
    for i in range(len(data)):
        if data[i] > 0:
            dat.append(int(data[i]))
            ids.append(i)

    return dat, ids

