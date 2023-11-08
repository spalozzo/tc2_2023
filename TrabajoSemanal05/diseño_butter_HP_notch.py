# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 13:02:58 2023

@author: Santi Palozzo
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pytc2.sistemas_lineales as tc2


#Defino los parametros de la plantilla
w0= 2*np.pi*300
wz= 2*np.pi*100

w0_n= w0/w0
wz_n= wz/w0

#Transformo a prototipo pasabajo
W0= 1/w0_n
Wz= 1/wz_n

alfa_max= 3 #en dB

ee2= 1
n= 3


print("- Aproximacion de Butterworth -")
print("Epsilon2= ",ee2)
print("Grado del filtro: ",n)

plt.close('all')

#Generacion del filtro

z,p,k= sig.buttap(n)

num_lp,den_lp= sig.zpk2tf(z,p,k)
tf_lp= sig.TransferFunction(num_lp,den_lp)

#Agrego cero de transmision
k= 1/(Wz/W0)**2
num_lp_notch= [1*k, 0, Wz**2 *k]
tf_lp_notch= sig.TransferFunction(num_lp_notch, den_lp)

#tc2.analyze_sys(tf_lp, sys_name="Prototipo Pasabajo")
#tc2.analyze_sys(tf_lp_notch, sys_name="Prototipo Pasabajo Notch")

#Transformacion a pasaalto
num_hp, den_hp= sig.lp2hp(num_lp, den_lp)
tf_hp= sig.TransferFunction(num_hp, den_hp)

k_hp= 1/(wz_n/w0_n)**2
#Agrego el cero de transmision
#num_hp_notch= [1, 0, wz_n**2,0]
num_hp[2]= wz_n**2

tf_hp_notch= sig.TransferFunction(num_hp, den_hp)

print(tf_hp_notch)


tc2.analyze_sys(tf_hp, sys_name="Filtro Pasa-alto")
tc2.analyze_sys(tf_hp_notch, sys_name="Filtro Pasa-alto Notch")






