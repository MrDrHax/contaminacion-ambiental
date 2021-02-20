"""
Este codigo esta hecho con la intencion de tomar el output en excel y convertirlo a graficas distintas.

Utiliza el formato creado en el pasado, y crea una grafica en matplotlib, para exportarla a imagen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl

tabla = pd.read_excel("procesados/output.xlsx")

busqueda = ["CO", "NO", "NO2", "NOX", "O3", "PM10", "PM25", "PMCO", "SO2"]

tiempos = [tabla['Año'].to_numpy(),tabla['Mes'].to_numpy()]
tiemposSting = [str(tiempos[0][i]) + " " + str(tiempos[1][i]) for i in range(len(tiempos[0]))]

conversiones = []

for item in busqueda:
    conversiones.append(tabla[item].to_numpy())

mpl.scatter(tiemposSting, conversiones[0])

mpl.show()