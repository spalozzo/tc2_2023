# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 13:02:58 2023

@author: Santi Palozzo
"""
# Librerías externas NumPy, SymPy y Matplotlib
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Librería de TC2
from pytc2.general import print_latex, print_subtitle, a_equal_b_latex_s
from pytc2.remociones import remover_valor, remover_polo_sigma, remover_polo_infinito

from pytc2.dibujar import display, dibujar_puerto_entrada, dibujar_funcion_exc_abajo,  dibujar_elemento_serie
from pytc2.dibujar import dibujar_elemento_derivacion, Drawing, Resistor, dibujar_tanque_RC_derivacion, Line
from pytc2.dibujar import dibujar_espacio_derivacion, Capacitor, Inductor

plt.close('all')

# Simulación simbólica
s = sp.symbols('s ', complex=True)

# Sea la siguiente función de excitación
Z1 = (s**2 + s + 1)/(s**2 + 2*s + 5)/(s + 1)

# Datos del ejercicio
sigma1 = 6
sigma2 = sp.Rational('7/2')

# Remociones
# Primer parametro cuadripolo sobrante, segundo parametro elemento removido

# Remuevo un capacitor en k_inf
Y2, kC1 = remover_polo_infinito(1/Z1)
C1 = kC1/s # Me quedo con el valor del componente

# Analizo extremos reales de la funcion excitacion
G_inf = sp.limit(Y2, s, sp.oo)
G_0 = sp.limit(Y2, s, 0)
# Remuevo la menor admitancia
R1 = 1/np.min((G_inf, G_0))
Y4 = Y2 - 1/R1

# Remuevo un inductor en k_inf
Z6, kL1 = remover_polo_infinito(1/Y4)
L1 = kL1/s # Me quedo con el valor del componente

# Analizo extremos reales de la funcion excitacion
R_inf = sp.limit(Z6, s, sp.oo)
R_0 = sp.limit(Z6, s, 0)
# Remuevo la menor resistencia
R2 = np.min((R_inf, R_0))
Z8 = Z6 - R2

# Remuevo un capacitor en k_inf
Y10, kC2 = remover_polo_infinito(1/Z8)
C2 = kC2/s # Me quedo con el valor del componente

# El residuo final es una R en paralelo
R3 = 1/Y10

# Dibujo la red
circuito = Drawing(unit=4)
circuito = dibujar_puerto_entrada(circuito, voltage_lbl = ('V'), current_lbl = 'I')
circuito, zz_lbl = dibujar_funcion_exc_abajo(circuito, 'Z', Z1, hacia_salida = True, k_gap_width = 0.5)
circuito = dibujar_elemento_derivacion(circuito, Capacitor, C1)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_elemento_derivacion(circuito, Resistor, R1)
circuito = dibujar_elemento_serie(circuito, Inductor, L1)
circuito = dibujar_elemento_serie(circuito, Resistor, R2)
circuito = dibujar_elemento_derivacion(circuito, Capacitor, C2)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_elemento_derivacion(circuito, Resistor, R3)
display(circuito) 








