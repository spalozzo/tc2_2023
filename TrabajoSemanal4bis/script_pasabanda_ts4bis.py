# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:37:48 2023

@author: Santi Palozzo

Tarea Semanal 4 bis - Diseño de pasabanda maxima planicidad

En este ejercicio se diseña un filtro pasabanda a partir de una plantilla,
utilizando el prototipo pasabajo y su nucleo de transformacion.

"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pytc2.sistemas_lineales as tc2

plt.close('all')

#%%Defino los parametros de la plantilla
fs1= 1250
fs2= 3200
fci= 1600
fcs= 2500

alfa_max= 3     # dB, es un butter
alfa_min= 20    # dB, igual para ambas bandas de stop

ganancia= 10    # dB, en la banda de paso

ee2= 1
n= 3
Q_bp= 20/9  # Calculado en papel
Bw= 1/Q_bp  # w0= 1

#%% Consigo el pasabanda de una
print("- Prototipo Pasabajo Butterworth -")
print("Epsilon2= ",ee2)
print("Grado del filtro: ",n)

z, p, k= sig.buttap(n)
num_lp, den_lp= sig.zpk2tf(z, p, k)
tc2.pretty_print_lti(num_lp, den_lp)

num_bp, den_bp= sig.lp2bp(num_lp, den_lp, bw = 1/Q_bp)
tc2.pretty_print_lti(num_bp, den_bp)

## Muestro la transferencia BP en secciones de 2do orden
sos_bp = tc2.tf2sos_analog(num_bp, den_bp)
tc2.pretty_print_SOS(sos_bp)

tf_bp =  sig.TransferFunction(num_bp, den_bp)
#tc2.analyze_sys(tf_bp, sys_name='Pasabanda 2do orden')

bp1n,bp2n,bp3n= [(0, 0.626/5, 0), (0, 1.1077/16.1, 0), (0, 0.903/16.1, 0)]
bp1d,bp2d,bp3d= [(1, 0.626/5, 1), (1, 1.1077/16.1, 1.1077**2), (1, 0.903/16.1, 0.903**2)]

num1=np.polymul(bp1n,bp2n)
den2=np.polymul(bp1d,bp2d)
tf_bp_pasiva =  sig.TransferFunction(np.polymul(num1,bp3n), np.polymul(den2,bp3d))
tc2.analyze_sys(tf_bp_pasiva, sys_name='Pasabanda 2do orden PASIVO')

"""
En este punto, si la simulacion salio bien de acuerdo a la plantilla, puedo
pasar a la implementacion circuital
"""

#Esto me devuelve numerador y denominador de las distintas secciones
#que componen el filtro