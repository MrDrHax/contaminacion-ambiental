"""
Este codigo esta hecho con la intencion de poder tomar informacion de distintas tablas del gobierno y unificarlas a una comun.
El lugar donde se encuentran todos los datos de informacion de contaminacion del medio ambiente es en:
http://www.aire.cdmx.gob.mx/default.php?opc=%27aKBh%27

Creado por: Alejandro Fernandez del Valle Herrera
"""

from os import error
import pandas as pd
import numpy as np

from pandas.core.construction import array

nombreDeTablaFinal = "procesados/output.xlsx"

pathInput = "datos/"

busqueda = ["CO", "NO", "NO2", "NOX", "O3", "PM10", "PM25", "PMCO", "SO2"]

celdaDeInteres = 6

inicio = 2000
fin = 2020

tiempos = np.arange(inicio, fin + 1, dtype = int)

MESES = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')

def crearTabla():
    """
    Crea una tabla vacia de pandas
    """
    columnas = ["Año", "Mes", "CO", "NO", "NO2", "NOX", "O3", "PM10", "PM25", "PMCO", "SO2"]
    dataframe = pd.DataFrame(columns=columnas)

    return dataframe

def abrirTabla(path):
    """
    Regresa el DF de la tabla de excel
    """
    try:
        tabla = pd.read_excel(pathInput + path)

        meses = []

        # esto se usa para sacar los promedios
        actual = 1
        contador = 0
        acumulador = 0

        for fila in range(len(tabla.index)):
            # me meto a cada fila para ver en que mes esta, y poder sacar promedio

            mesActual = tabla.iloc[fila][0].month
            
            if mesActual != actual: # corremos esto si es cambio de mes
                actual = mesActual

                try:
                    meses.append(acumulador / contador) # qui ponemos el promedio del mes en meses
                except:
                    meses.append(np.nan) # si hay una division entre 0 es que todo estuvo roto y no sirve
                contador = 0
                acumulador = 0
            
            if (valor := tabla.iloc[fila][celdaDeInteres]) != -99:
                contador += 1
                acumulador += valor

        try:
            meses.append(acumulador / contador) # qui ponemos el promedio del mes en meses
        except:
            meses.append(np.nan) # si hay una division entre 0 es que todo estuvo roto y no sirve

        print(meses)
        return meses
    except Exception as e:
        print(f"error al leer cosas: {e}")
        return [np.nan] * 12

def crearTablaConValores(year :int, valores : dict):
    """
    Agrega los valores a una tabla en el año especificado

    Regresa la tabla creada
    """

    tabla = crearTabla()
    
    for mes in range(12):
        row = [year, MESES[mes]] # se crean las primeras 2 columnas
        for key in busqueda: # luego se llenan
            try:
                
                row.append(valores[key][mes])
            except:
                row.append(np.nan)
        
        tabla.loc[mes] = row

    return tabla

def analizarDatos():
    tablaParaGuardar = crearTabla()
    for i in tiempos:
        diccionario = {}
        for j in busqueda:
            diccionario[j] = abrirTabla(f"{i}{j}.xls")
        
        tablaParaGuardar = tablaParaGuardar.append(crearTablaConValores(i,diccionario))
    

    tablaParaGuardar.to_excel(nombreDeTablaFinal)

analizarDatos()