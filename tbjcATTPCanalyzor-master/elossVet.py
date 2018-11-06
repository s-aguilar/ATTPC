import json
import numpy as np
import pandas as pd
from kinematicsSolver import *
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import matplotlib.patches as patches
from matplotlib.colors import LogNorm
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d import Axes3D
from Analyzor.KINEMATICS.tbjcconstants import *
from Analyzor.KINEMATICS.KINEMATICS import KINEMATICS
from Analyzor.EnergyAndRangeConvertor import PowerTable
from Analyzor.KINEMATICS.AtomicMassTable import GetElement

# Constants
_c = 3.0e8
_U = 931.4940954 #MeV/c^2
_m4He = GetElement(2,4)[3]*_U
_m10B = GetElement(5,10)[3]*_U
_m11B = GetElement(5,11)[3]*_U
_m10C = GetElement(6,10)[3]*_U


def beamEnergyLoss(table,E):
    """ Returns the spline of the dE/dX for that beam species of the table """

    e_Knots = np.linspace(0,E,100)
    dXdE_E = table.dXdE(e_Knots)
    dEdX_E = table.dEdX(e_Knots)

    X = [0.]*len(e_Knots-1)
    step = len(e_Knots)-1-1

    # trapezoidal integration (b-a)*(f(b)+f(a))/2.
    while step >=0:
        trapezoid = X[step+1]+0.5*(e_Knots[step+1]-e_Knots[step]) * \
                    (dXdE_E[step+1]+dXdE_E[step])
        X[step] = trapezoid
        step -=1

    spline = CubicSpline(list(reversed(X)),list(reversed(dEdX_E)))
    # xs = np.linspace(0,37.85,1000)
    # plt.plot(xs,spline(xs),color='b')
    # plt.scatter(X,dEdX_E)
    # plt.ylabel("$\\frac{dE}{dX}$ (MeV/cm)")
    # plt.xlabel("X (cm)")
    # plt.savefig("eLoss.pdf",rasterized=True)
    # plt.show()
    # print(spline.integrate(0,37.85))
    #
    # plt.scatter(X,e_Knots)
    # plt.ylabel("Energy (MeV)")
    # plt.xlabel("Range (cm)")
    # plt.savefig("energyVsRange.pdf",rasterized=True)
    # plt.show()
    #
    # plt.scatter(e_Knots,X)
    # plt.xlabel("Energy (MeV)")
    # plt.ylabel("Range (cm)")
    # plt.savefig("rangeVsEnergy.pdf",rasterized=True)
    # plt.show()
    return spline


pt4He = PowerTable("/Users/sebastian/Desktop/ActiveTargetGroup/tbjcATTPCanalyzor-master/Tables/EnergyTable/He_HeCO2_400_Torr.txt")
pt10C = PowerTable("/Users/sebastian/Desktop/ActiveTargetGroup/tbjcATTPCanalyzor-master/Tables/EnergyTable/10C_HeCO2_400_Torr.txt")
pt11B = PowerTable("/Users/sebastian/Desktop/ActiveTargetGroup/tbjcATTPCanalyzor-master/Tables/EnergyTable/11B_HeCO2_400Torr.txt")
pt10B = PowerTable("/Users/sebastian/Desktop/ActiveTargetGroup/tbjcATTPCanalyzor-master/Tables/EnergyTable/10B_HeCO2_400_Torr.txt")

loss = beamEnergyLoss(pt10C,34)

# print(loss)
