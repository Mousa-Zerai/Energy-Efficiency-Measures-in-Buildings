
import numpy as np
global pe_existing,hs,cs,ws,ls,as
#Doors specifications, proposed solutions and total heat transfer calculation

drowsex,dcolex = doorsdata.shape
for n in np.arange(1,drowsex+1).reshape(-1):
    u_doors[n] = 1 / (1 / h_in + 1 / doorsdata(n,3) + 1 / h_out)
    blc_doors1[n] = doorsdata(n,1) * doorsdata(n,2) * u_doors(n)

blc_doors = sum(blc_doors1)
#Windows specifications and proposed solutions and total heat transfer calculation

wndatarowsex,wndatacolumnsex = windata.shape
for n in np.arange(1,wndatarowsex+1).reshape(-1):
    u_wind[n] = 1 / (1 / h_in + 1 / windata(n,6) + 1 / h_out)
    blc_wn1[n] = windata(n,1) * windata(n,1) * u_wind(n)

blc_windows = sum(blc_wn1)
for j in np.arange(1,12+1).reshape(-1):
    windgain = 0
    for n in np.arange(1,wndatarowsex+1).reshape(-1):
        windgain = windgain + windata(n,1) * windata(n,3) * windata(n,4) * windata(n,5) * windata(n,7) * climate(j,2) * days(j,1)
    windgain1[j] = windgain

windgain = transpose(windgain1)
#Insulation choices
insrowsex,inscolex = ins_exist_data.shape
for i in np.arange(1,insrowsex+1).reshape(-1):
    if ins_exist_data(i,2) == 1:
        ins_exist_data[i,1] = 1 / ins_exist_data(i,1)
    else:
        ins_exist_data[i,1] = 0

#Walls specifications and total heat transfer calculation x10-x12#

wldatarowsex,wldatacolex = walldata.shape
for n in np.arange(1,wldatarowsex+1).reshape(-1):
    u_wl1[n] = 1.0 / (1.0 / h_in + 1.0 / walldata(n,3) + ins_exist_data(1,1) + 1.0 / h_out)
    blc_wl1[n] = walldata(n,1) * walldata(n,2) * u_wl1(n)

blc_walls = sum(blc_wl1)
#Floors specifications and total heat transfer calculatiom x13-x15 #

flrowsex,flcolex = floordata.shape
for n in np.arange(1,flrowsex+1).reshape(-1):
    u_fl1[n] = 1.0 / (1.0 / h_in + 1.0 / floordata(n,3) + ins_exist_data(2,1) + 1.0 / h_out)
    blc_fl1[n] = floordata(n,1) * floordata(n,2) * u_fl1(n)

blc_floors = sum(blc_fl1)
#Ceiling specifications and proposed solutions and total heat transfer calculation x16-x18#

clrowsex,clcolex = ceildata.shape
for n in np.arange(1,clrowsex+1).reshape(-1):
    u_cl1[n] = 1.0 / (1.0 / h_in + 1.0 / ceildata(n,3) + ins_exist_data(3,1) + 1.0 / h_out)
    blc_cl1[n] = ceildata(n,1) * ceildata(n,2) * u_cl1(n)

blc_ceils = sum(blc_cl1)
##Electric Appliances

#Consumption of Appliances#

for m in np.arange(1,12+1).reshape(-1):
    tv_dem[m] = (app_properties(1,1) * days(m,1) * tv_exist(1,1) * tv_exist(1,2)) / 1000
    tv_heat[m] = tv_dem(m)

for m in np.arange(1,12+1).reshape(-1):
    kitch_dem[m] = (app_properties(2,1) * days(m,1) * kitch_exist(1,1) * kitch_exist(1,2)) / 1000
    kitch_heat[m] = kitch_dem(m)

for m in np.arange(1,12+1).reshape(-1):
    wm_dem[m] = app_properties(3,1) * days(m,1) * wm_exist(1,1) * wm_exist(1,2)
    wm_heat[m] = wm_dem(m) / wm_exist(1,3)

for m in np.arange(1,12+1).reshape(-1):
    ref_dem[m] = app_properties(4,1) * days(m,1) * ref_exist(1,1)
    ref_heat[m] = ref_dem(m) / ref_exist(1,2)

# Consumption and Heat gain from appliances#
for m in np.arange(1,12+1).reshape(-1):
    app_cons[m] = as(m) * (tv_dem(1,m) + kitch_dem(1,m) + wm_dem(1,m) + ref_dem(1,m))
    app_tot_heat[m] = as(m) * (tv_heat(1,m) + kitch_heat(1,m) + wm_heat(1,m) + ref_heat(1,m))

app_tot_heat = transpose(app_tot_heat)
annual_app_cons = sum(app_cons) * 3.6
assignin('base','app_cons',app_cons)
## heating calculations##
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
assignin('base','q_heat_dem_ex',q_heat_dem)
## cooling calculations##
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
assignin('base','q_cool_dem_c_ex',q_cool_dem_c)
## Lighting x31-x33#

#Calculate the time of operation for lamps#
light_cons = sum(times(light_data(:,2),light_data(:,3)))
#Calculate the demand#

for m in np.arange(1,12+1).reshape(-1):
    light_dem[m] = ls(m) * light_tot * days(m,1) * light_cons / 1000

annual_light_dem = sum(light_dem) * 3.6
assignin('base','light_dem_ex',light_dem)
## Building Systems
# Electrical Heating system

if elheatdataexist(1,2) == 1:
    el_heat = elheatdataexist(1,2) / elheatdataexist(1,1)
else:
    el_heat = 0

# Non-Electrical Heating system

if nelheatdataexist(1,2) == 1:
    nel_heat = nelheatdataexist(1,2) / nelheatdataexist(1,1)
else:
    nel_heat = 0

# Cooling system
if cooldataexist(1,2) == 1:
    el_cool = cooldataexist(1,2) / cooldataexist(1,1)
else:
    el_cool = 0

# Electrical Heating-cooling system
if elhcdataexist(1,2) == 1:
    el_hc = elhcdataexist(1,2) / elhcdataexist(1,1)
else:
    el_hc = 0

# Electrical Heating-DHW system choices
if elhdhwdataexist(1,2) == 1:
    el_hw = elhdhwdataexist(1,2) / elhdhwdataexist(1,1)
else:
    el_hw = 0

# Non Electrical Heating-DHW system
if nelhdhwdataexist(1,2) == 1:
    nel_hw = nelhdhwdataexist(1,2) / nelhdhwdataexist(1,1)
else:
    nel_hw = 0

# Electrical DHW system

if eldhwdataexist(1,2) == 1:
    el_w = eldhwdataexist(1,2) / eldhwdataexist(1,1)
else:
    el_w = 0

# Non Electrical DHW system choices (55-57)#
if neldhwdataexist(1,2) == 1:
    nel_w = neldhwdataexist(1,2) / neldhwdataexist(1,1)
else:
    nel_w = 0

# Solar collector system choices (58-60)#
if slcdataexist(1,4) == 1:
    slc = slcdataexist(1,1) * slcdataexist(1,2) * slcdataexist(1,3) * slcdataexist(1,4)
else:
    slc = 0

## Calculation of primary energy consumption
# Heating

# electrical systems selection for heating#

seh_el = el_heat + el_hc + el_hw
#non_electrical systems selection for heating#
seh_nel = nel_heat + nel_hw
primary_heat_el1 = annual_heat_dem * (seh_el)
primary_heat_nel = annual_heat_dem * (seh_nel)
# Cooling

#electrical systems selection for cooling#

sec_el = el_cool + el_hc
primary_cool_el1 = annual_cool_dem * (sec_el)
# water supply calculations
# Calculation of the hot water demand#

#Calculation of the gross HW demand#
wdd = (t_dhw - climate(:,3))
for m in np.arange(1,12+1).reshape(-1):
    q_wat[m] = wat_sup * d_wat * cp_wat * wdd(m) * hours(m) * 3.6

assignin('base','q_wat',q_wat)
# supply from solar collector#
for m in np.arange(1,12+1).reshape(-1):
    slc_gen[m] = climate(m,2) * days(m,1) * slc * 3.6

# calculation of net demand#

for j in np.arange(1,12+1).reshape(-1):
    if q_wat(j) > slc_gen(j):
        dq_wat_dem[j] = q_wat(j) - slc_gen(j)
    else:
        dq_wat_dem[j] = 0
    dq_wat_dem[j] = ws(j) * dq_wat_dem(1,j)

annual_wat_dem = sum(dq_wat_dem)
assignin('base','dq_wat_dem_ex',dq_wat_dem)
# Calculation of primary water consumption#
# electrical systems selection for water#

sew_el = el_w + el_hw
# non-electrical systems selection for water#

sew_nel = nel_w + nel_hw
primary_wat_el1 = annual_wat_dem * sew_el
primary_wat_nel = annual_wat_dem * sew_nel
#Lighting primary consumption#
primary_light1 = annual_light_dem
#Appliances primary consumption#
primary_app1 = annual_app_cons
#Final primary consumption#

primary_heat = primary_heat_el1 / n_grid + primary_heat_nel
primary_cool = primary_cool_el1 / n_grid
primary_wat = primary_wat_el1 / n_grid + primary_wat_nel
primary_light = primary_light1 / n_grid
primary_app = primary_app1 / n_grid
pe_existing = (primary_heat + primary_cool + primary_wat + primary_light + primary_app)
#File for exporting the results
exp_filename2 = 'Energy Consumption Results.xlsx'
#Exporting Data to Excel for analysis regarding the energy demand #
sheet_exp = 1
heat_dem = q_heat_dem * 3.6
xlswrite(exp_filename2,heat_dem,sheet_exp,'b3:b14')
cool_dem = q_cool_dem_c * 3.6
xlswrite(exp_filename2,cool_dem,sheet_exp,'c3:c14')
wat_dem = transpose(dq_wat_dem)
xlswrite(exp_filename2,wat_dem,sheet_exp,'d3:d14')
lighting_dem = transpose(light_dem) * 3.6
xlswrite(exp_filename2,lighting_dem,sheet_exp,'e3:e14')
appliances_dem = transpose(app_cons) * 3.6
xlswrite(exp_filename2,appliances_dem,sheet_exp,'f3:f14')
for m in np.arange(1,12+1).reshape(-1):
    primary_heat_ex_m[m] = q_heat_dem(m) * (seh_el / n_grid + seh_nel) * 3.6
    primary_cool_ex_m[m] = q_cool_dem_c(m) * sec_el / n_grid * 3.6
    primary_dhw_ex_m[m] = dq_wat_dem(m) * (sew_el / n_grid + sew_nel)
    primary_light_ex_m[m] = light_dem(m) / n_grid * 3.6
    primary_app_ex_m[m] = app_cons(m) / n_grid * 3.6

primary_heat_ex_m = transpose(primary_heat_ex_m)
primary_cool_ex_m = transpose(primary_cool_ex_m)
primary_dhw_ex_m = transpose(primary_dhw_ex_m)
primary_light_ex_m = transpose(primary_light_ex_m)
primary_app_ex_m = transpose(primary_app_ex_m)
xlswrite(exp_filename2,primary_heat_ex_m,'i3:i14')
xlswrite(exp_filename2,primary_cool_ex_m,'j3:j14')
xlswrite(exp_filename2,primary_dhw_ex_m,'k3:k14')
xlswrite(exp_filename2,primary_light_ex_m,'l3:l14')
xlswrite(exp_filename2,primary_app_ex_m,'m3:m14')