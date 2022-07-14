import numpy as np
    
def Retrofit_Building_Primary_Energy_Function(x = None): 
    global climate,t_ih,t_ic,t_dhw,h_in,h_out,tot_hpeop,volume,n_grid,doorsdata,windata,walldata,floordata,ceildata,light_data,doorsprop,windprop,insdata,app_properties,tv_prop,kitch_prop,wm_prop,ref_prop,light_prop,elheatdata,nelheatdata,cooldata,elhcdata,elhdhwdata,nelhdhwdata,eldhwdata,neldhwdata,slcdata,pvdata,d_air,cp_air,ach,wat_sup,cp_wat,d_wat,days,hours,pe_existing,hs,cs,ws,ls,as,sol_abs_factor,h_fg,sh_month,sh_ticin
    #Doors specifications, proposed solutions and total heat transfer calculation x1-x3#
    
    drows,dcol = doorsprop.shape
    blc_d1 = sum(times(doorsdata(:,1),doorsdata(:,2)))
    for n in np.arange(1,drows+1).reshape(-1):
        i = 0 + n
        u_doors[n] = 1 / (1 / h_in + 1 / doorsprop(n,1) + 1 / h_out)
        blc_d2[n] = u_doors(n) * x(i)
    
    blc_doors = blc_d1 * sum(blc_d2)
    #Windows specifications and proposed solutions and total heat transfer calculation x4-x6#
    
    wndatarows,wndatacolumns = windata.shape
    wnrows,wncol = windprop.shape
    blc_wn1 = sum(times(windata(:,1),windata(:,2)))
    for n in np.arange(1,wnrows+1).reshape(-1):
        i = 3 + n
        u_wind[n] = 1.0 / (1.0 / h_in + 1.0 / windprop(n,1) + 1.0 / h_out)
        blc_wn2[n] = u_wind(n) * x(i)
        wingainfact[n] = x(i) * windprop(n,2)
    
    blc_windows = blc_wn1 * sum(blc_wn2)
    winggaintotfact = sum(wingainfact)
    for j in np.arange(1,12+1).reshape(-1):
        windgain = 0
        for n in np.arange(1,wndatarows+1).reshape(-1):
            windgain = windgain + windata(n,1) * windata(n,3) * windata(n,4) * windata(n,5) * climate(j,2) * days(j,1) * winggaintotfact
        windgain1[j] = windgain
    
    windgain = transpose(windgain1)
    #Insulation choices x7-x9 #
    
    insrows,inscol = insdata.shape
    for i in np.arange(1,insrows+1).reshape(-1):
        z = 6 + i
        u_ins1[i] = x(z) * insdata(i,1)
    
    u_ins = sum(u_ins1)
    # Walls  total heat transfer calculation with insulation
    
    wldatarows,wldatacol = walldata.shape
    for n in np.arange(1,wldatarows+1).reshape(-1):
        u_wl1[n] = 1.0 / (1.0 / h_in + 1.0 / walldata(n,3) + 1.0 / u_ins + 1.0 / h_out)
        blc_wl1[n] = walldata(n,1) * walldata(n,2) * u_wl1(n)
    
    blc_walls = sum(blc_wl1)
    # Floors  total heat transfer calculation with insulation
    
    fldatarows,fldatacol = floordata.shape
    for n in np.arange(1,fldatarows+1).reshape(-1):
        u_fl1[n] = 1.0 / (1.0 / h_in + 1.0 / floordata(n,3) + 1.0 / u_ins + 1.0 / h_out)
        blc_fl1[n] = floordata(n) * floordata(n,2) * u_fl1(n)
    
    blc_floors = sum(blc_fl1)
    #Ceilings total heat transfer calculation with insulation
    
    cldatarows,cldatacol = ceildata.shape
    for n in np.arange(1,cldatarows+1).reshape(-1):
        u_cl1[n] = 1.0 / (1.0 / h_in + 1.0 / ceildata(n,3) + 1.0 / u_ins + 1.0 / h_out)
        blc_cl1[n] = ceildata(n,1) * ceildata(n,2) * u_cl1(n)
    
    blc_ceils = sum(blc_cl1)
    ##Electric Appliances
    
    #Consumption of Appliances#
    
    #for tv x10 - x12#
    for z in np.arange(1,3+1).reshape(-1):
        i = 9 + z
        tvprop[z] = x(i) * tv_prop(z,1) * tv_prop(z,2)
    
    tv_sum = sum(tvprop)
    for m in np.arange(1,12+1).reshape(-1):
        tv_dem[m] = (app_properties(1,1) * days(m,1) * tv_sum) / 1000
        tv_heat[m] = tv_dem(m)
    
    #for kitchen x13 - x15#
    for z in np.arange(1,3+1).reshape(-1):
        i = 12 + z
        kitchprop[z] = x(i) * kitch_prop(z,1) * kitch_prop(z,2)
    
    kitch_sum = sum(kitchprop)
    for m in np.arange(1,12+1).reshape(-1):
        kitch_dem[m] = (app_properties(2,1) * days(m,1) * kitch_sum) / 1000
        kitch_heat[m] = kitch_dem(m)
    
    #for wm x16 - x18#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 15 + z
        wmprop[z] = x(i) * wm_prop(z,1) * wm_prop(z,2)
    
    wm_sum = sum(wmprop)
    for m in np.arange(1,12+1).reshape(-1):
        wm_dem[m] = app_properties(3,1) * days(m,1) * wm_sum
        wm_heat[m] = wm_dem(m) / wm_prop(z,3)
    
    #for rf x19 - x21#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 18 + z
        refprop[z] = x(i) * ref_prop(z,1)
    
    ref_sum = sum(refprop)
    for m in np.arange(1,12+1).reshape(-1):
        ref_dem[m] = app_properties(4,1) * days(m,1) * ref_sum
        ref_heat[m] = ref_dem(m) / ref_prop(z,2)
    
    # Consumption and Heat gain from appliances#
    for m in np.arange(1,12+1).reshape(-1):
        app_cons[m] = as(m) * (tv_dem(1,m) + kitch_dem(1,m) + wm_dem(1,m) + ref_dem(1,m))
        app_tot_heat[m] = as(m) * (tv_heat(1,m) + kitch_heat(1,m) + wm_heat(1,m) + ref_heat(1,m))
    
    app_tot_heat = transpose(app_tot_heat)
    annual_app_cons = sum(app_cons) * 3.6
    assignin('base','app_cons',app_cons)
    ##heating calculations##
#Calculation of the building load factor#
    
    blc_tot = blc_doors + blc_walls + blc_windows + blc_floors + blc_ceils
    #Calculation of the heating demand#
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
    assignin('base','hs',hs)
    ##cooling calculations##
#Calculation of the cooling demand#
    
    t_sol_air = np.zeros((12,1))
    for m in np.arange(1,12+1).reshape(-1):
        t_sol_air[m,1] = climate(m,1) + sol_abs_factor * climate(m,2) * 1000 / (24 * h_out)
    
    assignin('base','t_sol_air',t_sol_air)
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
    assignin('base','cs',cs)
    #Lighting x22-x24#
    
    #Calculate the time of operation for lamps#
    light_time = sum(times(light_data(:,1),light_data(:,2)))
    #Calculate the demand#
    
    for z in np.arange(1,3+1).reshape(-1):
        i = 21 + z
        lightprop[z] = x(i) * light_prop(z,1) / 1000
    
    lightsum = sum(lightprop)
    for m in np.arange(1,12+1).reshape(-1):
        light_dem[m] = ls(m) * light_time * days(m,1) * lightsum
    
    annual_light_dem = sum(light_dem) * 3.6
    assignin('base','light_dem',light_dem)
    ##Selection of Building Systems
#Electrical Heating system choices (x25-x27)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 24 + i
        el_heat[i] = x(j) / elheatdata(i,1)
    
    el_heat = transpose(el_heat)
    el_heat_sum = sum(el_heat)
    #Non-Electrical Heating system choices (x28-x30)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 27 + i
        nel_heat[i] = x(j) / nelheatdata(i,1)
    
    nel_heat = transpose(nel_heat)
    nel_heat_sum = sum(nel_heat)
    #Cooling system choices (x31-x33)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 30 + i
        el_cool[i] = x(j) / cooldata(i,1)
    
    el_cool = transpose(el_cool)
    el_cool_sum = sum(el_cool)
    #Electrical Heating-cooling system choices (x34-x36)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 33 + i
        el_hc[i] = x(j) / elhcdata(i,1)
    
    el_hc = transpose(el_hc)
    el_hc_sum = sum(el_hc)
    #Electrical Heating-DHW system choices (x37-x39)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 36 + i
        el_hw[i] = x(j) / elhdhwdata(i,1)
    
    el_hw = transpose(el_hw)
    el_hw_sum = sum(el_hw)
    #Non Electrical Heating-DHW system choices (x40-x42)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 39 + i
        nel_hw[i] = x(j) / nelhdhwdata(i,1)
    
    nel_hw = transpose(nel_hw)
    nel_hw_sum = sum(nel_hw)
    #Electrical DHW system choices (x43-x45)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 42 + i
        el_w[i] = x(j) / eldhwdata(i,1)
    
    el_w = transpose(el_w)
    el_w_sum = sum(el_w)
    #Non Electrical DHW system choices (x46-x48)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 45 + i
        nel_w[i] = x(j) / neldhwdata(i,1)
    
    nel_w = transpose(nel_w)
    nel_w_sum = sum(nel_w)
    #Solar collector system choices (x49-x51)#
    
    for i in np.arange(1,3+1).reshape(-1):
        j = 48 + i
        slc[i] = x(j) * slcdata(i,1) * slcdata(i,2) * slcdata(i,3)
    
    slc = transpose(slc)
    slc_sum = sum(slc)
    #solar PV (x52-x54)#
    
    for j in np.arange(1,3+1).reshape(-1):
        i = 51 + j
        pv_sys[j] = pvdata(j,1) * pvdata(j,2) * pvdata(j,3) * x(i)
        pv_sel[j] = x(i)
    
    pv_sys_sum = sum(pv_sys)
    pv_sel_sum = sum(pv_sel)
    #Calculation of primary heating consumption (not taking account the electricity supply system)#
    
    #electrical systems selection for heating#
    
    seh_el = el_heat_sum + el_hc_sum + el_hw_sum
    #non_electrical systems selection for heating#
    seh_nel = nel_heat_sum + nel_hw_sum
    primary_heat_el1 = annual_heat_dem * (seh_el)
    primary_heat_nel = annual_heat_dem * (seh_nel)
    #Calculation of primary cooling consumption (not taking account the electricity supply system)#
    
    #electrical systems selection for cooling#
    
    sec_el = el_cool_sum + el_hc_sum
    primary_cool_el1 = annual_cool_dem * (sec_el)
    ##water supply calculations##
#Calculation of the hot water demand#
    
    #Calculation of the gross HW demand#
    wdd = (t_dhw - climate(:,3))
    for m in np.arange(1,12+1).reshape(-1):
        q_wat[m] = wat_sup * d_wat * cp_wat * wdd(m) * hours(m) * 3.6
    
    assignin('base','q_wat',q_wat)
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
    slc_gen = transpose(slc_gen1)
    assignin('base','dq_wat_dem',dq_wat_dem)
    assignin('base','slc_gen',slc_gen)
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
    ##Electricity supply
#PV generation#
    for m in np.arange(1,12+1).reshape(-1):
        pvgen1[m] = climate(m,2) * days(m,1) * pv_sys_sum * 3.6
    
    annualpvgen = sum(pvgen1)
    pv_supply = annualpvgen
    pv_gen = transpose(pvgen1)
    assignin('base','pv_gen',pv_gen)
    #alternative systems power generation#
    alt_power = pv_supply
    if tot_el_dem > alt_power:
        grid_supply = tot_el_dem - alt_power
    else:
        grid_supply = 0
    
    total_power_supply = grid_supply + alt_power
    f_grid = grid_supply / total_power_supply
    f_pv = pv_supply / total_power_supply
    #Final primary consumption#
    
    for m in np.arange(1,12+1).reshape(-1):
        primary_heat_m[m] = q_heat_dem(m) * (seh_el * f_grid / n_grid + seh_nel) * 3.6
        primary_cool_m[m] = q_cool_dem_c(m) * sec_el * f_grid / n_grid * 3.6
        primary_dhw_m[m] = dq_wat_dem(m) * (sew_el * f_grid / n_grid + sew_nel)
        primary_light_m[m] = light_dem(m) * f_grid / n_grid * 3.6
        primary_app_m[m] = app_cons(m) * f_grid / n_grid * 3.6
    
    primary_heat_m = transpose(primary_heat_m)
    primary_cool_m = transpose(primary_cool_m)
    primary_dhw_m = transpose(primary_dhw_m)
    primary_light_m = transpose(primary_light_m)
    primary_app_m = transpose(primary_app_m)
    assignin('base','primary_heat_m',primary_heat_m)
    assignin('base','primary_cool_m',primary_cool_m)
    assignin('base','primary_dhw_m',primary_dhw_m)
    assignin('base','primary_light_m',primary_light_m)
    assignin('base','primary_app_m',primary_app_m)
    assignin('base','f_grid',f_grid)
    assignin('base','f_pv',f_pv)
    primary_heat = (primary_heat_el1 / n_grid * (f_grid) + primary_heat_nel)
    primary_cool = primary_cool_el1 / n_grid * (f_grid)
    primary_wat = (primary_wat_el1 / n_grid * (f_grid) + primary_wat_nel)
    primary_light = primary_light1 / n_grid * (f_grid)
    primary_app = primary_app1 / n_grid * (f_grid)
    pe_retrofit1 = primary_heat + primary_cool + primary_wat + primary_light + primary_app
    
    pe_retrofit = - pe_existing + pe_retrofit1
    return pe_retrofit
    
    return pe_retrofit