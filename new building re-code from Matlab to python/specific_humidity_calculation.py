    
def specific_humidity_calculation(t_air = None,rh_air = None): 
    Pressure = 1013.25
    
    P_sv = 6.11 * 10 ** (7.5 * t_air / (273.5 + t_air))
    P_v = rh_air * P_sv / 100
    mr = 0.622 * P_v / (Pressure - P_v)
    sh = mr / (1 + mr)
    return sh
    
    return sh