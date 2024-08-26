from BEM import *
import numpy as np
import matplotlib.pyplot as plt
from propeller_parameters import *
from fit_data import *
from performance_caracteristique import *

def convergence():
    clark_y = propeller_clark_y()  # Assurez-vous que cette fonction est définie ailleurs dans votre code
    wind_speed = 90 * 0.44704  # Converti la vitesse du vent en m/s
    colective_pitch_0_75 = 25  # Angle de pas collectif à 75% du rayon
    clark_y.collective_pitcth_0_75 = np.radians(colective_pitch_0_75)  # Conversion en radians
    cl_interpolator,cd_interpolator = clarkypolarsRe_interppolation() # load the interpolator for the cl and cd
    # Définir les pas pour l'analyse de convergence
    element_steps = [10, 20 ,30,40,50, 75,100,200,300]
    relative_error = []
    
    
    r_R = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    b_D = np.array([0.0360, 0.0525, 0.0700, 0.0760, 0.0735, 0.0660, 0.0565, 0.0450])
    p_D = np.array([0.670, 0.840, 0.940, 0.980, 1.020, 1.090, 1.125, 1.190])

    clark_y.nb_elements = element_steps[len(element_steps) - 1]
    clark_y.r_R = np.linspace(np.min(r_R), 1, element_steps[len(element_steps) - 1])
    clark_y.chord = section_chord(b_D,r_R,element_steps[len(element_steps) - 1],10 * 0.3048/2)
    clark_y.stragger_1_75 = data_pitch_angle(p_D,r_R,element_steps[len(element_steps) - 1],10 * 0.3048/2)
    mass_flow_true, thrust_true, power_true, couple_true, drag_true, dT_true, dP_true, r_true,matrix_v_a3= blade_element_method(wind_speed, clark_y ,cl_interpolator,cd_interpolator)
    J_true,CT_true,CP_true,eta_true = perfo_coeff(clark_y,thrust_true,power_true,wind_speed)
    print("C_T = ",CT_true)
    for nb_elements in element_steps:
        clark_y.nb_elements = nb_elements
        clark_y.r_R = np.linspace(np.min(r_R), 1,nb_elements)
        clark_y.chord = section_chord(b_D,r_R,nb_elements,clark_y.R)
        clark_y.stragger_1_75 = data_pitch_angle(p_D,r_R,nb_elements,clark_y.R)
        mass_flow, thrust, power, couple, drag, dT, dP, r, va_3 = blade_element_method(wind_speed, clark_y,cl_interpolator,cd_interpolator)
        J,CT,CP,eta = perfo_coeff(clark_y,thrust,power,wind_speed)
        current_error = np.abs(CT - CT_true) / CT_true
        current_error += np.abs(CP - CP_true) / CP_true
        relative_error.append(current_error)

    plt.plot(element_steps, relative_error, marker='o')
    plt.xlabel("Number of elements [-]")
    plt.ylabel("Relative error [-]")
    plt.grid()
    # plt.xscale('log')  # Logarithmic scale for better visualization
    plt.savefig("figure/convergence.pdf", bbox_inches='tight', dpi=300, format='pdf')

convergence()