#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 10:51:58 2023

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

def bodePlotDigitalBP(system, fpass, fstop, freq, fs, xlim=False, ylim=False, numfig=None, sos=True):
    
    if(sos):
        wd,hd= sig.sosfreqz(system, worN=freq, fs=fs)
        wdelay, gdelay= sig.group_delay(sig.sos2tf(system),fs=fs)
    else:
        wd,hd= sig.freqz(system[0], system[1], worN=freq, fs=fs)
        wdelay, gdelay= sig.group_delay(system, w=freq ,fs=fs)
            
    
    fig_bode= plt.figure(numfig)
    ax_mod, ax_phase, ax_delay= fig_bode.subplots(3, 1, sharex=True)

    mod_d, phase_d= mod_phase_h(hd)   
    
    mod_d[0]= 0.00001

    # MODULE
    fig_bode.sca(ax_mod)
    ax_mod.plot(wd,20*np.log10(mod_d), label='FIR')
    ax_mod.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    plt.xlim(fstop[0]/2, fstop[1]*3/2)
    plt.ylim(-60, 10)
    plt.ylabel('Magnitude [dB]')
    plt.title('Magnitude response')
    
    for f in fpass:
        plotFreqLine(f, 'green')
    
    for f in fstop:
        plotFreqLine(f, 'red')
    
    # PHASE
    fig_bode.sca(ax_phase)
    ax_phase.plot(wd,phase_d, label='FIR')
    ax_phase.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    #plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase [rad]')
    plt.title('Phase response')
    
    # GROUP DELAY
    fig_bode.sca(ax_delay)
    ax_delay.plot(wdelay,gdelay, label='FIR')
    ax_delay.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    # plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Group Delay [samples]')
    plt.title('Group Delay') 
    
    plt.show()
    
    return 0;

def plotImpulseResponse(response):
    
    plt.figure()
    plt.plot(response, label='IIR')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Impulse Response')
    plt.title('Impulse Response')
    
    return

def plot_fir_plantilla(frecs,ripple,attenuation,fs):
    plt.title('Filtros diseñados')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Módulo [dB]')
    plt.grid()
    plt.axis([0, 10000, -60, 5 ]);

    axes_hdl = plt.gca()
    axes_hdl.legend()


    tc2.plot_plantilla(filter_type = 'bandstop', fpass = frecs[[1, 4]], ripple = ripple , fstop = frecs[ [2, 3] ], attenuation = atenuacion, fs = fs)
    

plt.close("all")


fs = 44100.0 # Hz
nyq_frec = fs / 2

# Filter Design
ripple = 0.1 # dB
atenuacion = 20 # dB

wp1 = 2000 #Hz
ws1 = 4000 #Hz
ws2 = 6000 #Hz
wp2 = 8000 #Hz

frecs = np.array([0.0,         wp1,         ws1,     ws2,     wp2,         nyq_frec   ])# / nyq_frec
gains = np.array([-ripple, -ripple, -atenuacion, -atenuacion,  -ripple, -ripple])
gains = 10**(gains/20)
###

### Diseño Filtro Digital
ws_array= np.array([ws1, ws2])
wp_array= np.array([wp1, wp2])

freq_ax= 10000

numtaps= 151
# Diseño filtro Band Reject
fir_firls= sig.firls(numtaps, frecs, gains, fs=fs) #No especifico fs porque ya paso las f normalizadas
den_br_fir= [1]


w_fir, h_fir= sig.freqz(fir_firls, worN=100000)

BR_system= [fir_firls, 1]
#bodePlotDigitalBP(BR_system, frecs[[1, 4]], frecs[[2, 3]], fs)

plt.plot(w_fir* nyq_frec/np.pi, 20*np.log10(abs(h_fir)),label='FIRLS-{:d}TAPS'.format(fir_firls.shape[0]))

plot_fir_plantilla(frecs,ripple,atenuacion,fs)


