# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 09:09:08 2023

@author: Santi
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

#from splane import plot_plantilla

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
    


plt.close("all")


fs = 44100.0 # Hz
nyq_frec = fs / 2

# Filter Design
ripple = 0.1 # dB
atenuacion = 20 # dB

wp1 = 1000 #Hz
ws1 = 2000 #Hz


frecs = np.array([0.0,         wp1,         ws1,         nyq_frec   ])# / nyq_frec
gains = np.array([-ripple, -ripple, -atenuacion, -atenuacion])
gains = 10**(gains/20)
###

### Diseño Filtro Digital
#ws_array= np.array([ws1, ws2])
#wp_array= np.array([wp1, wp2])

freq_ax= 10000

numtaps= 201
# Diseño filtro Band Reject
fir_equiripple= sig.remez(numtaps, frecs, gains[[1,2]], fs=fs) #No especifico fs porque ya paso las f normalizadas
den_br_fir= [1]


w_fir, h_fir= sig.freqz(fir_equiripple, worN=100000)

BR_system= [fir_equiripple, 1]
#bodePlotDigitalBP(BR_system, frecs[[1, 4]], frecs[[2, 3]], fs)

plt.plot(w_fir* nyq_frec/np.pi, 20*np.log10(abs(h_fir)),label='FIR Equiripple-{:d}TAPS'.format(fir_equiripple.shape[0]))

plot_fir_plantilla(frecs,ripple,atenuacion,fs)