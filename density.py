import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

try:
    from mpl_toolkits.basemap import Basemap
    basemap = True
except ImportError:
    basemap = False

df = pd.read_csv('cds_ssslp.data.csv')


# Filter SLP location data in
lat = df['lat']
long = df['long']
risk = df['Riesgo']

slp_top_left = [22.219247, -101.053618]
slp_bottom_right = [22.023170, -100.817158]
inslp = [];
count = 0;
for i in range(len(lat)):
    inslp.append(False);
    if lat[i] < slp_top_left[0] and lat[i] > slp_bottom_right[0] and long[i] > slp_top_left[1] and long[i] < slp_bottom_right[1]:
        inslp[i] = True;
        count = count +1;

latSLP = []
longSLP = []
riskSLP = []
label = []

for i in range(len(risk)):
    label.append(False)
    if risk[i] == "MARRON" or risk[i] == "ROJO" or risk[i] == "MORADO":
        label[i] = True;
        
        
        



for i in range(len(lat)):
    if inslp[i] == True and label[i] == True:
        latSLP.append(lat[i])
        longSLP.append(long[i])
        riskSLP.append(risk[i]) 

opt = ["Bajo",                  # AMARILLO 0
            "Grave",                 # MARRON 1
            "Síntomas respiratorios",#MORADO 2
            "Medio ",                #NARANJA 3
            "Alto",                  #ROJO 4
            "Sin riesgo"             #VERDE 5
 ];

# compuate data arrays for KDE
Xtrain = np.vstack([latSLP, longSLP]).T
Xtrain *= np.pi / 180.  # Convert lat/long to radians

kde = KernelDensity(bandwidth=0.0001, metric='haversine',
                        kernel='gaussian', algorithm='ball_tree')
kde.fit(Xtrain)


# compute grid
gridSize = 500
ygrid = np.linspace(slp_bottom_right[0], slp_top_left[0], gridSize )
xgrid = np.linspace(slp_bottom_right[1], slp_top_left[1], gridSize )
X, Y = np.meshgrid(xgrid, ygrid)
xy = np.vstack([Y.ravel(), X.ravel()]).T
xy *= np.pi / 180.
Z = np.exp(kde.score_samples(xy))
Z = Z.reshape(X.shape)

fig = plt.figure()
levels = np.linspace(0, Z.max(), 25)
#contour = plt.contour(X, Y, Z, levels=levels, cmap=plt.cm.Reds)

plt.contour(X,Y,Z, levels=levels, cmap=plt.cm.Reds)

plt.show()

