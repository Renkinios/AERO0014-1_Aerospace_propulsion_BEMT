import numpy as np
from fit_data import *
class propeller_param : 
    def __init__(self,n,RPM,D,r_R_start) :
        """Class propeller :
        Parameters :
        - n : int : number of blades
        - root_cut_out : float : chord at the root radially
        """
        self.n = n                                   # number of blades [-]
        self.D = D                                   # diameter of the propeller [m]
        self.R = D/2                                 # radius of the propeller [m]
        self.RPM = RPM                               # rotation speed [rpm]
        self.RPS = RPM/60                            # rotation speed [rps]
        self.omega = self.RPS  * 2 * np.pi           # rotation speed [rad/s]
        self.r_R = 0                                 # matrix of radial position
        self.chord = 0                               # matrix of chord
        self.nb_elements = 0                         # number of elements
        self.stragger_1_75 = 0                       # (stagger - stragger(0.75)) [rad]
        self.collective_pitcth_0_75 = 0              # collective pitch at 0.75 radius [rad]


def propeller_clark_y() : 
    # -------------------------------------------------------------------------
    #  Propeller: Clark Y
    # -------------------------------------------------------------------------

    n = 3
    D =  10 * 0.3048 # feet to meters
    RPM = 800
    r_r_start = 0.2
    propeller = propeller_param(n, RPM,D,r_r_start)
    n_b_elems = 100
    propeller.nb_elements = n_b_elems
    r_R = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    b_D = np.array([0.0360, 0.0525, 0.0700, 0.0760, 0.0735, 0.0660, 0.0565, 0.0450])
    p_D = np.array([0.670, 0.840, 0.940, 0.980, 1.020, 1.090, 1.125, 1.190])
    propeller.r_R = np.linspace(np.min(r_R), 1, n_b_elems)
    propeller.chord = section_chord(b_D,r_R,n_b_elems,propeller.R)

    propeller.stragger_1_75 = data_pitch_angle(p_D,r_R,n_b_elems,propeller.R)

    return propeller


