# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:50:02 2023

@author: Santiago Palozzo
"""
#%%
import numpy as np
import matplotlib.pyplot as plt

def bodePlot(modulo, fase, my_label, fig):
    '''
    Parameters
    ----------
    modulo : vector de 2 columnas
        Primera columna eje frecuencial, segunda ganancia en [dB]
    fase : vector de 2 columnas
        Primera columna eje frecuencial, segunda fase en [radianes]
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
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase [rad]')
    plt.title('Phase response')
    plt.show()
    
    return 0
#%%

plt.close('all')

#Levanto los archivos del analizador de audio
modulo= np.genfromtxt("./barrido_modulo.csv", delimiter=",")
fase=   np.genfromtxt("./barrido_fase.csv", delimiter=",")
fase[:,1]= [item * np.pi/180 for item in fase[:,1] ]


bodePlot(modulo, fase, 'Pasabanda Cheby UAF42', 1)

#Levanto los archivos medidos del osciloscopio
modulo_osc= np.genfromtxt("./modulo_osciloscopio.csv", delimiter=";")
fase_osc=   np.genfromtxt("./fase_osciloscopio.csv", delimiter=";")

bodePlot(modulo_osc, fase_osc, 'Pasabanda Cheby UAF42', 2)


