import matplotlib.pyplot as plt
import numpy as np


def lire_fichier(nom_fichier):
    x = []
    y = []
    try:
        with open(nom_fichier, 'r') as fichier:
            for ligne in fichier:
                valeurs = ligne.strip().split(';')
                if len(valeurs) == 2:  # Assure qu'il y a exactement deux valeurs par ligne
                    x_val, y_val = valeurs
                    x.append(float(x_val.replace(',', '.')))  # Remplace la virgule par un point pour la conversion
                    y.append(float(y_val.replace(',', '.')))
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

    return x, y



def find_max_common_element(matrix1, matrix2, tolerance=0.1):
    """
    Trouve l'élément maximum qui est commun aux mêmes positions dans deux matrices de la même taille.

    Args:
    matrix1 (np.array): Première matrice.
    matrix2 (np.array): Deuxième matrice.

    Returns:
    int: L'élément maximum commun ou None si aucun élément commun n'est trouvé.
    """
    # Convertir les listes en tableaux numpy pour une manipulation facile
    mat1 = np.array(matrix1)
    mat2 = np.array(matrix2)

    # Trouver les positions où les deux matrices sont presque égales
    common_positions = np.isclose(mat1, mat2, atol=tolerance)
    common_indices = np.where(common_positions)[0]

    # Extraire les éléments communs
    common_elements = mat1[common_positions]

    # Retourner l'élément maximum parmi les éléments communs et le taux d'erreur
    if common_indices.size > 0:
        max_common_index = common_indices[np.argmax(mat1[common_indices])]
        return max_common_index
    else:
        return None


def trust_span_graph(T_span,r,wind_speed,colective_pitch_0_75) : 
    R = np.max(r)
    r = r/R
    for i in range(len(colective_pitch_0_75)):
        plt.plot(r,T_span[i],label=rf"$\theta_{{75}} = {colective_pitch_0_75[i]}^\circ$, $v_\infty = {int(round(wind_speed[i]/0.44704))}$ mph")
    
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')  # Charge les polices nécessaires

    plt.xlabel(r'$r/R~[-]$',fontsize=14)
    plt.ylabel(r'$d\mathcal{T}~[N/m]$',fontsize=14)
    plt.legend(fontsize='xx-large')  # This makes the legend text very large
    
    plt.xlim(np.min(r),np.max(r))
    plt.ylim(np.min(T_span) - 0.5,np.max(T_span)+0.5)
    plt.savefig("figure/BEM/question_2/dT_r.pdf", bbox_inches='tight',dpi=300, format='pdf')
    plt.close()


def power_span_graph(P_span,r,wind_speed,colective_pitch_0_75) :
    R = np.max(r)
    r = r/R
    for i in range(len(colective_pitch_0_75)):
        plt.plot(r,P_span[i]/10**3,label=rf"$\theta_{{0.75}} = {colective_pitch_0_75[i]}^\circ$, $v_\infty = {int(round(wind_speed[i]/0.44704))}$ mph")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')  # Charge les polices nécessaires
    plt.xlabel(r'$r/R~[-]$',fontsize=14)
    plt.ylabel(r'$d\mathcal{P}~[kW/m]$',fontsize=14)
    plt.legend(fontsize='large')
    plt.xlim(np.min(r),np.max(r))
    plt.ylim(np.min(P_span[1]/10**3) - 0.5,np.max(P_span[1]/10**3)+0.5)
    plt.savefig("figure/BEM/question_2/dP_r.pdf", bbox_inches='tight',dpi=300, format='pdf')
    plt.close()


def plot_general(r,x,label,colective_pitch_0_75,wind_speed) : 
    R = np.max(r)
    r = r/R
    if "d_alpha" == label : 
        plt.hlines(0,np.min(r),np.max(r),linestyles='dashed',label=r'$\Delta \alpha = 0$')
        # for i in range(len(colective_pitch_0_75)):
        #     plt.plot(r,x[i],label=rf"$\theta_{{0.75}} = {colective_pitch_0_75[i]}^\circ$, $v_\infty = {int(round(wind_speed[i]/0.44704))}$ mph")
        plt.ylabel("AOA [rad]")
    for i in range(len(colective_pitch_0_75)):
        plt.plot(r,x[i],label=rf"$\theta_{{0.75}} = {colective_pitch_0_75[i]}^\circ$, $v_\infty = {int(round(wind_speed[i]/0.44704))}$ mph")
    if "cl" == label: 
    
        arg_max_common = find_max_common_element(x[0],x[1],tolerance=0.001)
        # print("arg_max_common",arg_max_common)
        plt.vlines(r[arg_max_common],np.min(x[1]),np.max(x[1]),linestyles='dashed',label=r'$r = R$')
    elif label == "dL" :
        arg_max_common = find_max_common_element(x[0],x[1])

        plt.vlines(r[arg_max_common],np.min(x[1]),np.max(x[1]),linestyles='dashed',label=r'$r = R$')
    plt.xlabel(r'$r/R~[-]$')
    plt.legend()
    plt.xlim(np.min(r),np.max(r))
    plt.savefig(f"figure/BEM/question_2/{label}_r.pdf", bbox_inches='tight',dpi=300, format='pdf')
    plt.close()


def plot_differnce(x,y,labe) :
    R = np.max(x)
    plt.plot(x/R,y[1] - y[0],label = labe)
    plt.show()
    plt.close()



def plot_eta_advance_ratio(advance_ratio, eta, colective_pitch):
    plt.figure(figsize=(12, 8))  # Définit la taille de la figure
    # plt.style.use('seaborn-v0_8-darkgrid')  # Utilise le style seaborn-darkgrid pour un arrière-plan foncé avec grille

    # Génère une palette de couleurs pour le nombre de séries de données
    color_palette = plt.get_cmap('tab10')

    for i in range(len(colective_pitch)):
        eta_i = np.array(eta[i]) 
        plt.plot(advance_ratio[i], eta_i, label=rf"$\theta_{{75}} = {colective_pitch[i]}^\circ$", color=color_palette(i), linewidth=2, markersize=5)
        if colective_pitch[i] in [15, 20, 25, 30, 35, 40, 45]:
            data = "data_naca/eta_naca/theta_" + str(colective_pitch[i]) + "_eta.txt"
            x,y = lire_fichier(data)
            plt.plot(x,y,color=color_palette(i),linestyle='--')
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')  # Charge les polices nécessaires
    plt.xlabel("Advance ratio $\\mathcal{J} [-]$", fontsize=18)
    plt.ylabel("Efficiency $\eta [-]$", fontsize=18)

    # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Place la légende à l'extérieur
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')  # Ajoute une grille

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize='xx-large')  # This makes the legend text very large

    plt.ylim(0, 1.4)
    plt.tight_layout()  # Ajuste automatiquement les paramètres du subplot pour donner un padding spécifié
    # plt.show()
    plt.savefig("figure/BEM/question_3/eta_J.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()

def plot_CT_advance_ratio(advance_ratio,CT,colective_pitch) : 
    plt.figure(figsize=(12, 8))  # Définit la taille de la figure
    # plt.style.use('seaborn-v0_8-darkgrid')  # Utilise le style seaborn-darkgrid pour un arrière-plan foncé avec grille

    # Génère une palette de couleurs pour le nombre de séries de données
    color_palette = plt.get_cmap('tab10')

    for i in range(0, len(colective_pitch)):
        CT_i = np.array(CT[i])
        plt.plot(advance_ratio[i], CT_i, label=rf"$\theta_{{75}} = {colective_pitch[i]}^\circ$", color=color_palette(i), linewidth=2, markersize=5)
        if colective_pitch[i] in [15, 20, 25, 30, 35, 40, 45]:

            data = "data_naca/CT_naca/CT_" + str(colective_pitch[i]) + ".txt"
            x,y = lire_fichier(data)
            plt.plot(x,y,color=color_palette(i),linestyle='--') 
    
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')  # Charge les polices nécessaires

    plt.xlabel("Advance ratio $\\mathcal{J} [-]$", fontsize=18)

    plt.ylabel("Thrust coefficient $C_{\\mathcal{T}} [-]$", fontsize=18)

    # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Place la légende à l'extérieur
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')  # Ajoute une grille

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize='xx-large')  # This makes the legend text very large
 
    plt.ylim(0, 0.23)
    plt.tight_layout()  # Ajuste automatiquement les paramètres du subplot pour donner un padding spécifié
    # plt.show()
    plt.savefig("figure/BEM/question_3/CT_J.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()

def plot_CP_advance_ratio(advance_ratio,CP,colective_pitch) :
    plt.figure(figsize=(12, 8))  # Définit la taille de la figure
    # plt.style.use('seaborn-v0_8-darkgrid')  # Utilise le style seaborn-darkgrid pour un arrière-plan foncé avec grille

    # Génère une palette de couleurs pour le nombre de séries de données
    color_palette = plt.get_cmap('tab10')

    for i in range(0, len(colective_pitch)):
        CP_i = np.array(CP[i])
        plt.plot(advance_ratio[i], CP_i, label=rf"$\theta_{{75}} = {colective_pitch[i]}^\circ$", color=color_palette(i), linewidth=2, markersize=5)
        if colective_pitch[i] in [15, 20, 25, 30, 35, 40, 45]:
            data = "data_naca/CP_naca/CP_" + str(colective_pitch[i]) + ".txt"
            x,y = lire_fichier(data)
            plt.plot(x,y,color=color_palette(i),linestyle='--')

    # plt.rc('text', usetex=True)
    # plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')  # Charge les polices nécessaires
    plt.xlabel("Advance ratio $J [-]$", fontsize=18)
    plt.ylabel("Power coefficient $C_P$", fontsize=18)
    plt.ylim(0, 0.4)

    # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Place la légende à l'extérieur
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')  # Ajoute une grille

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize='xx-large')  # This makes the legend text very large

    
    plt.tight_layout()  # Ajuste automatiquement les paramètres du subplot pour donner un padding spécifié
    # plt.show()
    plt.savefig("figure/BEM/question_3/CP_J.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()

# def plot_C_P_C_T_J(CP,CT,J) : 
#     plt.figure(figsize=(12, 8))  # Définit la taille de la figure
    
#     color_palette = plt.get_cmap('tab10')
#     for i in range(len(CP)):
#         plt.plot(J[i], CP[i], label=f"Collective pitch: {i}°", color=color_palette(i), linewidth=2, markersize=5)



def plot_cl_app(aoa, cl_app, cl):
    plt.plot(aoa, cl, label=r"Clark Y - $c_l$", color='b', linestyle='-', linewidth=2)
    plt.plot(aoa, cl_app, label=r"Polynomial Approximation - $c_l$", color='r', linestyle='--', linewidth=2)
    plt.xlabel(r"Angle of Attack ($\alpha$) [degrees]", fontsize=12)
    plt.ylabel(r"Lift Coefficient ($c_l$) [-]", fontsize=12)
    # plt.title(r"Comparison of Lift Coefficients vs. $\alpha$", fontsize=16)
    plt.legend(fontsize='x-large')
    # plt.grid(True)  # Add grid
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()  # Adjusts the padding for the subplot
    # plt.show()
    plt.savefig("figure/BEM/question_1/Cl_app.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()

def plot_cd_app(aoa, cd_app, cd):
    plt.plot(aoa, cd, label=r"Clark Y - $c_d$", color='b', linestyle='-', linewidth=2)
    plt.plot(aoa, cd_app, label=r"Polynomial Approximation - $c_d$", color='r', linestyle='--', linewidth=2)
    plt.xlabel(r"Angle of Attack ($\alpha$) [degrees]", fontsize=12)
    plt.ylabel(r"Drag Coefficient ($c_d$) [-]", fontsize=12)
    # plt.title(r"Comparison of Drag Coefficients vs. $\alpha$", fontsize=16)
    plt.legend(fontsize='x-large')
    # plt.grid(True)  # Add grid
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()  # Adjusts the padding for the subplot
    # plt.show()
    plt.savefig("figure/BEM/question_1/CD_app.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()

def plot_Re(aoa, Re) :
    plt.plot(aoa, Re, color='b', linestyle='-', linewidth=2)
    plt.xlabel(r"Angle of Attack ($\alpha$) [degrees]", fontsize=12)
    plt.ylabel(r"Reynolds Number [-]", fontsize=12)
    # plt.title(r"Comparison of Drag Coefficients vs. $\alpha$", fontsize=16)
    plt.legend(fontsize='x-large')
    # plt.grid(True)  # Add grid
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()  # Adjusts the padding for the subplot
    # plt.show()
    plt.savefig("figure/BEM/question_1/Re.pdf", bbox_inches='tight', dpi=300, format='pdf')
    plt.close()



