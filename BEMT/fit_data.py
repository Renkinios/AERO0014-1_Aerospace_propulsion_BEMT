import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Let's define the data points as numpy arrays
# Function to calculate polynomial coefficients and residuals
def fit_polynomial(x, y,max_degree=5):
    coefs = []
    residuals = []
    for degree in range(1, max_degree + 1):
        # Fit polynomial of degree 'degree'
        p = np.poly1d(np.polyfit(x, y, degree))
        # Calculate residual sum of squares
        y_fit = p(x)
        residual = np.sum((y - y_fit)**2)
        coefs.append(p)
        residuals.append(residual)
        
    # Return the polynomial coefficients and residuals for each degree
    return coefs, residuals
def choice_interpolation(r_R,X) :
    coefs_X, residuals_X = fit_polynomial(r_R, X)
    # Finding the polynomial with the least residual for b/D and p/D
    min_residual_index_X = np.argmin(residuals_X)
    best_poly_X = coefs_X[min_residual_index_X]
    return best_poly_X

def fit_data_b_D(r_R,b_D,nb_elems) : 
    r_R = np.append(r_R,1)
    b_D = np.append(b_D,0)
    # Fit polynomials to b/D and p/D data
    best_poly_b_D = choice_interpolation(r_R,b_D)
    # Plotting the best fit polynomial for b/D
    x_fit = np.linspace(min(r_R), 1, nb_elems)
    b_D_fit = best_poly_b_D(x_fit)
    return x_fit,b_D_fit

def fit_data_p_D(r_R,p_D,nb_elems) :
    # Plotting the best fit polynomial for p/D
    x_fit = np.linspace(min(r_R), 1, nb_elems)
    best_poly_p_D = choice_interpolation(r_R,p_D)
    p_D_fit = best_poly_p_D(x_fit)
    return x_fit,p_D_fit
# Plotting the data and the polynomial fits
def plot_data_b_D(r_R,b_D,n_b_elems) : 
    x_fit,b_D_fit = fit_data_b_D(r_R,b_D,n_b_elems)
    b_D_fit = b_D_fit 
    print(b_D_fit[len(b_D_fit)-1])
    plt.figure(figsize=(10, 6))
    plt.plot(r_R, b_D, 'o', label='Data')
    plt.plot(x_fit, b_D_fit, label=f'Polynomial approximation')
    plt.xlabel('r/R [-]')
    plt.ylabel('b/D [-]')
    plt.legend()
    plt.grid(True)
    plt.savefig("figure/data_P_B/fit_data_b_D.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()
    
def calcule_colective_pitch(data_pitch_angle,collective_pitcth_0_75) :
    return data_pitch_angle  + collective_pitcth_0_75

def plot_data_p_D_b_D(r_R,p_D,b_D,n_b_elems,propeller) :
    dpi = 100
    fig_width = 682 / dpi  # largeur en pouces
    fig_height = 765 / dpi  # hauteur en pouces
    color_palette = plt.get_cmap('tab10')

    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    propeller.collective_pitcth_0_75 = np.radians(35)
    # Création du premier axe
    x_fit,b_D_fit = fit_data_b_D(r_R,b_D,n_b_elems)
    x_fit,p_D_fit = fit_data_p_D(r_R,p_D,n_b_elems)
    fig, ax1 = plt.subplots()
    # Dessiner la première ligne sur l'axe y gauche
    ax1.plot(x_fit, b_D_fit, color = color_palette(0))  # 'g-' pour une ligne verte
    ax1.set_xlabel(r'r/R [-]',fontsize=12)
    ax1.set_ylabel(r'$b/D$ [-]', color = color_palette(0),fontsize=12)

    # Créer un deuxième axe qui partage le même axe x
    ax2 = ax1.twinx()
    ax2.plot(x_fit, p_D_fit, color = color_palette(1))  # 'b-' pour une ligne bleue
    ax2.set_ylabel(r'$p/D$ [-]', color = color_palette(1),fontsize=12)
    pitch_angle = calcule_colective_pitch(propeller.stragger_1_75,propeller.collective_pitcth_0_75)
    P_colective_pitch = np.tan(pitch_angle) * np.pi * x_fit
    ax2.plot(x_fit, P_colective_pitch, color = color_palette(1))  # 'b-' pour une ligne bleue
    ax2.text(0.8,1.25, r'$\theta_{75} = 25^{\circ}$', fontsize=10, color = color_palette(1))
    ax2.text(0.85,1.9, r'$\theta_{75} = 35^{\circ}$', fontsize=10, color = color_palette(1))
    # plt.show()
    # plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')  # Ajoute une grille

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.legend(fontsize='large')
    plt.savefig("figure/data_P_B/fit_data_p_D_b_D.pdf", dpi=dpi, format='pdf')
    plt.close()
def plot_data_p_D(r_R,p_D,n_b_elems) :
    x_fit,p_D_fit = fit_data_p_D(r_R,p_D,n_b_elems)
    plt.figure(figsize=(10, 6))
    plt.plot(r_R, p_D, 'o', label='Data')
    plt.plot(x_fit, p_D_fit, label=f'Polynomial approximation')
    plt.xlabel('r/R [-]')
    plt.ylabel('p/D [-]')
    plt.legend()
    plt.grid(True)
    plt.savefig("figure/data_P_B/fit_data_p_D.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()
def calcule_pitch(P,r) :

    stragger = np.arctan(P/(2*np.pi*r))
    return stragger
def data_pitch_angle(p_D,r_R,nb_elment,radius) : 

    # Fit polynomials to b/D and p/D data
    r_R_fit,p_R_fit = fit_data_p_D(r_R,p_D,nb_elment)

    P = p_R_fit * radius * 2 
    r = r_R_fit * radius

    pitch_data = calcule_pitch(P,r) - np.radians(25)
    return pitch_data

def section_chord(b_D,r_R,nb_elment,radius) : 
    # Fit polynomials to b/D and p/D data

    r_R_fit,b_D_fit = fit_data_b_D(r_R,b_D,nb_elment)

    b = b_D_fit * radius * 2
    return b


def graph_interpolation_cl(cl_interpolator) :
    aoa = np.linspace(np.radians(-20),np.radians(20),100)
    Re  = np.linspace(1e4,1e7,100)
    cl = np.zeros((len(aoa),len(Re)))
    for i in range(len(aoa)) : 
        for j in range(len(Re)) : 
            cl[i][j] = cl_interpolator((aoa[i], Re[j]))
    contour = plt.contour(Re, aoa, cl, levels=20)
    plt.clabel(contour, inline=True, fontsize=8)
    plt.show()
    plt.close()
