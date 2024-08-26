import numpy as np
import matplotlib.pyplot as plt
from propeller_parameters import *
from performance_caracteristique import *
from BEM import *
from graph_bem import *
from fit_data import *
from clarkypolarsRe import *

plot_interpolation = False
Question_1         = True
Question_2         = False
Question_3         = False


clark_y = propeller_clark_y() # instanciate the propeller
cl_interpolator,cd_interpolator = clarkypolarsRe_interppolation() # load the interpolator for the cl and cd



# graph_interpolation_cl(cl_interpolator)
# Question 1 
# Considering an engine rotational speed of 800 RPM, compute the thrust, the power absorbed by the propeller
# and the propulsive efficiency for θ_75 = 25◦ at a wind speed of 90 mph, and for θ_75 = 35◦ at a wind speed of
# 135 mph. Plot the thrust and power distribution along the span and discuss the pitchwise distribution of the
# velocity triangles, torque and thrust. (10/20)

if plot_interpolation:
    r_R = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    b_D = np.array([0.0360, 0.0525, 0.0700, 0.0760, 0.0735, 0.0660, 0.0565, 0.0450])
    p_D = np.array([0.670, 0.840, 0.940, 0.980, 1.020, 1.090, 1.125, 1.190])
    plot_data_b_D(r_R,b_D,100)
    plot_data_p_D(r_R,p_D,100)
    plot_data_p_D_b_D(r_R,p_D,b_D,100,clark_y)


if Question_1:
    wind_speed = 90 * 0.44704
    clark_y.collective_pitcth_0_75 = np.radians(25)
    mass_flow, thrust, power, couple, drag, dT, dP, r, aoa, Ren = blade_element_method(wind_speed, clark_y,cl_interpolator,cd_interpolator)
    cl = cl_interpolator((aoa,Ren))
    cd = cd_interpolator((aoa,Ren))
    aoa = np.degrees(aoa)
    cl_app    = 0.1101 *aoa + 0.4409
    cd_app    = 0.0006 *aoa**2 - 0.0042 *aoa + 0.0050
    plot_cl_app(aoa, cl_app, cl)
    plot_cd_app(aoa, cd_app, cd)
if Question_2:
    trust = np.zeros(2)
    power = np.zeros(2)
    efficiency = np.zeros(2)

    colective_pitch_0_75 = np.array([25,35])

    wind_speed = np.array([90,135]) * 0.44704
    dT_matrix = []
    dP_matrix = []
    for i in range(len(colective_pitch_0_75)):
        clark_y.collective_pitcth_0_75 = np.radians(colective_pitch_0_75[i])
        mass_flow, thrust, power, couple, drag, dT, dP, r, aoa, Ren = blade_element_method(wind_speed[i], clark_y,cl_interpolator,cd_interpolator)
        dT_matrix.append(dT)
        dP_matrix.append(dP)

        J,CT,CP,eta = perfo_coeff(clark_y,thrust,power,wind_speed[i])
        print(f"collective_pitch_0_75: {clark_y.collective_pitcth_0_75} [rad]\t wind_speed: {wind_speed[i]} [m/s]")

        print("trust \t",thrust)
        print("power \t",power)
        print("J \t",J)
        print("CT \t",CT)
        print("CP \t",CP)
        print("eta \t",eta)
        print("#"*50)
    
    trust_span_graph(dT_matrix,r,wind_speed,colective_pitch_0_75)
    power_span_graph(dP_matrix,r,wind_speed,colective_pitch_0_75)



# Question 2
# Reproduce the experiments of [1] by computing the thrust coefficient, power coefficient and propulsive efficiency
# with respect to advance ratio for θ75 = 15◦
# to 45◦
# . Compare your results with the experimental results.


if Question_2:
    nb_airspeeds     = 40
    min_airspeed     = 30 * 0.44704
    max_airspeed     = 115 * 0.44704
    airspeeds_matrix = np.linspace(min_airspeed,max_airspeed,nb_airspeeds)


    nb_RPM     = 30
    RPM_matrix = np.linspace(339,800,nb_RPM)


    CT  = []
    CP  = []
    J   = []
    eta = []

    colective_pitch_0_75 = np.array([15,20,25,30,35,40,45])


    clark_y.nb_elements = 100
    clark_y.r_R         = np.linspace(0.2,1,clark_y.nb_elements)

    for i in range(len(colective_pitch_0_75)):
        if colective_pitch_0_75[i] < 25:
            clark_y.RPM   = 1000
            clark_y.RPS   = clark_y.RPM / 60
            clark_y.omega = clark_y.RPS  * 2 * np.pi
        else:
            clark_y.RPM   = 800
            clark_y.RPS   = clark_y.RPM / 60
            clark_y.omega = clark_y.RPS  * 2 * np.pi
        CT.append([])
        CP.append([])
        J.append([])
        eta.append([])
        for j in range(nb_airspeeds + nb_RPM):

            if j >= nb_airspeeds :
                airspeeds     = 115 * 0.44704
                clark_y.RPM   = RPM_matrix[-j + nb_airspeeds + nb_RPM -1]
                clark_y.RPS   = clark_y.RPM / 60
                clark_y.omega = clark_y.RPS  * 2 * np.pi
            else : 
                airspeeds = airspeeds_matrix[j]
            clark_y.collective_pitcth_0_75 = np.radians(colective_pitch_0_75[i])
            mass_flow, thrust, power, couple, drag, T_span, P_span,r, _, _ = blade_element_method(airspeeds, clark_y,cl_interpolator, cd_interpolator)
            J_coef,CT_coef,CP_coef,eta_coef = perfo_coeff(clark_y,thrust,power,airspeeds)
            # print("J_coef \t",J_coef, "eta_coef \t",eta_coef)
            CT[i].append(CT_coef)
            CP[i].append(CP_coef)
            J[i].append(J_coef)
            eta[i].append(eta_coef)

            if eta[i][j] < 0 or CT[i][j] < 0 or CP[i][j] < 0:
                eta[i][j] = 0
                break
    
    # plot_question_2_general(J,m_flow,colective_pitch_0_75,"masse_flow")
    plot_eta_advance_ratio(J,eta,colective_pitch_0_75)
    plot_CT_advance_ratio(J,CT,colective_pitch_0_75)
    plot_CP_advance_ratio(J,CP,colective_pitch_0_75)



