#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 18:52:17 2023

@author: Santiago Palozzo
"""

# Librerías externas NumPy, SciPy y Matplotlib
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt
import numpy as np


# Librería de TC2
from pytc2.sistemas_lineales import pzmap, GroupDelay, bodePlot

#Valores desnormalizados
#R1= 1000; R2=1000; R3=1000; C=1e-6;

#Valores normalizados
R1= 1; R2=R1; R3=R1; C=1/R1;

#w0 = 1/(R3*C)
w0 = 1

my_tf_norm = TransferFunction( [1, -(R2/R1)*w0], [1, w0] )

plt.close('all')

bodePlot(my_tf_norm, fig_id=1, filter_description = 'Pasatodo')

pzmap(my_tf_norm, fig_id=2, filter_description = 'Pasatodo') #S plane pole/zero plot

GroupDelay(my_tf_norm, fig_id=3, filter_description = 'Pasatodo')
