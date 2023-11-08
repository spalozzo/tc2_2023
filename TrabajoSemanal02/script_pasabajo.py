#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 18:44:39 2023

@author: santi
"""
#%% Inicializacion de librerias
# Librerías externas NumPy, SciPy y Matplotlib
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt
import numpy as np

# Librería de TC2
from pytc2.sistemas_lineales import pzmap, GroupDelay, bodePlot

#%% Defino los parametros
w0=10**0 ; q=3 ; r=1 ; k=1

#%% Defino los componentes y la transferencia
R1= r/k; R2=q*r*w0; R3=r; C=1/(r*w0);

my_tf = TransferFunction( [k * w0**2], [1, w0/q, w0**2] )

#%% Gráficos
plt.close('all')

bodePlot(my_tf, fig_id=1, filter_description = 'Pasabajo')

pzmap(my_tf, fig_id=2, filter_description = 'Pasabajo') #S plane pole/zero plot

GroupDelay(my_tf, fig_id=3, filter_description = 'Pasabajo')
