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

from pytc2.dibujar import display, dibujar_puerto_entrada, dibujar_puerto_salida, dibujar_funcion_exc_abajo
from pytc2.dibujar import dibujar_elemento_serie, dibujar_elemento_derivacion, Drawing
from pytc2.dibujar import Resistor, Capacitor, dibujar_tanque_RC_serie, dibujar_espacio_derivacion

plt.close('all')

# Simulación simbólica
s = sp.symbols('s ', complex=True)

# Sea la siguiente función excitacion
Y22 = (s + 2)*(s + 4)/(s + 3)


# Remociones   
Y4, kC2 = remover_polo_infinito(Y22) # Remocion en infinito - C en paralelo
C2 = kC2 / s

Y6, G2 = remover_valor(Y4, sigma_zero = 1) # Remocion parcial - R en paralelo

R0, ZRC, R1, C1 = remover_polo_sigma(1/Y6, 1, isImpedance = True)  # Remocion finita - RC en serie

# R0 es el residuo final, una R en serie

# Dibujo la red
circuito = Drawing(unit=4)
circuito = dibujar_puerto_entrada(circuito,voltage_lbl = ('V1'), current_lbl = 'I1')

circuito = dibujar_elemento_serie(circuito, Resistor, R0)
circuito = dibujar_tanque_RC_serie(circuito, R1, C1)
circuito = dibujar_elemento_derivacion(circuito, Resistor, 1/G2)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_elemento_derivacion(circuito, Capacitor, C2)

circuito, zz_lbl = dibujar_funcion_exc_abajo(circuito, 'Y22(s)', Y22, hacia_entrada = True, k_gap_width=0.5)
circuito = dibujar_puerto_salida(circuito,voltage_lbl = ('V2'), current_lbl = 'I2')

display(circuito)   

###############################################################################
# Sintesis mediante impedancia Z11

# Sea la siguiente función excitacion
Z11 = (s + 2)*(s + 4)/s/(s + 3)


# Remociones   
Y4, kC2 = remover_polo_infinito(Y22) # Remocion en infinito - C en paralelo
C2 = kC2 / s

Y6, G2 = remover_valor(Y4, sigma_zero = 1) # Remocion parcial - R en paralelo

R0, ZRC, R1, C1 = remover_polo_sigma(1/Y6, 1, isImpedance = True)  # Remocion finita - RC en serie

# R0 es el residuo final, una R en serie


circuito = Drawing(unit=4)
circuito = dibujar_puerto_entrada(circuito,voltage_lbl = ('V1'), current_lbl = 'I1')

circuito = dibujar_elemento_serie(circuito, Resistor, R0)
circuito = dibujar_tanque_RC_serie(circuito, R1, C1)
circuito = dibujar_elemento_derivacion(circuito, Resistor, 1/G2)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_espacio_derivacion(circuito)
circuito = dibujar_elemento_derivacion(circuito, Capacitor, C2)

circuito, zz_lbl = dibujar_funcion_exc_abajo(circuito, 'Y22(s)', Y22, hacia_entrada = True, k_gap_width=0.5)
circuito = dibujar_puerto_salida(circuito,voltage_lbl = ('V2'), current_lbl = 'I2')
display(circuito)







