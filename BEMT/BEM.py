import numpy as np
from propeller_parameters import *
from clarkypolarsRe import *
from fit_data import *
# This part of the code is inspired ny the predict performance section 2.3.2 of the lecture notes

def blade_element_method(wind_speed,propeller,cl_interpolator,cd_interpolator) :
    # The most common guess is to simply consider that the propeller has no 
    # impact on the flow, hence va3 = v∞ and vu2+ = 0. 
    # For more understanding, see in lecture note Figure 2.1.
    
    # data precisoin 
    n_b_iterations    = 100
    tolerance         = 1e-4
    new_v_a3          = wind_speed
    new_v_u2_p        = 0
    nb_element_blade  = propeller.nb_elements
    # data air at sea level
    rho            = 1.225              #air density at sea level
    mu             = 1.85e-5            #dynamic viscosity of air at sea level

    #  Parameters of the propeller 
    r                      = propeller.r_R * propeller.R 
    chord                  = propeller.chord
    pitch_angle            = calcule_colective_pitch(propeller.stragger_1_75,propeller.collective_pitcth_0_75)
    pitch_angle_25         = calcule_colective_pitch(propeller.stragger_1_75,np.radians(25))
    # dr = r[1] - r[0]
    dr = 1

    
    #Initialisation matrix
    d_mass_flow = np.zeros(nb_element_blade)
    dL          = np.zeros(nb_element_blade)
    dD          = np.zeros(nb_element_blade)
    dT_n        = np.zeros(nb_element_blade)
    dC_n        = np.zeros(nb_element_blade)
    dP_n        = np.zeros(nb_element_blade)
    aoa_store   = np.zeros(nb_element_blade)
    # cl_appStore = np.zeros(nb_element_blade)
    # cd_appStore = np.zeros(nb_element_blade)
    cl_store    = np.zeros(nb_element_blade)
    cd_store    = np.zeros(nb_element_blade)
    Ren_store   = np.zeros(nb_element_blade)

    for i in range(nb_element_blade) : 
        # Iteratif process inspired from the aerospace propulsion exercice 
        old_v_a3 = 1
        old_v_u2_p = 1
        new_v_a3 = wind_speed
        new_v_u2_p = 0
        j = 0
        while n_b_iterations > j:
            # Vérifie si old_v_a3 ou old_v_u2_p est zéro et ajuste la condition en conséquence
            condition1 = np.inf if old_v_a3 == 0 else np.abs((new_v_a3-old_v_a3)/old_v_a3)
            condition2 = np.inf if old_v_u2_p == 0 else np.abs((new_v_u2_p-old_v_u2_p)/old_v_u2_p)
            if condition1 < tolerance or condition2 < tolerance:
                break
            old_v_a3   = new_v_a3
            old_v_u2_p = new_v_u2_p
            
            # Compute the velocity component at the propeller disk
            va2_n = (wind_speed + old_v_a3)/2
            vu2_n = old_v_u2_p/2
            wa2_n = va2_n 
            wu2_n = vu2_n - propeller.omega * r[i]
            # from the axial velocity,we find the local mass flow  
            # Note that the element thrust and power are given per meter of span ( i.e. dr = 1).
            d_mass_flow[i] = 2 * np.pi * r[i] * rho * va2_n * dr
            w2_n           = np.sqrt(wa2_n**2 + wu2_n**2)
            # always negatif due to the definition of the angle : defined positif if oriened in the direction of ratasion 
            beta2_n           = np.arctan2(wu2_n,wa2_n)  

            local_pitch_angle = pitch_angle[i]
            aoa_n             = local_pitch_angle - beta2_n - np.pi/2
            aoa_n             = np.arctan2(np.sin(aoa_n), np.cos(aoa_n))
            aoa_store[i]      = aoa_n
            Re_n              = rho * w2_n * chord[i] / mu
            Ren_store[i]      = Re_n
            cl    = cl_interpolator((aoa_n, Re_n))
            cd    = cd_interpolator((aoa_n, Re_n))
            # cl_app    = 0.1101 *aoa_n + 0.4409
            # cd_app    = 0.0006 *aoa_n**2 - 0.0042 *aoa_n + 0.0050
            # cl_appStore[i] = cl_app
            # cd_appStore[i] = cd_app
            cl_store[i] = cl
            cd_store[i] = cd

            # multiplie by n, due to the fact the dL and dD correspondant to the whole stram tube 
            # and therofore to the sum of the force of all balde
            dL[i] = cl * propeller.n * chord[i] * 0.5 * rho * w2_n**2 * dr
            dD[i] = cd * propeller.n * chord[i] * 0.5 * rho * w2_n**2 * dr
            # Calcul de la poussée et du couple de façon géométrique (2.69)
            dF_a = -(dL[i] * np.sin(beta2_n) + dD[i] * np.cos(beta2_n)) 
            dF_u = dL[i] * np.cos(beta2_n) - dD[i] * np.sin(beta2_n)

            dT_n[i] = dF_a
            dC_n[i] = r[i] * dF_u
            dP_n[i] = propeller.omega * dC_n[i]  # (2.56)

            new_v_a3   = wind_speed + dF_a / d_mass_flow[i]
            new_v_u2_p = dF_u / d_mass_flow[i]
            
            j += 1
    # mass_flow = np.trapz(d_mass_flow)
    # thrust    = np.trapz(dT_n)
    # power     = np.trapz(dP_n)
    # couple    = np.trapz(dC_n)
    # drag      = np.trapz(dD)
    mass_flow = np.trapz(d_mass_flow,r)
    thrust    = np.trapz(dT_n,r)
    power     = np.trapz(dP_n,r)
    couple    = np.trapz(dC_n,r)
    drag      = np.trapz(dD,r)


    return mass_flow, thrust, power, dC_n, dD, dT_n, dP_n, r, aoa_store, Ren_store