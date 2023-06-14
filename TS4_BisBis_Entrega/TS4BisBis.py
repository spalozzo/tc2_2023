from scipy.signal import TransferFunction
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from pytc2.sistemas_lineales import analyze_sys, pretty_print_bicuad_omegayq, tf2sos_analog, pretty_print_SOS


#----------------------Definicion de las variables---------------------

xi = 0.35
n = 3
rp = 0.5

#---------------------------Definicion de HLP--------------------------

[zLP, pLP, kLP] = ss.cheb1ap(n, rp)

[numLP, denLP] = ss.zpk2tf(zLP, pLP, kLP)

LP_sos = tf2sos_analog(numLP, denLP)

HLP = TransferFunction(numLP, denLP)

#-------------------------Transformación LP-BP-------------------------

[numBP, denBP] = ss.lp2bp(numLP, denLP, 1, 1/5)

[zBP, pBP, kBP] = ss.tf2zpk(numBP, denBP)

BP_sos = tf2sos_analog(numBP, denBP)

HBP = TransferFunction(numBP, denBP)

#-----------------------------Visualizacion----------------------------

# -------- LP --------
print("HLP(s): ")
pretty_print_SOS(LP_sos, mode='omegayq')
print("zLP = ", zLP, "\n", "pLP = ", pLP, "\n", "kLP =", kLP)
analyze_sys(HLP, "Cheby LP")

# -------- BP --------
print("HBP(s): ")
pretty_print_SOS(BP_sos, mode='omegayq')
print("zBP = ", zBP, "\n", "pBP = ", pBP, "\n", "kBP =", kBP)
analyze_sys(HBP, "Cheby BP", same_figs=False)
  
