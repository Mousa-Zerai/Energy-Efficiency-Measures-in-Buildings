import numpy as np
    
def New_Building_MOO_Function(x = None): 
    global climate,t_ih,t_ic,t_dhw,h_in,h_out,tot_hpeop,volume,n_grid,doorsdata,windata,walldata,floordata,ceildata,light_data,doorsprop,windprop,insdata,ceilprop,wallprop,floorprop,app_prop,tv_prop,kitch_prop,wm_prop,ref_prop,light_prop,elheatdata,nelheatdata,cooldata,elhcdata,elhdhwdata,nelhdhwdata,eldhwdata,neldhwdata,slcdata,pvdata,d_air,cp_air,ach,wat_sup,cp_wat,d_wat,days,hours,doors_area,windows_area,walls_area,floors_area,ceil_area,light_tot,g1min,g1max,g2min,g2max,p1,p2,hs,cs,ls,ws,as,sh_month,sh_ticin,h_fg
    #Doors specifications, proposed solutions and total heat transfer calculation x1-x3#
    
    drows,dcol = doorsprop.shape
    blc_d1 = sum(times(doorsdata(:,1),doorsdata(:,2)))
    for n in np.arange(1,drows+1).reshape(-1):
        i = 0 + n
        u_doors[n] = 1 / (1 / h_in + 1 / doorsprop(n,1) + 1 / h_out)
        blc_d2[n] = u_doors(n) * x(i)
        doors_cost1[n] = x(i) * doorsprop(n,2)
    
    u_doors = transpose(u_doors)
    blc_doors = blc_d1 * sum(blc_d2)
    doors_cost1 = transpose(doors_cost1)
    doors_cost = sum(doors_cost1)
    doors_inv_cost = doors_area * doors_cost
    #Windows specifications and proposed solutions and total heat transfer calculation x4-x6#
    
    wndatarows,wndatacolumns = windata.shape
    wnrows,wncol = windprop.shape
    blc_wn1 = sum(times(windata(:,1),windata(:,2)))
    for n in np.arange(1,wnrows+1).reshape(-1):
        i = 3 + n
        u_wind[n] = 1 / (1 / h_in + 1 / windprop(n,1) + 1 / h_out)
        blc_wn2[n] = u_wind(n) * x(i)
        wind_cost1[n] = windprop(n,3) * x(i)
    
    u_wind = transpose(u_wind)
    blc_windows = blc_wn1 * sum(blc_wn2)
    wind_cost1 = transpose(wind_cost1)
    wind_cost = sum(wind_cost1)
    windows_inv_cost = windows_area * wind_cost
    for i in np.arange(1,wnrows+1).reshape(-1):
        z = 3 + i
        wingainfact[i] = x(z) * windprop(i,2)
    
    winggaintotfact = sum(wingainfact)
    for j in np.arange(1,12+1).reshape(-1):
        windgain = 0
        for n in np.arange(1,wndatarows+1).reshape(-1):
            windgain = windgain + windata(n,1) * windata(n,3) * windata(n,4) * windata(n,5) * climate(j,2) * days(j,1) * winggaintotfact
        windgain1[j] = windgain
    
    annualwingain = sum(windgain1)
    windgain = transpose(windgain1)
    #Insulation choices x7-x9#
    
    insrows,inscol = insdata.shape
    for i in np.arange(1,insrows+1).reshape(-1):
        z = 6 + i
        u_ins1[i] = x(z) * insdata(i,1)
        cost_ins1[i] = insdata(i,2) * x(z)
    
    u_ins = sum(u_ins1)
    cost_ins = sum(cost_ins1)
    #Walls specifications and proposed solutions and total heat transfer
# calculation x10-x12
    
    wlproprows,wlpropcol = wallprop.shape
    blc_wl1 = sum(times(walldata(:,1),walldata(:,2)))
    for n in np.arange(1,wlproprows+1).reshape(-1):
        k = 9 + n
        u_wl1[n] = x(k) * 1.0 / (1.0 / h_in + 1.0 / wallprop(n,1) + 1.0 / u_ins + 1.0 / h_out)
        wlcost1[n] = wallprop(n,3) * x(k)
        wall[n] = x(k)
    
    wall_sum = sum(wall)
    blc_wl2 = sum(u_wl1)
    blc_walls = blc_wl1 * blc_wl2
    wall_cost = sum(wlcost1)
    wall_inv_cost = walls_area * (wall_cost + cost_ins)
    #Floors specifications and proposed solutions and total heat transfer
# calculatiom x13-x15
    
    flrows,flcol = floorprop.shape
    blc_fl1 = sum(times(floordata(:,1),floordata(:,2)))
    for n in np.arange(1,flrows+1).reshape(-1):
        k = 12 + n
        u_fl1[n] = x(k) * 1.0 / (1.0 / h_in + 1.0 / floorprop(n,1) + 1.0 / u_ins + 1.0 / h_out)
        flcost1[n] = floorprop(n,2) * x(k)
    
    blc_fl2 = sum(u_fl1)
    blc_floors = blc_fl1 * blc_fl2
    floor_cost = sum(flcost1)
    floor_inv_cost = floors_area * (floor_cost + cost_ins)
    #Ceiling specifications and proposed solutions and total heat transfer
# calculation x16-x18
    
    clrows,flcol = ceilprop.shape
    blc_cl1 = sum(times(ceildata(:,1),ceildata(:,2)))
    for n in np.arange(1,clrows+1).reshape(-1):
        k = 15 + n
        u_cl1[n] = x(k) * 1.0 / (1.0 / h_in + 1.0 / ceilprop(n,1) + 1.0 / u_ins + 1.0 / h_out)
        clcost1[n] = ceilprop(n,2) * x(k)
    
    blc_cl2 = sum(u_cl1)
    blc_ceils = blc_cl1 * blc_cl2
    ceil_cost = sum(clcost1)
    ceil_inv_cost = ceil_area * (ceil_cost + cost_ins)
    ## Electric Appliances
    
    #Consumption of Appliances#
    
    #for tv x19-x21#
    for z in np.arange(1,3+1).reshape(-1):
        i = 18 + z
        tvprop[z] = x(i) * tv_prop(z,1) * tv_prop(z,2)
        tvcost1[z] = x(i) * app_prop(1,1) * tv_prop(z,3)
    
    tv_sum = sum(tvprop)
    tv_cost = transpose(tvcost1)
    tv_inv_cost = sum(tv_cost)
    for m in np.arange(1,12+1).reshape(-1):
        tv_dem[m] = (app_prop(1,1) * days(m,1) * tv_sum) / 1000
        tv_heat[m] = tv_dem(m)
    
    #for kitchen x22-x24#
    for z in np.arange(1,3+1).reshape(-1):
        i = 21 + z
        kitchprop[z] = x(i) * kitch_prop(z,1) * kitch_prop(z,2)
        kitchcost1[z] = x(i) * app_prop(2,1) * kitch_prop(z,3)
    
    kitch_sum = sum(kitchprop)
    kitch_cost = transpose(kitchcost1)
    kitch_inv_cost = sum(kitch_cost)
    for m in np.arange(1,12+1).reshape(-1):
        kitch_dem[m] = (app_prop(2,1) * days(m,1) * kitch_sum) / 1000
        kitch_heat[m] = kitch_dem(m)
    
    #for wm x25-x27#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 24 + z
        wmprop[z] = x(i) * wm_prop(z,1) * wm_prop(z,2)
        wmcost1[z] = x(i) * app_prop(3,1) * wm_prop(z,4)
    
    wm_sum = sum(wmprop)
    wm_cost = transpose(wmcost1)
    wm_inv_cost = sum(wm_cost)
    for m in np.arange(1,12+1).reshape(-1):
        wm_dem[m] = app_prop(3,1) * days(m,1) * wm_sum
        wm_heat[m] = wm_dem(m) / wm_prop(z,3)
    
    #for rf x28-x30#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 27 + z
        refprop[z] = x(i) * ref_prop(z,1) * ref_prop(z,2)
        refcost1[z] = x(i) * app_prop(4,1) * ref_prop(z,3)
    
    ref_sum = sum(refprop)
    ref_cost = transpose(refcost1)
    ref_inv_cost = sum(ref_cost)
    for m in np.arange(1,12+1).reshape(-1):
        ref_dem[m] = app_prop(4,1) * days(m,1) * ref_sum
        ref_heat[m] = ref_dem(m) / ref_prop(z,3)
    
    # Consumption and Heat gain from appliances#
    for m in np.arange(1,12+1).reshape(-1):
        app_cons[m] = as(m) * (tv_dem(1,m) + kitch_dem(1,m) + wm_dem(1,m) + ref_dem(1,m))
        app_tot_heat[m] = as(m) * (tv_heat(1,m) + kitch_heat(1,m) + wm_heat(1,m) + ref_heat(1,m))
    
    app_tot_heat = transpose(app_tot_heat)
    annual_app_cons = sum(app_cons) * 3.6
    assignin('base','app_cons',app_cons)
    ## Heating calculations
# Calculation of the building load factor#
    
    blc_tot = blc_doors + blc_walls + blc_windows + blc_floors + blc_ceils
    # Calculation of the heating demand#
    hdd = (t_ih - climate(:,1))
    q_loss_heat = np.multiply((blc_tot * hdd),hours) / 1000
    q_loss_vent = np.multiply((d_air * cp_air * ach * volume / 3600 * hdd),hours)
    for m in np.arange(1,12+1).reshape(-1):
        peop_heat[m] = tot_hpeop / 1000 * hours(m,1)
    
    peop_heat = transpose(peop_heat)
    q_in_gain = peop_heat + app_tot_heat
    q_sol_gain = windgain
    q_heat_dem = q_loss_heat + q_loss_vent - q_in_gain - q_sol_gain
    for j in np.arange(1,12+1).reshape(-1):
        q_heat_dem[j,1] = hs(j) * q_heat_dem(j,1)
        if q_heat_dem(j,1) > 0:
            q_heat_dem[j,1] = q_heat_dem(j,1)
        else:
            q_heat_dem[j,1] = 0
    
    annual_heat_dem = sum(q_heat_dem) * 3.6
    assignin('base','q_heat_dem',q_heat_dem)
    ## Cooling calculations##
#Calculation of the cooling demand#
    
    t_sol_air = np.zeros((12,1))
    for i in np.arange(1,3+1).reshape(-1):
        for m in np.arange(1,12+1).reshape(-1):
            t_sol_air[m,1] = climate(m,1) + wallprop(i,2) * wall_sum * climate(m,2) * 1000 / (24 * h_out)
    
    cdd_1 = (t_ic - t_sol_air(:,1))
    cdd_2 = (t_ic - climate(:,1))
    q_loss_heat_c = np.multiply((blc_tot * cdd_1),hours) / 1000
    q_loss_vent_c = np.multiply((d_air * cp_air * ach * volume / 3600 * cdd_2),hours) + np.multiply(d_air * ach * volume * h_fg / 3600 * (sh_ticin - sh_month(:,1)),hours)
    q_in_gain_c = peop_heat + app_tot_heat
    q_sol_gain_c = windgain
    q_cool_dem_c = + q_in_gain_c + q_sol_gain_c - q_loss_heat_c - q_loss_vent_c
    for j in np.arange(1,12+1).reshape(-1):
        q_cool_dem_c[j,1] = cs(j) * q_cool_dem_c(j,1)
        if q_cool_dem_c(j,1) > 0:
            q_cool_dem_c[j,1] = q_cool_dem_c(j,1)
        else:
            q_cool_dem_c[j,1] = 0
    
    annual_cool_dem = sum(q_cool_dem_c) * 3.6
    assignin('base','q_cool_dem_c',q_cool_dem_c)
    ## Lighting x31-x33#
    
    #Calculate the time of operation for lamps#
    light_time = sum(times(light_data(:,1),light_data(:,2)))
    light_tot = sum(light_data(:,1))
    #Calculate the demand#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 30 + z
        lightprop[z] = x(i) * light_prop(z,1) / 1000
        lightcost1[z] = x(i) * light_prop(z,2) * light_tot
    
    lightsum = sum(lightprop)
    light_cost = transpose(lightcost1)
    light_inv_cost = sum(light_cost)
    for m in np.arange(1,12+1).reshape(-1):
        light_dem[m] = ls(m) * light_time * days(m,1) * lightsum
    
    annual_light_dem = sum(light_dem) * 3.6
    assignin('base','light_dem',light_dem)
    ## Selection of Building Systems
#Electrical Heating system choices (34-36)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 33 + i
        el_heat[i] = x(j) / elheatdata(i,1)
        el_heat_cost1[i] = x(j) * elheatdata(i,2)
    
    el_heat = transpose(el_heat)
    el_heat_sum = sum(el_heat)
    el_heat_cost = transpose(el_heat_cost1)
    el_heat_inv_cost = sum(el_heat_cost)
    #Non-Electrical Heating system choices (37-39)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 36 + i
        nel_heat[i] = x(j) / nelheatdata(i,1)
        nel_heat_cost1[i] = x(j) * nelheatdata(i,2)
    
    nel_heat = transpose(nel_heat)
    nel_heat_sum = sum(nel_heat)
    nel_heat_cost = transpose(nel_heat_cost1)
    nel_heat_inv_cost = sum(nel_heat_cost)
    #Cooling system choices (40-42)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 39 + i
        el_cool[i] = x(j) / cooldata(i,1)
        el_cool_cost1[i] = x(j) * cooldata(i,2)
    
    el_cool = transpose(el_cool)
    el_cool_sum = sum(el_cool)
    el_cool_cost = transpose(el_cool_cost1)
    el_cool_inv_cost = sum(el_cool_cost)
    #Electrical Heating-cooling system choices (43-45)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 42 + i
        el_hc[i] = x(j) / elhcdata(i,1)
        el_hc_cost1[i] = x(j) * elhcdata(i,2)
    
    el_hc = transpose(el_hc)
    el_hc_sum = sum(el_hc)
    el_hc_cost = transpose(el_hc_cost1)
    el_hc_inv_cost = sum(el_hc_cost)
    #Electrical Heating-DHW system choices (46-48)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 45 + i
        el_hw[i] = x(j) / elhdhwdata(i,1)
        el_hw_cost1[i] = x(j) * elhdhwdata(i,2)
    
    el_hw = transpose(el_hw)
    el_hw_sum = sum(el_hw)
    el_hw_cost = transpose(el_hw_cost1)
    el_hw_inv_cost = sum(el_hw_cost)
    #Non Electrical Heating-DHW system choices (49-51)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 48 + i
        nel_hw[i] = x(j) / nelhdhwdata(i,1)
        nel_hw_cost1[i] = x(j) * nelhdhwdata(i,2)
    
    nel_hw = transpose(nel_hw)
    nel_hw_sum = sum(nel_hw)
    nel_hw_cost = transpose(nel_hw_cost1)
    nel_hw_inv_cost = sum(nel_hw_cost)
    #Electrical DHW system choices (52-54)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 51 + i
        el_w[i] = x(j) / eldhwdata(i,1)
        el_w_cost1[i] = x(j) * eldhwdata(i,2)
    
    el_w = transpose(el_w)
    el_w_sum = sum(el_w)
    el_w_cost = transpose(el_w_cost1)
    el_w_inv_cost = sum(el_w_cost)
    #Non Electrical DHW system choices (55-57)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 54 + i
        nel_w[i] = x(j) / neldhwdata(i,1)
        nel_w_cost1[i] = x(j) * neldhwdata(i,2)
    
    nel_w = transpose(nel_w)
    nel_w_sum = sum(nel_w)
    nel_w_cost = transpose(nel_w_cost1)
    nel_w_inv_cost = sum(nel_w_cost)
    #Solar collector system choices (58-60)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 57 + i
        slc[i] = x(j) * slcdata(i,1) * slcdata(i,2) * slcdata(i,3)
        slc_cost1[i] = x(j) * slcdata(i,4)
    
    slc = transpose(slc)
    slc_sum = sum(slc)
    slc_cost = transpose(slc_cost1)
    slc_inv_cost = sum(slc_cost)
    #solar PV (61-63)#
    
    for j in np.arange(1,3+1).reshape(-1):
        i = 60 + j
        pv_sys[j] = pvdata(j,1) * pvdata(j,2) * pvdata(j,3) * x(i)
        pv_cost1[j] = x(i) * pvdata(j,4)
        pv_sel[j] = x(i)
    
    pv_sys_sum = sum(pv_sys)
    pv_sel_sum = sum(pv_sel)
    pv_cost = transpose(pv_cost1)
    pv_inv_cost = sum(pv_cost)
    #Calculation of primary heating consumption
    
    #electrical systems selection for heating#
    
    seh_el = el_heat_sum + el_hc_sum + el_hw_sum
    #non_electrical systems selection for heating#
    seh_nel = nel_heat_sum + nel_hw_sum
    primary_heat_el1 = annual_heat_dem * (seh_el)
    primary_heat_nel = annual_heat_dem * (seh_nel)
    #Calculation of primary cooling consumption
    
    #electrical systems selection for cooling#
    
    sec_el = el_cool_sum + el_hc_sum
    primary_cool_el1 = annual_cool_dem * (sec_el)
    ## Water Energy Consumption
#Calculation of the hot water demand#
    
    #Calculation of the gross HW demand#
    wdd = (t_dhw - climate(:,3))
    for m in np.arange(1,12+1).reshape(-1):
        q_wat[m] = wat_sup * d_wat * cp_wat * wdd(m) * hours(m) * 3.6
    
    #supply from solar collector#
    for m in np.arange(1,12+1).reshape(-1):
        slc_gen1[m] = climate(m,2) * days(m,1) * slc_sum * 3.6
    
    annualslcgain = sum(slc_gen1)
    #calculation of net demand#
    
    for j in np.arange(1,12+1).reshape(-1):
        if q_wat(j) > slc_gen1(j):
            dq_wat_dem[j] = q_wat(j) - slc_gen1(j)
        else:
            dq_wat_dem[j] = 0
        dq_wat_dem[j] = ws(j) * dq_wat_dem(1,j)
    
    annual_wat_dem = sum(dq_wat_dem)
    assignin('base','q_wat',q_wat)
    assignin('base','dq_wat_dem',dq_wat_dem)
    #Calculation of primary water consumption#
#electrical systems selection for water#
    
    sew_el = el_w_sum + el_hw_sum
    #non-electrical systems selection for water#
    
    sew_nel = nel_w_sum + nel_hw_sum
    primary_wat_el1 = annual_wat_dem * sew_el
    primary_wat_nel = annual_wat_dem * sew_nel
    #Lighting primary consumption#
    primary_light1 = annual_light_dem
    #Appliances primary consumption#
    primary_app1 = annual_app_cons
    #Total electrity demand#
    tot_el_dem = primary_heat_el1 + primary_cool_el1 + primary_wat_el1 + primary_light1 + primary_app1
    ## Electricity supply
#PV generation#
    for m in np.arange(1,12+1).reshape(-1):
        pvgen1[m] = climate(m,2) * days(m,1) * pv_sys_sum * 3.6
    
    annualpvgen = sum(pvgen1)
    pv_supply = annualpvgen
    #alternative systems power generation#
    alt_power = pv_supply
    if tot_el_dem > alt_power:
        grid_supply = tot_el_dem - alt_power
    else:
        grid_supply = 0
    
    total_power_supply = grid_supply + alt_power
    f_grid = grid_supply / total_power_supply
    f_pv = pv_supply / total_power_supply
    ## Final primary consumption
    
    primary_heat = (primary_heat_el1 / n_grid * (f_grid) + primary_heat_nel)
    primary_cool = primary_cool_el1 / n_grid * (f_grid)
    primary_wat = (primary_wat_el1 / n_grid * (f_grid) + primary_wat_nel)
    primary_light = primary_light1 / n_grid * (f_grid)
    primary_app = primary_app1 / n_grid * (f_grid)
    pe = primary_heat + primary_cool + primary_wat + primary_light + primary_app
    cost = doors_inv_cost + windows_inv_cost + wall_inv_cost + floor_inv_cost + + ceil_inv_cost + tv_inv_cost + kitch_inv_cost + wm_inv_cost + + ref_inv_cost + light_inv_cost + el_heat_inv_cost + + nel_heat_inv_cost + el_cool_inv_cost + el_hc_inv_cost + + el_hw_inv_cost + nel_hw_inv_cost + el_w_inv_cost + + nel_w_inv_cost + slc_inv_cost + pv_inv_cost
    global_criterion = p1 / (g1max - g1min) * (pe - g1min) + p2 / (g2max - g2min) * (cost - g2min)
    return global_criterion
    
    return global_criterion