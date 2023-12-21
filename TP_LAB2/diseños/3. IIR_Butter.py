#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 9:31:58 2023

@author: Santiago Palozzo
"""

# Módulos importantantes
import scipy.signal as sig
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.io as sio
import pytc2.sistemas_lineales as tc2

#Cositas para plotear
fig_sz_x = 10
fig_sz_y = 7
fig_dpi = 100 # dpi

fig_font_size = 16

mpl.rcParams['figure.figsize'] = (fig_sz_x,fig_sz_y)
plt.rcParams.update({'font.size':fig_font_size})

#####################################################################
def plot_fir_plantilla(frecs,ripple,attenuation,fs):
    plt.title('Filtros diseñados')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Módulo [dB]')
    plt.grid()
    plt.axis([0, 10000, -60, 5 ]);

    axes_hdl = plt.gca()
    axes_hdl.legend()


    tc2.plot_plantilla(filter_type = 'lowpass', fpass = frecs[1], ripple = ripple , fstop = frecs[2], attenuation = atenuacion, fs = fs)
#####################################################################

plt.close("all")


fs = 44100.0 # Hz
nyq_frec = fs / 2

# Filter Design
ripple = 1 # dB
atenuacion = 20 # dB

wp1 = 2000 #Hz
ws1 = 3000 #Hz


frecs = np.array([0.0,         wp1,         ws1,         nyq_frec   ])# / nyq_frec
gains = np.array([-ripple, -ripple, -atenuacion, -atenuacion])
gains = 10**(gains/20)
###

freq_ax= 10000

numtaps= 201

iir_butter = sig.iirdesign(wp1, ws1, ripple, atenuacion, ftype='butter', output='sos', fs=fs)
w_iir, h_iir= sig.sosfreqz(iir_butter, worN=10000, fs=fs)

####################################################################################################
###    La salida tiene que ser SOS porque la plantilla es muy exigente entonces requiere una     ###
###    alta recursividad del IIR. Python simplemente no llega a hcer bien los calculos debido    ###
###    a la exigencia de los mismos entonces una salida como numerador y denominador tira        ###
###    cualquier cosa.                                                                           ###
####################################################################################################

plt.figure(1)

plt.plot(w_iir, 20*np.log10(abs(h_iir)),label='IIR Butterworth')
plot_fir_plantilla(frecs,ripple,atenuacion,fs)

### Corrijo las ganancias de las distintas etapas para que sean parejas
#Debo prestar atencion a que los coeficientes que multiplican las SOS se cancelen
#### --> -6 +2 +2 +2 = 0
iir_np= np.array(iir_butter)

iir_np[0,[0,1,2]]= iir_np[0,[0,1,2]] * 10**6
iir_np[0,3]= 1

iir_np[1,[0,1,2]]= iir_np[1,[0,1,2]] * 10**-2
iir_np[1,3]= 1

iir_np[2,[0,1,2]]= iir_np[2,[0,1,2]] * 10**-2
iir_np[2,3]= 1

iir_np[3,[0,1,2]]= iir_np[3,[0,1,2]] * 10**-2
iir_np[3,3]= 1

#### Ploteo cada SOS por separado

for i in [2,3,4,5]:
    
    index= i-2
    
    w_iir, h_iir= sig.sosfreqz(iir_np[index,:], worN=10000, fs=fs)

    plt.figure(i)
    
    plt.plot(w_iir, 20*np.log10(abs(h_iir)),label='IIR Butterworth SOS{:d}'.format(i-1))
    plot_fir_plantilla(frecs,ripple,atenuacion,fs)


### Ploteo el filtro con las ganancias modificadas
w_iir, h_iir= sig.sosfreqz(iir_np, worN=10000, fs=fs)

plt.figure(6)

plt.plot(w_iir, 20*np.log10(abs(h_iir)),label='IIR Butterworth Resultante')
plot_fir_plantilla(frecs,ripple,atenuacion,fs)





