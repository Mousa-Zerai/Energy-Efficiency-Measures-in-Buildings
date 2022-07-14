import numpy as np
    
def Retrofit_Building_Cost_Function(x = None): 
    global doorsprop,windprop,insdata,app_properties,tv_prop,kitch_prop,wm_prop,ref_prop,light_prop,elheatdata,nelheatdata,cooldata,elhcdata,elhdhwdata,nelhdhwdata,eldhwdata,neldhwdata,slcdata,pvdata,doors_area,windows_area,walls_area,floors_area,ceil_area,light_tot,doorsdata,windata,walldata,floordata,ceildata,light_data
    ## Building Envelope
#Doors specifications, proposed solutions and total heat transfer calculation x1-x3#
    
    drows,dcol = doorsprop.shape
    doors_area = sum(doorsdata(:,1))
    for n in np.arange(1,drows+1).reshape(-1):
        i = 0 + n
        doors_cost1[n] = x(i) * doorsprop(n,2)
    
    doors_cost1 = transpose(doors_cost1)
    doors_cost = sum(doors_cost1)
    doors_inv_cost = doors_area * doors_cost
    #Windows specifications and proposed solutions and total heat transfer calculation x4-x6#
    
    wnrows,wncol = windprop.shape
    windows_area = sum(windata(:,1))
    for n in np.arange(1,wnrows+1).reshape(-1):
        i = 3 + n
        wind_cost1[n] = windprop(n,3) * x(i)
    
    wind_cost1 = transpose(wind_cost1)
    wind_cost = sum(wind_cost1)
    windows_inv_cost = windows_area * wind_cost
    #Insulation choices x7-x9#
    
    insrows,inscol = insdata.shape
    for i in np.arange(1,insrows+1).reshape(-1):
        z = 6 + i
        cost_ins1[i] = insdata(i,2) * x(z)
    
    cost_ins = sum(cost_ins1)
    # Insulation cost for walls, floors and ceilings
    
    walls_area = sum(walldata(:,1))
    floors_area = sum(floordata(:,1))
    ceil_area = sum(ceildata(:,1))
    ins_inv_cost = (walls_area + floors_area + ceil_area) * cost_ins
    ## Electric Appliances
    
    #for tv x10-x12#
    for z in np.arange(1,3+1).reshape(-1):
        i = 9 + z
        tvcost1[z] = x(i) * app_properties(1,1) * tv_prop(z,3)
    
    tv_cost = transpose(tvcost1)
    tv_inv_cost = sum(tv_cost)
    #for kitchen x13-x15#
    for z in np.arange(1,3+1).reshape(-1):
        i = 12 + z
        kitchcost1[z] = x(i) * app_properties(2,1) * kitch_prop(z,3)
    
    kitch_cost = transpose(kitchcost1)
    kitch_inv_cost = sum(kitch_cost)
    #for wm x16-x18#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 15 + z
        wmcost1[z] = x(i) * app_properties(3,1) * wm_prop(z,4)
    
    wm_cost = transpose(wmcost1)
    wm_inv_cost = sum(wm_cost)
    #for rf x19-x21#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 18 + z
        refcost1[z] = x(i) * app_properties(4,1) * ref_prop(z,3)
    
    ref_cost = transpose(refcost1)
    ref_inv_cost = sum(ref_cost)
    ## Lighting x22-x24#
    
    light_tot = sum(light_data(:,1))
    for z in np.arange(1,3+1).reshape(-1):
        i = 21 + z
        lightcost1[z] = x(i) * light_prop(z,2) * light_tot
    
    light_cost = transpose(lightcost1)
    light_inv_cost = sum(light_cost)
    ## Selection of Building Systems
#Electrical Heating system choices (x25-x27)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 24 + i
        el_heat_cost1[i] = x(j) * elheatdata(i,2)
    
    el_heat_cost = transpose(el_heat_cost1)
    el_heat_inv_cost = sum(el_heat_cost)
    #Non-Electrical Heating system choices (x28-x30)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 27 + i
        nel_heat_cost1[i] = x(j) * nelheatdata(i,2)
    
    nel_heat_cost = transpose(nel_heat_cost1)
    nel_heat_inv_cost = sum(nel_heat_cost)
    #Cooling system choices (x31-x33)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 30 + i
        el_cool_cost1[i] = x(j) * cooldata(i,2)
    
    el_cool_cost = transpose(el_cool_cost1)
    el_cool_inv_cost = sum(el_cool_cost)
    #Electrical Heating-cooling system choices (x34-x36)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 33 + i
        el_hc_cost1[i] = x(j) * elhcdata(i,2)
    
    el_hc_cost = transpose(el_hc_cost1)
    el_hc_inv_cost = sum(el_hc_cost)
    #Electrical Heating-DHW system choices (x37-x39)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 36 + i
        el_hw_cost1[i] = x(j) * elhdhwdata(i,2)
    
    el_hw_cost = transpose(el_hw_cost1)
    el_hw_inv_cost = sum(el_hw_cost)
    #Non Electrical Heating-DHW system choices (x40-x42)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 39 + i
        nel_hw_cost1[i] = x(j) * nelhdhwdata(i,2)
    
    nel_hw_cost = transpose(nel_hw_cost1)
    nel_hw_inv_cost = sum(nel_hw_cost)
    #Electrical DHW system choices (x43-x45)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 42 + i
        el_w_cost1[i] = x(j) * eldhwdata(i,2)
    
    el_w_cost = transpose(el_w_cost1)
    el_w_inv_cost = sum(el_w_cost)
    #Non Electrical DHW system choices (x46-x48)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 45 + i
        nel_w_cost1[i] = x(j) * neldhwdata(i,2)
    
    nel_w_cost = transpose(nel_w_cost1)
    nel_w_inv_cost = sum(nel_w_cost)
    #Solar collector system choices (x49-x51)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 48 + i
        slc_cost1[i] = x(j) * slcdata(i,4)
    
    slc_cost = transpose(slc_cost1)
    slc_inv_cost = sum(slc_cost)
    #solar PV (x52-x54)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 51 + i
        pv_cost1[i] = x(j) * pvdata(i,4)
    
    pv_cost = transpose(pv_cost1)
    pv_inv_cost = sum(pv_cost)
    re_cost = doors_inv_cost + windows_inv_cost + ins_inv_cost + tv_inv_cost + kitch_inv_cost + wm_inv_cost + + ref_inv_cost + light_inv_cost + el_heat_inv_cost + + nel_heat_inv_cost + el_cool_inv_cost + el_hc_inv_cost + + el_hw_inv_cost + nel_hw_inv_cost + el_w_inv_cost + + nel_w_inv_cost + slc_inv_cost + pv_inv_cost
    return re_cost
    
    return re_cost