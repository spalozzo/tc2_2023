# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:50:02 2023

@author: Santiago Palozzo
"""
#%%
import numpy as np
import matplotlib.pyplot as plt

def bodePlot(modulo, fase, retardo, my_label, fig):
    '''
    Parameters
    ----------
    modulo : vector de 2 columnas
        Primera columna eje frecuencial, segunda ganancia en [dB]
    fase : vector de 2 columnas
        Primera columna eje frecuencial, segunda fase en [radianes]
    retardo : vector de 2 columnas
        Primera columna eje frecuencial, segunda retardo de grupo en [segundos]
    my_label : string
        Leyenda del grafico
    fig : int
        N° de figura

    Returns
    -------
    int
        DESCRIPTION.
    '''
    
    bode_plots= plt.figure(fig)
    mod_plot, fase_plot= bode_plots.subplots(2, 1, sharex=True)
    # mod_plot, fase_plot, ret_plot= bode_plots.subplots(3, 1, sharex=True)
    

    #bode_plots.suptitle('Diagramas de Bode')

    ## Ploteo el modulo
    plt.sca(mod_plot)
    mod_plot.plot(modulo[:,0], modulo[:,1], label=my_label)
    mod_plot.set(xscale='log')
    mod_plot.legend()
    mod_plot.grid()
    plt.ylabel('Magnitude [dB]')
    plt.title('Magnitude response')

    ## Ploteo la fase
    plt.sca(fase_plot)
    fase_plot.plot(fase[:,0], fase[:,1], label=my_label)
    fase_plot.set(xscale='log')
    fase_plot.legend()
    fase_plot.grid()
    # plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase [rad]')
    plt.title('Phase response')
    plt.show()
    
    # ## Ploteo el retardo
    # plt.sca(ret_plot)
    # ret_plot.plot(retardo[:,0], retardo[:,1], label=my_label)
    # ret_plot.set(xscale='log')
    # ret_plot.legend()
    # ret_plot.grid()
    # plt.xlabel('Angular frequency [rad/sec]')
    # plt.ylabel('Group delay [sec]')
    # plt.title('Group delay')
    # plt.show()
    
    return 0
#%%

plt.close('all')

#Levanto los archivos del analizador de audio
modulo= np.genfromtxt("./barrido_modulo.csv", delimiter=",")
fase= np.genfromtxt("./barrido_fase.csv", delimiter=",")
fase[:,1]= [item * np.pi/180 for item in fase[:,1] ]

retardo= fase.copy()
    
# for i in range(len(fase)):
#     if(i < len(fase)-1):
#         retardo[i][1]= fase[i+1][1]-fase[i][1]

# retardo[i][1]= retardo[i-1][1]

dx = retardo[1][0] - retardo[0][0]  # Paso entre los puntos
dy = np.diff(retardo[:,1])  # Diferencias entre los valores de y
dy.resize(len(retardo))

retardo[:,1] = dy / dx  # Derivada aproximada

bodePlot(modulo, fase, retardo, 'Pasabanda Cheby UAF42', 1)


#%%
#Levanto los archivos medidos del osciloscopio
modulo_osc= np.genfromtxt("./modulo_osciloscopio.csv", delimiter=";")
fase_osc= np.genfromtxt("./fase_osciloscopio.csv", delimiter=";")
retardo_osc= np.genfromtxt("./retardo_osciloscopio.csv", delimiter=";")

retardo_osc= fase_osc.copy()

dx = 1000  # Paso entre los puntos
dy = np.diff(retardo_osc[:,1])  # Diferencias entre los valores de y
dy.resize(len(retardo_osc))

retardo_osc[:,1] = dy   # Derivada aproximada


bodePlot(modulo_osc, fase_osc, retardo_osc, 'Pasabanda Cheby UAF42', 2)


