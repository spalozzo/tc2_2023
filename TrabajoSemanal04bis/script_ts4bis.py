#%% Inicializacion de librerias
# Librerías externas NumPy, SciPy y Matplotlib
import scipy.signal as sig
import matplotlib.pyplot as plt
import numpy as np

# Librería de TC2
import pytc2.sistemas_lineales as tc2

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
print("\n Prototipo pasabajos Butterworth")
tc2.pretty_print_lti(num_lp, den_lp)

num_bp, den_bp= sig.lp2bp(num_lp, den_lp, bw = 1/Q_bp)
print("\n Transferencia pasabanda")
tc2.pretty_print_lti(num_bp, den_bp)

## Muestro la transferencia BP en secciones de 2do orden
print("\n Transferencia pasabanda factorizada en SOS")
sos_bp = tc2.tf2sos_analog(num_bp, den_bp)
tc2.pretty_print_SOS(sos_bp)

tf_bp =  sig.TransferFunction(num_bp, den_bp)
tc2.analyze_sys(tf_bp, sys_name='Pasabanda 2do orden')