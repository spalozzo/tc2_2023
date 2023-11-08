# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 13:02:58 2023

@author: Santi Palozzo
"""
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

from pytc2.general import print_latex, print_subtitle, a_equal_b_latex_s
from pytc2.remociones import remover_valor, remover_polo_sigma, remover_polo_infinito

from pytc2.dibujar import display, dibujar_puerto_entrada, dibujar_funcion_exc_abajo,  dibujar_elemento_serie
from pytc2.dibujar import dibujar_elemento_derivacion, Drawing, Resistor, dibujar_tanque_RC_derivacion, Line
from pytc2.dibujar import dibujar_espacio_derivacion, Line

plt.close('all')

# Simulación simbólica
s = sp.symbols('s ', complex=True)

# Sea la siguiente función de excitación
Z1 = (s**2 + 6*s + 8)/(s**2 + 4*s + 3)

# Datos del ejercicio
sigma1 = 6
sigma2 = sp.Rational('7/2')

# Remociones   
Z2, Ra = remover_valor(Z1, sigma_zero = sigma1) # Remocion parcial - R en serie
Y4, Y3, R1, C1 = remover_polo_sigma(1/Z2, sigma1, isImpedance = False)  # Remocion finita - RC en paralelo
Z6, Rb = remover_valor(1/Y4, sigma_zero = sigma2) # Remocion parcial - R en serie
Y8, Y7, R2, C2 = remover_polo_sigma(1/Z6, sigma2, isImpedance = False) # Remocion finita - RC en paralelo
Rc = 1/Y8 # Residuo final - R en paralelo

# Dibujo la red
circuito = Drawing(unit=4)
circuito = dibujar_puerto_entrada(circuito,voltage_lbl = ('Vi'), current_lbl = 'I')
circuito, zz_lbl = dibujar_funcion_exc_abajo(circuito, 
                                          'Z(s)',  
                                          Z1, 
                                          hacia_salida = True,
                                          k_gap_width = 0.5)
circuito = dibujar_elemento_serie(circuito, Resistor, Ra)
circuito = dibujar_tanque_RC_derivacion(circuito, R1, C1)
circuito = dibujar_elemento_serie(circuito, Resistor, Rb)
circuito = dibujar_tanque_RC_derivacion(circuito, R2, C2)
# circuito = dibujar_elemento_serie(circuito, Resistor, Rc)
# circuito = dibujar_elemento_derivacion(circuito, Line)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_elemento_derivacion(circuito, Resistor, Rc)

display(circuito)   








