# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 18:58:29 2023

@author: santi
"""

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

def plotDigitalFilter(mod,phase,numfig=1,limits=False,lines=False):
    fig_bode= plt.figure(numfig)
    ax_mod, ax_phase= fig_bode.subplots(2, 1, sharex=True)
    # MODULE
    fig_bode.sca(ax_mod)
    ax_mod.plot(wd,20*np.log10(mod), label='PasaTodo Digital N=2')
    ax_mod.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    if(limits):
        plt.ylim(-1,1)
    plt.ylabel('Magnitude [dB]')
    plt.title('Magnitude response')
    if(lines):
        plt.axvline(125, color='green', linestyle=':')
        plt.axvline(3*125, color='green', linestyle=':')

    # PHASE
    fig_bode.sca(ax_phase)
    ax_phase.plot(wd,phase, label='PasaTodo Digital N=2')
    ax_phase.set(xscale='log')
    plt.legend()
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase [rad]')
    plt.title('Phase response')
    if(lines):
        plt.axvline(125, color='green', linestyle=':')
        plt.axvline(3*125, color='green', linestyle=':')

    plt.show()

plt.close('all')

# Filtro
num1= [0.8, 0, 1]
den1= [1, 0, 0.8]

tf_digital= sig.TransferFunction(num1, den1)
print(tf_digital)

# freq= np.linspace(0.01, 10e4, 100000)
wd,hd= sig.freqz(num1, den1, fs=1)


mod1= np.abs(hd)
phase1= np.angle(hd)


plotDigitalFilter(mod1,phase1,limits=True)

num2= [1.8, 0, 0, 0, 1.8]
den2= [1.0, 0, 0, 0, 0.8]

tf_digital2= sig.TransferFunction(num2, den2)
print(tf_digital2)

# freq= np.linspace(0.01, 10e4, 100000)
wd,hd= sig.freqz(num2, den2, fs=8*125)


mod2= np.abs(hd)
phase2= np.angle(hd)

plotDigitalFilter(mod2,phase2,2,lines=True)
plt.figure(2)



