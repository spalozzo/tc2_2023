#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 05:47:28 2023

@author: Santiago Palozzo
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

# Librería de TC2
import pytc2.sistemas_lineales as tc2

#Defino constantes
BUTTER= 0
CHEBY=  1

texto_aprox= ["Butterworth", "Chebyshev"]
#Defino los parametros de la plantilla
wc=1
ws=3
fc= 2*np.pi*wc
fs= 2*np.pi*ws
alfa_max= 0.4   #en dB
alfa_min= 48    #en dB

tipo_aprox= CHEBY

ee2= 10**(alfa_max/10) - 1

alfa=0
n=1
while(alfa<alfa_min):
    if(tipo_aprox==BUTTER):
        alfa=0
    else:
        n+=1
        alfa= 10* np.log10(1 + (ee2 * np.cosh(n*np.arccosh(ws))**2))

print("- Aproximacion de ",texto_aprox[tipo_aprox] ," -")
print("Epsilon2= ",ee2)
print("Grado del filtro: ",n)

#Generacion del filtro

z,p,k= sig.cheb1ap(n, alfa_max)

num,den= sig.zpk2tf(z,p,k)

my_tf= sig.TransferFunction(num,den)

plt.close('all')
tc2.analyze_sys(my_tf, sys_name="Filtro Cheby")

"""
En este punto, si la simulacion salio bien de acuerdo a la plantilla, puedo
pasar a la implementacion circuital
"""

#Esto me devuelve numerador y denominador de las distintas secciones
#que componen el filtro

sos= tc2.tf2sos_analog(num,den)
print(sos)



















    