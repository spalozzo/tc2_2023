# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 13:02:58 2023

@author: Santi Palozzo
"""
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


from pytc2.general import print_latex, print_subtitle, a_equal_b_latex_s
from pytc2.remociones import remover_polo_dc, remover_polo_jw, remover_polo_infinito

from pytc2.dibujar import display, dibujar_puerto_entrada, dibujar_funcion_exc_abajo, dibujar_puerto_salida
from pytc2.dibujar import dibujar_elemento_serie, dibujar_elemento_derivacion, Drawing
from pytc2.dibujar import Inductor, Capacitor, dibujar_tanque_derivacion, dibujar_espacio_derivacion

plt.close('all')

# Simulación simbólica
s = sp.symbols('s ', complex=True)

# Sea la siguiente función transferencia
Y11 = 3*s * (s**2 + sp.Rational('7/3'))/(s**2 + 2)/(s**2 + 5)

Z1 = 1/Y11

# Remociones
Z2, kL1 = remover_polo_infinito(Z1) # Remocion en infinito - L en serie
L1 = kL1 / s

Z2_2, kC1 = remover_polo_dc(Z2, omega_zero = 1 ) # Remocion parcial - C en serie
C1= kC1 * s
Y2 = 1/Z2_2

Y4, YLC, L2, C2 = remover_polo_jw(Y2, 1 , isImpedance = False)  # Remocion finita - RC en paralelo

C3= Y4 / s
# Y4 es la admitancia final, un C en paralelo

# Dibujo la red
circuito = Drawing(unit=4)
circuito = dibujar_puerto_entrada(circuito,voltage_lbl = ('V1'), current_lbl = 'I1')
circuito, zz_lbl = dibujar_funcion_exc_abajo(circuito, 'Y11(s)', Y11, hacia_salida = True, k_gap_width=0.5)
circuito = dibujar_elemento_serie(circuito, Inductor, L1)
circuito = dibujar_elemento_serie(circuito, Capacitor, C1)
circuito = dibujar_tanque_derivacion(circuito, L2, C2)
circuito = dibujar_elemento_serie(circuito, Capacitor, C3)
circuito = dibujar_puerto_salida(circuito,voltage_lbl = ('V2'), current_lbl = 'I2')

display(circuito)  







