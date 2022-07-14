
#Global variables used in the functions
import numpy as np
global climate,t_ih,t_ic,t_dhw,h_in,h_out,tot_hpeop,volume,n_grid,doorsdata,windata,walldata,floordata,ceildata,light_data,doorsprop,windprop,insdata,ins_exist_data,app_properties,tv_prop,tv_exist,kitch_prop,kitch_exist,wm_prop,wm_exist,ref_prop,ref_exist,light_prop,elheatdata,nelheatdata,cooldata,elhcdata,elhdhwdata,nelhdhwdata,eldhwdata,neldhwdata,slcdata,pvdata,d_air,cp_air,ach,wat_sup,cp_wat,d_wat,days,hours,g1min,g1max,doors_area,windows_area,walls_area,floors_area,ceil_area,light_tot,p1,p2,g2min,g2max,elheatdataexist,nelheatdataexist,cooldataexist,eldhwdataexist,elhdhwdataexist,neldhwdataexist,nelhdhwdataexist,slcdataexist,elhcdataexist,hs,cs,ws,ls,as,sol_abs_factor,sh_month,sh_ticin,h_fg
## Input Data
#The excel file containing the data for the proposed solutions and the
#export file of the results
filename = 'Retrofit Building Data.xlsx'
exp_filename = 'Pareto Results.xlsx'
#Climate data of the location#
sheet = 1
xlRange = 'B2:E13'
climate = xlsread(filename,sheet,xlRange)
tihin = xlsread(filename,sheet,'b17')
ticin = xlsread(filename,sheet,'b18')
tiwin = xlsread(filename,sheet,'b19')
rh_ann = xlsread(filename,sheet,'e14')
h_in = xlsread(filename,sheet,'b20')
h_out = xlsread(filename,sheet,'b21')
people = xlsread(filename,sheet,'b22')
volume = xlsread(filename,sheet,'b23')
wat_dem_per = xlsread(filename,sheet,'b24')
#Local grid efficiency#
n_grid = xlsread(filename,sheet,'b25')
# monthly indicators
hs = xlsread(filename,sheet,'g2:g13')
cs = xlsread(filename,sheet,'h2:h13')
ls = xlsread(filename,sheet,'i2:i13')
ws = xlsread(filename,sheet,'j2:j13')
as = xlsread(filename,sheet,'k2:k13')
## Building characteristics

print('Insert the properties of the doors: ' % ())
doorsdata = xlsread(filename,- 1)
doorssheet = 2
doorsrange = 'H2:I4'
doorsprop = xlsread(filename,doorssheet,doorsrange)
print('\\nInsert the properties of the windows: ' % ())
windata = xlsread(filename,- 1)
windowssheet = 3
windowsrange = 'L2:N4'
windprop = xlsread(filename,windowssheet,windowsrange)
inssheet = 7
ins_prop_range = 'E2:F4'
insdata = xlsread(filename,inssheet,ins_prop_range)
ins_exist_range = 'E9:F11'
ins_exist_data = xlsread(filename,inssheet,ins_exist_range)
print('\\nInsert the properties of the walls: ' % ())
walldata = xlsread(filename,- 1)
sol_abs_factor = xlsread(filename,4,'N2')
print('\\nInsert the properties of the floors: ' % ())
floordata = xlsread(filename,- 1)
print('\\nInsert the properties of the ceilings: ' % ())
ceildata = xlsread(filename,- 1)
doors_area = sum(doorsdata(:,1))
windows_area = sum(windata(:,1))
walls_area = sum(walldata(:,1))
floors_area = sum(floordata(:,1))
ceil_area = sum(ceildata(:,1))
applsheet = 9
app_data = 'B2:B5'
tv_range = 'B8:D10'
tv_exist_range = 'I2:J2'
kitchen_range = 'B13:D15'
kitchen_exist_range = 'I5:J5'
wm_range = 'B18:E20'
wm_exist_range = 'I8:K8'
ref_range = 'B23:D25'
ref_exist_range = 'I11:J11'
app_properties = xlsread(filename,applsheet,app_data)
tv_prop = xlsread(filename,applsheet,tv_range)
tv_exist = xlsread(filename,applsheet,tv_exist_range)
kitch_prop = xlsread(filename,applsheet,kitchen_range)
kitch_exist = xlsread(filename,applsheet,kitchen_exist_range)
wm_prop = xlsread(filename,applsheet,wm_range)
wm_exist = xlsread(filename,applsheet,wm_exist_range)
ref_prop = xlsread(filename,applsheet,ref_range)
ref_exist = xlsread(filename,applsheet,ref_exist_range)
print('\\nInsert the properties of the lamps:' % ())
light_data = xlsread(filename,- 1)
lightsheet = 8
light_tot = sum(light_data(:,1))
light_range = 'H2:I4'
light_prop = xlsread(filename,lightsheet,light_range)
heatsheet = 10
heatrange = 'D3:E5'
heat_exist = 'L3:M3'
elheatdata = xlsread(filename,heatsheet,heatrange)
elheatdataexist = xlsread(filename,heatsheet,heat_exist)
nelheatrange = 'D11:E13'
nelheat_exist = 'L5:M5'
nelheatdata = xlsread(filename,heatsheet,nelheatrange)
nelheatdataexist = xlsread(filename,heatsheet,nelheat_exist)
coolsheet = 11
coolrange = 'D3:E5'
cool_exist = 'L3:M3'
cooldata = xlsread(filename,coolsheet,coolrange)
cooldataexist = xlsread(filename,coolsheet,cool_exist)
hcsheet = 12
elhcrange = 'D3:E5'
elhcexist = 'L3:M3'
elhcdata = xlsread(filename,hcsheet,elhcrange)
elhcdataexist = xlsread(filename,hcsheet,elhcexist)
hdhwsheet = 13
elhdhwrange = 'D3:E5'
elhdhw_exist = 'L3:M3'
elhdhwdata = xlsread(filename,hdhwsheet,elhdhwrange)
elhdhwdataexist = xlsread(filename,hdhwsheet,elhdhw_exist)
nelhdhwrange = 'D11:E13'
nelhdhw_exist = 'L5:M5'
nelhdhwdata = xlsread(filename,hdhwsheet,nelhdhwrange)
nelhdhwdataexist = xlsread(filename,hdhwsheet,nelhdhw_exist)
dhwsheet = 14
eldhwrange = 'D3:E5'
eldhw_exist = 'L3:M3'
eldhwdata = xlsread(filename,dhwsheet,eldhwrange)
eldhwdataexist = xlsread(filename,dhwsheet,eldhw_exist)
neldhwrange = 'D11:E13'
neldhw_exist = 'L5:M5'
neldhwdata = xlsread(filename,dhwsheet,neldhwrange)
neldhwdataexist = xlsread(filename,dhwsheet,neldhw_exist)
slcsheet = 15
slcrange = 'D2:G4'
slcdata = xlsread(filename,slcsheet,slcrange)
slc_exist = 'D10:G10'
slcdataexist = xlsread(filename,slcsheet,slc_exist)
# proposed pv #
pvsheet = 16
pvrange = 'D2:G4'
pvdata = xlsread(filename,pvsheet,pvrange)
## Preliminary Calculations for primary energy consumption
#Base temperature for heating,cooling, humidity and heat transfer coeffcients#

sh_month = np.zeros((12,1))
for i in np.arange(1,12+1).reshape(-1):
    sh_month[i,1] = specific_humidity_calculation(climate(i,1),climate(i,4))

sh_ticin = specific_humidity_calculation(ticin,rh_ann)
climate[:,1] = climate(:,1) + 273
climate[:,3] = climate(:,3) + 273
t_ih = tihin + 273
t_ic = ticin + 273
t_dhw = tiwin + 273
#People heat gain#

q_peop = 115

tot_hpeop = people * q_peop
#Ventilation#
d_air = 1.2
cp_air = 1.0035
ach = 1.5
h_fg = 2340

#water demand#

wat_sup = people * wat_dem_per * (10 ** - 3) / (24 * 3600)
cp_wat = 4.18
d_wat = 1000
#Months days and hours#
days = np.array([[31],[28],[31],[30],[31],[30],[31],[31],[30],[31],[30],[31]])
hours = 24 * days
## Calculation of the primary energy consumption of the existing building

Existing_Building_Primary_Energy
print('\\nThe primary energy consumption of the existing building' % ())
print('\\nMJ/year) is: %g\\n' % (pe_existing))
## Solution for minimizing primary energy consumption
#Table with for equality constraints#
Aeq = np.zeros((11,54))
Aeq[1,np.arange[1,3+1]] = 1
Aeq[2,np.arange[4,6+1]] = 1
Aeq[3,np.arange[7,9+1]] = 1
Aeq[4,np.arange[10,12+1]] = 1
Aeq[5,np.arange[13,15+1]] = 1
Aeq[6,np.arange[16,18+1]] = 1
Aeq[7,np.arange[19,21+1]] = 1
Aeq[8,np.arange[22,24+1]] = 1
Aeq[9,np.arange[25,30+1]] = 1
Aeq[9,np.arange[34,42+1]] = 1
Aeq[10,np.arange[31,36+1]] = 1
Aeq[11,np.arange[37,48+1]] = 1
#Values of equality constraints
beq = np.ones((11,1))
#Table with inequality constraints#
A_ineq = np.zeros((2,54))
A_ineq[1,np.arange[49,51+1]] = 1
A_ineq[2,np.arange[52,54+1]] = 1
#Values of inequality constraints#
b_ineq = np.ones((2,1))
#lower and upper function bounds#
lb = np.zeros((54,1))
ub = np.ones((54,1))
#Creating integer variables and initial value of the solution
for j in np.arange(1,54+1).reshape(-1):
    int_var[1,j] = 0 + j

x0 = np.ones((54,1))
#Calling function for independent minimization of primary energy
#consumption

primary_energy_function = Retrofit_Building_Primary_Energy_Function
#Options and selection of algorithm#
opts = optiset('display','iter','warnings','all','solver','bonmin')
Opt = opti('fun',primary_energy_function,'eq',Aeq,beq,'ineq',A_ineq,b_ineq,'bounds',lb,ub,'int',int_var,'options',opts)
#solution for minimize primary energy consumption
x,fval,exitflag,info = solve(Opt,x0)
g1max = fval

x_energy_save_min = x

## Solution for minimizing acquisition cost
cost_function = Retrofit_Building_Cost_Function
Opt = opti('fun',cost_function,'eq',Aeq,beq,'ineq',A_ineq,b_ineq,'bounds',lb,ub,'int',int_var,'options',opts)
x,fval,exitflag,info = solve(Opt,x0)
g2min = fval

x_cost_re_min = x

## Multi-objective optimization with global criterion method

#Creating an array for the values of the global criterion function
Pareto_frontier = np.zeros((21,1))
#Creating an array for the x solutions for each case
x_min_global = np.zeros((54,21))
x_min_global[:,1] = x_energy_save_min(:,1)
x_min_global[:,21] = x_cost_re_min(:,1)
#Vectors for weight coefficients
weight_1 = np.arange(0,1+0.05,0.05)
weight_2 = 1 - weight_1
# An itterative procedure for solving the moo function for all weight
# coefficients and create the Pareto frontier

primary_energy = np.zeros((21,1))
primary_energy[1,1] = g1max
primary_energy[21,1] = Retrofit_Building_Primary_Energy_Function(x_min_global(:,21))
inv_cost = np.zeros((21,1))
inv_cost[21,1] = g2min
inv_cost[1,1] = Retrofit_Building_Cost_Function(x_min_global(:,1))
# Pay-off table
g1min = primary_energy(21,1)
g2max = inv_cost(1,1)
for i in np.arange(1,19+1).reshape(-1):
    z = i + 1
    p1 = weight_2(z)
    p2 = weight_1(z)
    #Calling function and options for the multi objective optimization
    moo_function = Retrofit_Building_MOO_Function
    Opt = opti('fun',moo_function,'eq',Aeq,beq,'ineq',A_ineq,b_ineq,'bounds',lb,ub,'int',int_var,'options',opts)
    print('Iteration number: %g\\n' % (z))
    x,fval = solve(Opt,x0)
    primary_energy[z,1] = Retrofit_Building_Primary_Energy_Function(x)
    inv_cost[z,1] = Retrofit_Building_Cost_Function(x)
    x_min_global[:,z] = x(:,1)
    Pareto_frontier[z,1] = fval

p1_coef = transpose(weight_2)
p2_coef = transpose(weight_1)
energy_savings = np.abs(primary_energy)
#Exporting data to excel
sheet_exp = 1
x_min_global1 = transpose(x_min_global)
xlswrite(exp_filename,pe_existing,sheet_exp,'b28')
xlswrite(exp_filename,x_min_global1,sheet_exp,'f2:bg22')
xlswrite(exp_filename,inv_cost,sheet_exp,'e2:e22')
xlswrite(exp_filename,energy_savings,sheet_exp,'d2:d22')
xlswrite(exp_filename,p2_coef,sheet_exp,'c2:c22')
xlswrite(exp_filename,p1_coef,sheet_exp,'b2:b22')
xlswrite(exp_filename,Pareto_frontier,sheet_exp,'a2:a22')
print('\\n' % ())
print('\\nThe optimizations are finished and the results are located' % ())
print('\\nin the Excel File "Pareto Results".' % ())
print('\\n' % ())