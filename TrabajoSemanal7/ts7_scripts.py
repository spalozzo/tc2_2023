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

def mod_phase_h(h):

    mod= np.abs(h)
    phase= np.angle(h)
    
    return mod, phase;

def bodeCompareAnalogDigital(wa, h_analog, wd, h_digital, numfig):
    
    fig_bode= plt.figure(numfig)
    ax_mod, ax_phase= fig_bode.subplots(2, 1, sharex=True)

    mod_a, phase_a= mod_phase_h(h_analog)
    mod_d, phase_d= mod_phase_h(h_digital)   

    fig_bode.sca(ax_mod)
    ax_mod.plot(wd,20*np.log10(mod_d), label='Butter Digital N=2')
    ax_mod.plot(wa,20*np.log10(mod_a), label='Butter Analogico N=2',linestyle='--')
    plt.legend()
    plt.grid()
    plt.ylabel('Magnitude [dB]')
    plt.title('Magnitude response')

    fig_bode.sca(ax_phase)
    ax_phase.plot(wd,phase_d, label='Butter Digital N=2')
    ax_phase.plot(wa,phase_a, label='Butter Analogico N=2',linestyle='--')
    plt.legend()
    plt.grid()
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase [rad]')
    plt.title('Phase response')

    plt.show()
    
    return 0;


plt.close("all")

n= 2
fc= 1000
norma_fc= 1
fc_norm= fc/norma_fc
fs= 100e3
freq= np.linspace(0, 3e3, 1000)

# Genero el filtro Butter analogico

num_butt, den_butt= sig.butter(2, fc_norm, btype="low", analog=True)
tf_analog_butter= sig.TransferFunction(num_butt, den_butt)
tc2.pretty_print_lti(num_butt, den_butt)
#tc2.analyze_sys(tf_analog_butter, sys_name="Pasabajo Butter n=2")

wa, ha= sig.freqs(num_butt, den_butt, worN= freq)
mod_a= np.abs(ha)
phase_a= np.angle(ha)

#### Butter Digital

# Parametros
w0= 2*np.pi*fc_norm
k= 2*fs
Q= 1/np.sqrt(2)

# Filtro
num_butt_digital= [w0**2, 2 * w0**2, w0**2]
den_butt_digital= [k**2+(k*w0/Q)+w0**2, (2*w0**2)-(2*k**2), k**2-(k*w0/Q)+w0**2]

tf_digital_butter= sig.TransferFunction(num_butt_digital, den_butt_digital)
tc2.pretty_print_lti(num_butt_digital, den_butt_digital)


wd,hd= sig.freqz(num_butt_digital, den_butt_digital, worN= freq, fs=fs)

# mod_d= np.abs(hd)
# phase_d= np.angle(hd)

# fig_bode= plt.figure(1)
# ax_mod, ax_phase= fig_bode.subplots(2, 1, sharex=True)


# fig_bode.sca(ax_mod)
# ax_mod.plot(wd,20*np.log10(mod_d), label='Butter Digital N=2')
# ax_mod.plot(wa,20*np.log10(mod_a), label='Butter Analogico N=2',linestyle='--')
# plt.legend()
# plt.grid()
# plt.ylabel('Magnitude [dB]')
# plt.title('Magnitude response')

# fig_bode.sca(ax_phase)
# ax_phase.plot(wd,phase_d, label='Butter Digital N=2')
# ax_phase.plot(wa,phase_a, label='Butter Analogico N=2',linestyle='--')
# plt.legend()
# plt.grid()
# plt.xlabel('Angular frequency [rad/sec]')
# plt.ylabel('Phase [rad]')
# plt.title('Phase response')

# plt.show()

bodeCompareAnalogDigital(wa, ha, wd, hd, 1)

############################################################################

# num_butt_hp, den_butt_hp= sig.butter(2, fc_norm, btype="high", analog=True)
# tf_analog_butter_hp= sig.TransferFunction(num_butt_hp, den_butt_hp)
# tc2.pretty_print_lti(num_butt_hp, den_butt_hp)
# #tc2.analyze_sys(tf_analog_butter, sys_name="Pasabajo Butter n=2")

# wa_hp, ha_hp= sig.freqs(num_butt_hp, den_butt_hp, worN= freq)
# mod_a= np.abs(ha_hp)
# phase_a= np.angle(ha_hp)

# #### Butter Digital

# # Parametros
# w0= 2*np.pi*fc_norm
# k= 2*fs
# Q= 1/np.sqrt(2)

# # Filtro
# num_butt_digital= [w0**2, 2 * w0**2, w0**2]
# den_butt_digital= [k**2+(k*w0/Q)+w0**2, (2*w0**2)-(2*k**2), k**2-(k*w0/Q)+w0**2]

# tf_digital_butter= sig.TransferFunction(num_butt_digital, den_butt_digital)
# tc2.pretty_print_lti(num_butt_digital, den_butt_digital)


# wd,hd= sig.freqz(num_butt_digital, den_butt_digital, worN= freq, fs=fs)

# mod_d= np.abs(hd)
# phase_d= np.angle(hd)

# fig_bode= plt.figure(1)
# ax_mod, ax_phase= fig_bode.subplots(2, 1, sharex=True)


# fig_bode.sca(ax_mod)
# ax_mod.plot(wd,20*np.log10(mod_d), label='Butter Digital N=2')
# ax_mod.plot(wa,20*np.log10(mod_a), label='Butter Analogico N=2',linestyle='--')
# plt.legend()
# plt.grid()
# plt.ylabel('Magnitude [dB]')
# plt.title('Magnitude response')

# fig_bode.sca(ax_phase)
# ax_phase.plot(wd,phase_d, label='Butter Digital N=2')
# ax_phase.plot(wa,phase_a, label='Butter Analogico N=2',linestyle='--')
# plt.legend()
# plt.grid()
# plt.xlabel('Angular frequency [rad/sec]')
# plt.ylabel('Phase [rad]')
# plt.title('Phase response')

# plt.show()

