import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
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

    plt.plot(X,e_Knots,antialiased=True)
    plt.ylabel("Beam Energy (MeV)")
    plt.xlabel("Range (cm)")

    return spline


def beamRangeToEnergy(func,E,r):
    """ Given an initial beam energy 'E', integrate its energy loss curve
    'func' out to a certain range 'r'. Return the energy (MeV) for a given
    range (cm) """

    energy = E - func.integrate(0,r)

    return energy





# Read in SRIM data
pt10C = PowerTable("Tables/EnergyTable/10C_HeCO2_400_Torr.txt")
pt11B = PowerTable("Tables/EnergyTable/11B_HeCO2_400_Torr.txt")
pt10B = PowerTable("Tables/EnergyTable/10B_HeCO2_400_Torr.txt")
pt7Be = PowerTable("Tables/EnergyTable/7Be_HeCO2_400_Torr.txt")


# Spline of Energy as function of range
# Second parameter is max energy (MeV) that is stopped (from SRIM), comment is max Range

spline_10C_Beam = beamEnergyLoss(pt10C,35) # 37.842 cm
spline_10B_Beam = beamEnergyLoss(pt10B,30) # 41.590 cm
spline_11B_Beam = beamEnergyLoss(pt11B,30) # 39.929 cm
spline_7Be_Beam = beamEnergyLoss(pt7Be,40) # 117 cm
plt.legend(('$^{10}C$','$^{10}B$','$^{11}B$','$^{7}Be$'))
plt.savefig("plots/energyVsRange.pdf")
plt.show()

# Beam energies
ebeam_10C = 35
ebeam_10B = 25
ebeam_11B = 26.4
ebeam_7Be = 24


# SAMPLE CALCULATION
# Energy (MeV) at range r (cm)
r = 10
eVertex_10C = beamRangeToEnergy(spline_10C_Beam,ebeam_10C,r)
eVertex_10B = beamRangeToEnergy(spline_10B_Beam,ebeam_10B,r)
eVertex_11B = beamRangeToEnergy(spline_11B_Beam,ebeam_11B,r)
eVertex_7Be = beamRangeToEnergy(spline_7Be_Beam,ebeam_7Be,r)

print(eVertex_10B)
