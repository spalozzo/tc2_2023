# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:50:02 2023

@author: Santiago Palozzo
"""
#%%
import numpy as np
import matplotlib.pyplot as plt

def bodePlot(modulo, my_label, fig):
    '''
    Parameters
    ----------
    modulo : vector de 2 columnas
        Primera columna eje frecuencial, segunda ganancia en [dB]
    my_label : string
        Leyenda del grafico
    fig : int
        N° de figura

    Returns
    -------
    int
        DESCRIPTION.
    '''
    
    plt.figure(fig)

    #bode_plots.suptitle('Diagramas de Bode')

    ## Ploteo el modulo
    plt.plot(modulo[:,0], modulo[:,1], label=my_label)
    plt.xscale("log")
    plt.legend()
    plt.grid()
    plt.ylabel('Magnitude [dB]')
    plt.title('Magnitude response')
    plt.show()
    
    return 0

def bodePlot4Filters(modulo, my_label):
    '''
    Parameters
    ----------
    modulo : vector de 2 columnas con los 4 filtros
        Primera columna eje frecuencial, segunda ganancia en [dB]
    my_label : string
        Array con las leyendas del grafico

    Returns
    -------
    int
        DESCRIPTION.
    
    '''
    # plt.figure(fig)

    bode_plots, filters= plt.subplots(2, 2)
    # mod_plot, fase_plot, ret_plot= bode_plots.subplots(3, 1, sharex=True)
    

    bode_plots.suptitle('Diagramas de Bode para los Filtros Ensayados')
    bode_plots.tight_layout()
    
    ## Ploteo el filtro 1
    plt.sca(filters[0,0])
    filters[0,0].plot(modulo[0][:,0], modulo[0][:,1], 'tab:blue', label=my_label[0])
    filters[0,0].set(xscale='log')
    filters[0,0].legend()
    filters[0,0].grid()
    filters[0,0].xaxis.set_tick_params(labelbottom=True)
    # i=-1
    # for item in modulo[0][:,1]:
    #     i += 1
    #     if item < -3:
    #         plt.axvline((modulo[0][i][0]), color='red', linestyle='--')   # stop   frequency
    #         break
    plt.axvline(7590, color='red', linestyle='--')   # stop   frequency
    
    plt.ylabel('Magnitude [dB]')
    plt.title('Caracteristica del Sistema')

    # ## Ploteo el filtro 2
    plt.sca(filters[0,1])
    filters[0,1].plot(modulo[1][:,0], modulo[1][:,1], 'tab:orange', label=my_label[1])
    filters[0,1].set(xscale='log')
    filters[0,1].legend()
    filters[0,1].grid()
    filters[0,1].xaxis.set_tick_params(labelbottom=True)
    # filters[0,1].yaxis.set_tick_params(labelleft=False)
    plt.axvline(1000, color='green', linestyle='--') # cutoff frequency
    plt.axvline(2000, color='red', linestyle='--')   # stop   frequency
    # plt.ylabel('Magnitude [dB]')
    plt.title('Pasabajos FIR')
    
    # ## Ploteo el filtro 3
    plt.sca(filters[1,0])
    filters[1,0].plot(modulo[2][:,0], modulo[2][:,1], 'tab:green', label=my_label[2])
    filters[1,0].set(xscale='log')
    filters[1,0].legend()
    filters[1,0].grid()
    plt.axvline(2000, color='green', linestyle='--') # cutoff frequency
    plt.axvline(4000, color='red', linestyle='--')   # stop   frequency
    plt.axvline(6000, color='red', linestyle='--') # stop   frequency
    plt.axvline(8000, color='green', linestyle='--') # cutoff frequency
    plt.ylabel('Magnitude [dB]')
    plt.xlabel('Angular frequency [rad/sec]')
    plt.title('Elimina Banda FIR')
    
    # ## Ploteo el filtro 4
    plt.sca(filters[1,1])
    filters[1,1].plot(modulo[3][:,0], modulo[3][:,1], 'tab:red', label=my_label[3])
    filters[1,1].set(xscale='log')
    filters[1,1].legend()
    filters[1,1].grid()
    # filters[1,1].yaxis.set_tick_params(labelleft=False)
    plt.axvline(2000, color='green', linestyle='--') # cutoff frequency
    plt.axvline(3000, color='red', linestyle='--')   # stop   frequency
    # plt.ylabel('Magnitude [dB]')
    plt.xlabel('Angular frequency [rad/sec]')
    plt.title('Pasabajos IIR')
    
    # for ax in filters.flat:
    #     ax.label_outer()
    
    plt.show()
    
    return 0
#%%
plt.close('all')

#Levanto los archivos del analizador de audio
# modulo = np.zeros((4,2),dtype=np.ndarray)

modulo= np.zeros(4, dtype=np.ndarray)
labels= ["Filtro Talkthrough", "FIR Equiripple", "FIR Least Squares", "IIR Butterworth"]
for (i) in [0,1,2,3]:    
    modulo[i]= np.genfromtxt("./SweepData_{:d}.csv".format(i), delimiter=",")
    # bodePlot(modulo[i], labels[i], i+1)

bodePlot4Filters(modulo, labels)


#%%
# #Levanto los archivos medidos del osciloscopio
# modulo_osc= np.genfromtxt("./modulo_osciloscopio.csv", delimiter=";")


# bodePlot(modulo_osc, 'Pasabanda Cheby UAF42', 2)


