#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 09:47:03 2023

Tarea Semanal 7: Filtros Digitales

@author: santi
"""

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import pytc2.sistemas_lineales as tc2

def gen_analog_butter(n, fc, btype, frequency_ax, print_tf=False):
    
    num_butt, den_butt= sig.butter(n, fc, btype, analog=True)
    tf_analog_butter= sig.TransferFunction(num_butt, den_butt)
    
    if print_tf:
        #tc2.pretty_print_lti(num_butt, den_butt)
        print(tf_analog_butter)

    wa, ha= sig.freqs(num_butt, den_butt, frequency_ax)
    
    tf_parameters= [tf_analog_butter, wa, ha]
    
    return tf_parameters

def mod_phase_h(h):

    mod= np.abs(h)
    phase= np.angle(h)
    
    return mod, phase;

def bodeCompareAnalogDigital(wa, h_analog, wd, h_digital, fc, numfig):
    
    fig_bode= plt.figure(numfig)
    ax_mod, ax_phase= fig_bode.subplots(2, 1, sharex=True)

    mod_a, phase_a= mod_phase_h(h_analog)
    mod_d, phase_d= mod_phase_h(h_digital)   

    # MODULE
    fig_bode.sca(ax_mod)
    ax_mod.plot(wd,20*np.log10(mod_d), label='Butter Digital N=2')
    ax_mod.plot(wa,20*np.log10(mod_a), label='Butter Analogico N=2',linestyle='--')
    ax_mod.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    plt.ylabel('Magnitude [dB]')
    plt.title('Magnitude response')
    plt.axvline(fc, color='green', linestyle='--') # cutoff frequency
    
    # PHASE
    fig_bode.sca(ax_phase)
    ax_phase.plot(wd,phase_d, label='Butter Digital N=2')
    ax_phase.plot(wa,phase_a, label='Butter Analogico N=2',linestyle='--')
    ax_phase.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase [rad]')
    plt.title('Phase response')
    plt.axvline(fc, color='green', linestyle='--') # cutoff frequency
    
    plt.show()
    
    return 0;


plt.close("all")

n= 2
fc= 1000
norma_fc= 1
fc_norm= fc/norma_fc
fs= 100e3
freq_lp= np.linspace(fc_norm/(10), fc_norm*10, 100000)

# Genero el filtro Butter analogico

analog_butter_lp= gen_analog_butter(n, fc_norm, "low", freq_lp)

#### Butter Digital

# Parametros
w0= 2*np.pi*fc_norm
k_comun= 2*fs
f_prewarp= 1000
k_prewarp= np.pi*f_prewarp/np.tan(np.pi*f_prewarp/fs)
k= k_comun
Q= 1/np.sqrt(2)

# Filtro
num_butt_digital= [w0**2, 2 * w0**2, w0**2]
den_butt_digital= [k**2+(k*w0/Q)+w0**2, (2*w0**2)-(2*k**2), k**2-(k*w0/Q)+w0**2]

tf_digital_butter= sig.TransferFunction(num_butt_digital, den_butt_digital)
#tc2.pretty_print_lti(num_butt_digital, den_butt_digital)
wd,hd= sig.freqz(num_butt_digital, den_butt_digital, worN= freq_lp, fs=fs)


bodeCompareAnalogDigital(analog_butter_lp[1], analog_butter_lp[2], wd, hd, fc= fc_norm, numfig= 1)

########################### BUTTER PASAALTOS ##################################

fc_hp= 6e3
norma_hp= 1
fc_norm_hp= fc_hp/norma_hp
freq_hp= np.linspace(fc_norm_hp/10, fc_norm_hp*10, 100000)

# Genero el filtro Butter analogico
analog_butter_hp= gen_analog_butter(n, fc_norm_hp, "high", freq_hp, True)


#### Butter Digital
# Parametros
w0= 2*np.pi*fc_norm_hp
k= 2*fs
Q= 1/np.sqrt(2)

# Filtro
num_butt_digital= [k**2, -2 * k**2, k**2]
den_butt_digital= [k**2+(k*w0/Q)+w0**2, (2*w0**2)-(2*k**2), k**2-(k*w0/Q)+w0**2]

# num_butt_digital, den_butt_digital= sig.butter(2, fc_norm_hp, btype='high', fs=fs)

tf_digital_butter= sig.TransferFunction(num_butt_digital, den_butt_digital)
#tc2.pretty_print_lti(num_butt_digital, den_butt_digital)
wd,hd= sig.freqz(num_butt_digital, den_butt_digital, worN= freq_hp, fs=fs)

bodeCompareAnalogDigital(analog_butter_hp[1], analog_butter_hp[2], wd, hd, fc= fc_norm_hp, numfig= 2)


####################### BUTTER DIGITAL CON PYTHON #############################








