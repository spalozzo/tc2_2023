# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 17:26:54 2023

@author: Santi Palozzo

Tarea Semanal 4 bis2

Diseño de un filtro pasabanda mediante la aproximacion de Chebyshev y la
transformacion en frecuencia de un prototipo pasabajos.

"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pytc2.sistemas_lineales as tc2

plt.close('all')

#Parametros de la plantilla
alfa_max= 0.5
n=3
Q_bp= 5

#%%Prototipo pasabajo
w0_lp1= 0.626
w0_lp2= 1.069
Q_lp2= 1.71

#Pasabajos 1er orden
num_lp1= np.array([w0_lp1])
den_lp1= np.array([1, w0_lp1])

#Pasabajos 2do orden
num_lp2= np.array([w0_lp2**2])
den_lp2= np.array([1, w0_lp2/Q_lp2, w0_lp2**2])

num_lp= np.polymul(num_lp1, num_lp2)
den_lp= np.polymul(den_lp1, den_lp2)

#print(num_lp); print(den_lp)
sos_lp = tc2.tf2sos_analog(num_lp, den_lp)
print("Transferencia Pasabajos como SOS")
tc2.pretty_print_SOS(sos_lp)

#%%Transformacion en frecuencia
num_bp, den_bp= sig.lp2bp(num_lp, den_lp, bw = 1/Q_bp)

sos_bp = tc2.tf2sos_analog(num_bp, den_bp)
print("\nTransferencia Pasabanda como SOS")
tc2.pretty_print_SOS(sos_bp)
#tc2.pretty_print_SOS(sos_bp, mode='omegayq')

tf_bp =  sig.TransferFunction(num_bp, den_bp)

tc2.analyze_sys(tf_bp, sys_name="Pasabanda Cheby Q=5")
