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

#from splane import plot_plantilla

#####################################################################

def mod_phase_h(h):

    mod= np.abs(h)
    phase= np.angle(h)
    
    return mod, phase;

def plotFreqLine(f, color='black'):
    plt.axvline(f, color=color, linestyle='--') # cutoff frequency

def bodePlotDigitalBP(digital_sos, fpass, fstop, freq, fs, numfig):
    
    wd,hd= sig.sosfreqz(digital_sos, worN=freq, fs=fs)
    
    
    fig_bode= plt.figure(numfig)
    ax_mod, ax_phase= fig_bode.subplots(2, 1, sharex=True)

    mod_d, phase_d= mod_phase_h(hd)   

    # MODULE
    fig_bode.sca(ax_mod)
    ax_mod.plot(wd,20*np.log10(mod_d), label='Butter Digital N=2')
    ax_mod.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    plt.ylabel('Magnitude [dB]')
    plt.title('Magnitude response')
    
    for f in fpass:
        plotFreqLine(f, 'green')
    
    for f in fstop:
        plotFreqLine(f, 'red')
    
    # PHASE
    fig_bode.sca(ax_phase)
    ax_phase.plot(wd,phase_d, label='Butter Digital N=2')
    ax_phase.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase [rad]')
    plt.title('Phase response')
    
    plt.show()
    
    return 0;


plt.close("all")


###
## Señal de ECG registrada a 1 kHz, con contaminación de diversos orígenes.
###

# para listar las variables que hay en el archivo
#io.whosmat('ecg.mat')

mat_struct = sio.loadmat('ecg.mat')

ecg_one_lead = mat_struct['ecg_lead']
ecg_one_lead = ecg_one_lead.flatten()
cant_muestras = len(ecg_one_lead)

fs = 1000 # Hz
nyq_frec = fs / 2



# Plantilla

# filter design
ripple = 0.5 # dB
atenuacion = 40 # dB

ws1 = 1 #Hz
wp1 = 3.0 #Hz
wp2 = 25.0 #Hz
ws2 = 35.0 #Hz

frecs = np.array([0.0,         ws1,         wp1,     wp2,     ws2,         nyq_frec   ]) / nyq_frec
gains = np.array([-atenuacion, -atenuacion, -ripple, -ripple, -atenuacion, -atenuacion])
gains = 10**(gains/20)
###

### Diseño Filtro Digital
wp_array= np.array([wp1, wp2])
ws_array= np.array([ws1, ws2])
freq_ax= np.linspace(0, nyq_frec, 100000)

bp_sos = sig.iirdesign(wp_array, ws_array, ripple, atenuacion,ftype='butter', output='sos', fs=fs)
# bp_sos = sig.iirdesign(wp_array, ws_array, ripple, atenuacion,ftype='ellip', output='sos', fs=fs)
# bp_sos = sig.iirdesign(wp_array, ws_array, ripple, atenuacion,ftype='cheby1', output='sos', fs=fs)
# bp_sos = sig.iirdesign(wp_array, ws_array, ripple, atenuacion,ftype='cheby2', output='sos', fs=fs)

####################################################################################################
###    La salida tiene que ser SOS porque la plantilla es muy exigente entonces requiere una     ###
###    alta recursividad del IIR. Python simplemente no llega a hcer bien los calculos debido    ###
###    a la exigencia de los mismos entonces una salida como numerador y denominador tira        ###
###    cualquier cosa.                                                                           ###
####################################################################################################

#Si le paso como argumento fs, no necesito normalizar por nyquist en las frec de paso y corte
bodePlotDigitalBP(bp_sos, wp_array, ws_array, freq_ax, fs, 1)

# IIR
ECG_f_butt = sig.sosfilt(bp_sos, ecg_one_lead)

# demora = int(...)
# calcule la demora para cada caso, dicha demora adelantará la señal de salida, como puede ver más abajo.
demora = 0 #750

         
# Segmentos de interés con ALTA contaminación

regs_interes = ( 
        np.array([5, 5.2]) *60*fs, # minutos a muestras
        np.array([12, 12.4]) *60*fs, # minutos a muestras
        np.array([15, 15.2]) *60*fs, # minutos a muestras
        )

for ii in regs_interes:
    
    # intervalo limitado de 0 a cant_muestras
    zoom_region = np.arange(np.max([0, ii[0]]), np.min([cant_muestras, ii[1]]), dtype='uint')
    
    plt.figure(figsize=(fig_sz_x, fig_sz_y), dpi= fig_dpi, facecolor='w', edgecolor='k')
    plt.plot(zoom_region, ecg_one_lead[zoom_region], label='ECG', linewidth=2)
    #plt.plot(zoom_region, ECG_f_butt[zoom_region], label='Butter')
    plt.plot(zoom_region, ECG_f_butt[zoom_region + demora], label='Filtrado')
    
    plt.title('ECG filtering example from ' + str(ii[0]) + ' to ' + str(ii[1]) )
    plt.ylabel('Adimensional')
    plt.xlabel('Muestras (#)')
    
    axes_hdl = plt.gca()
    axes_hdl.legend()
    axes_hdl.set_yticks(())
            
    plt.show()











