def perfo_coeff(propeller,T,P,wind_speed) : 
    """
    Function to compute the performance coefficients of the propeller
    Parameters :
    - propeller : object : propeller object
    - T : float : thrust
    - C : float : torque
    - P : float : power
    Returns :
    - J : float : advance ratio
    - CT : float : thrust coefficient
    - CP : float : power coefficient
    - eta : float : efficiency
    """
    rho = 1.225
    # rho = 1.058
    J = wind_speed /(propeller.RPS * propeller.D)
    CT = T / (propeller.D**4 * rho * propeller.RPS**2)
    CP = P / (rho * propeller.RPS**3 * propeller.D**5)
    eta = wind_speed * T / P
    return J,CT,CP,eta

