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
    plt.axis([0, 100, -60, 5 ]);

    axes_hdl = plt.gca()
    axes_hdl.legend()


    tc2.plot_plantilla(filter_type = 'bandpass', fpass = frecs[[2, 3]]* nyq_frec, ripple = ripple , fstop = frecs[ [1, 4] ]* nyq_frec, attenuation = atenuacion, fs = fs)
    

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
ripple = 0 # dB
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

# freq_ax= np.linspace(0, 1, 100000)
freq_ax= 10000

# bp_sos = sig.iirdesign(wp_array, ws_array, ripple, atenuacion,ftype='butter', output='sos', fs=fs)

Ntaps= 1501

num_bp_fir= sig.firwin2(Ntaps, frecs, gains, window='blackmanharris')
den_bp_fir= [1]

# w  = np.append(np.logspace(-1, 0.8, 250), np.logspace(0.9, 1.6, 250) )
# w  = np.append(w, np.linspace(110, nyq_frec, 100, endpoint=True) ) / nyq_frec * np.pi

w_fir, h_fir= sig.freqz(num_bp_fir, den_bp_fir, freq_ax)

# w = w / np.pi * nyq_frec

plt.plot(w_fir/np.pi * nyq_frec, 20 * np.log10(abs(h_fir)), label='FIR-Win {:d}'.format(num_bp_fir.shape[0]))

plot_fir_plantilla(frecs,ripple,atenuacion,fs)

##### Diseño del FIR como una cascada de pasa altos + pasa bajos 

## PASA ALTOS ##
Ntaps= 3501

frecs_hp = np.array([0.0,         ws1,         wp1,         nyq_frec   ]) / nyq_frec
gains_hp = np.array([-atenuacion, -atenuacion, -ripple, -atenuacion])
gains_hp = 10**(gains_hp/20)

num_hp_fir= sig.firwin2(Ntaps, frecs_hp, gains_hp, window='blackmanharris')
den_hp_fir= [1]

w_fir_hp, h_fir_hp= sig.freqz(num_hp_fir, den_hp_fir, freq_ax)


plt.figure(2)
plt.plot(w_fir_hp/np.pi * nyq_frec, 20 * np.log10(abs(h_fir_hp)), label='FIR-Win {:d}'.format(num_hp_fir.shape[0]))
plot_fir_plantilla(frecs,ripple,atenuacion,fs)


## PASA BAJOS ##
Ntaps= 3501

frecs_lp = np.array([0.0,         wp2,         ws2,         nyq_frec   ]) / nyq_frec
gains_lp = np.array([-ripple, -ripple, -atenuacion, -atenuacion])
gains_lp = 10**(gains_lp/20)

num_lp_fir= sig.firwin2(Ntaps, frecs_lp, gains_lp, window='blackmanharris')
den_lp_fir= [1]

w_fir_lp, h_fir_lp= sig.freqz(num_lp_fir, den_lp_fir, freq_ax)

plt.figure(3)
plt.plot(w_fir_lp/np.pi * nyq_frec, 20 * np.log10(abs(h_fir_lp)), label='FIR-Win {:d}'.format(num_lp_fir.shape[0]))
plot_fir_plantilla(frecs,ripple,atenuacion,fs)

num_bp_fir2= np.polymul(num_hp_fir, num_lp_fir)
den_bp_fir2= [1]

w_fir_bp2, h_fir_bp2= sig.freqz(num_bp_fir2, den_bp_fir2, freq_ax)

plt.figure(4)
plt.plot(w_fir_bp2/np.pi * nyq_frec, 20 * np.log10(abs(h_fir_bp2)), label='FIR-Win {:d}'.format(num_bp_fir2.shape[0]))
plot_fir_plantilla(frecs,ripple,atenuacion,fs)


bodePlotDigitalBP([num_bp_fir2,den_bp_fir2], wp_array, ws_array, freq_ax, fs, sos=False)

impulse= sig.unit_impulse(freq_ax)
impulse_response= sig.lfilter(num_bp_fir2, den_bp_fir2, impulse)
plotImpulseResponse(impulse_response)







