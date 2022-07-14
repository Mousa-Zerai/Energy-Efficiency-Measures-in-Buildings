
#Global variables used in the functions
import numpy as np
global climate,t_ih,t_ic,t_dhw,h_in,h_out,tot_hpeop,volume,n_grid,doorsdata,windata,walldata,floordata,ceildata,light_data,doorsprop,windprop,insdata,ceilprop,wallprop,floorprop,app_prop,tv_prop,kitch_prop,wm_prop,ref_prop,light_prop,elheatdata,nelheatdata,cooldata,elhcdata,elhdhwdata,nelhdhwdata,eldhwdata,neldhwdata,slcdata,pvdata,d_air,cp_air,ach,wat_sup,cp_wat,d_wat,days,hours,g1min,g1max,g2min,g2max,doors_area,windows_area,walls_area,floors_area,ceil_area,light_tot,p1,p2,hs,cs,ls,ws,as,sh_month,sh_ticin,h_fg
## Input Data
#The excel file containing the data for the proposed solutions and the
#export file of the results
filename = 'New Building Data.xlsx'
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
hs = xlsread(filename,sheet,'g2:g13')
cs = xlsread(filename,sheet,'h2:h13')
ls = xlsread(filename,sheet,'i2:i13')
ws = xlsread(filename,sheet,'j2:j13')
as = xlsread(filename,sheet,'k2:k13')
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
insrange = 'E2:F4'
insdata = xlsread(filename,inssheet,insrange)
print('\\nInsert the properties of the walls: ' % ())
walldata = xlsread(filename,- 1)
wallssheet = 4
wallsrange = 'M2:O4'
wallprop = xlsread(filename,wallssheet,wallsrange)
print('\\nInsert the properties of the floors: ' % ())
floordata = xlsread(filename,- 1)
floorssheet = 5
floorsrange = 'M2:N4'
floorprop = xlsread(filename,floorssheet,floorsrange)
print('\\nInsert the properties of the ceilings: ' % ())
ceildata = xlsread(filename,- 1)
ceilssheet = 6
ceilsrange = 'M2:N4'
ceilprop = xlsread(filename,ceilssheet,ceilsrange)
doors_area = sum(doorsdata(:,1))
windows_area = sum(windata(:,1))
walls_area = sum(walldata(:,1))
floors_area = sum(floordata(:,1))
ceil_area = sum(ceildata(:,1))
applsheet = 9
app_data = 'B2:B5'
tv_range = 'B8:D10'
kitchen_range = 'B13:D15'
wm_range = 'B18:E20'
ref_range = 'B23:D25'
app_prop = xlsread(filename,applsheet,app_data)
tv_prop = xlsread(filename,applsheet,tv_range)
kitch_prop = xlsread(filename,applsheet,kitchen_range)
wm_prop = xlsread(filename,applsheet,wm_range)
ref_prop = xlsread(filename,applsheet,ref_range)
print('\\nInsert the properties of the lamps:' % ())
light_data = xlsread(filename,- 1)
lightsheet = 8
light_tot = sum(light_data(:,1))
light_range = 'H2:I4'
light_prop = xlsread(filename,lightsheet,light_range)
heatsheet = 10
heatrange = 'D3:E5'
elheatdata = xlsread(filename,heatsheet,heatrange)
nelheatrange = 'D11:E13'
nelheatdata = xlsread(filename,heatsheet,nelheatrange)
coolsheet = 11
coolrange = 'D3:E5'
cooldata = xlsread(filename,coolsheet,coolrange)
hcsheet = 12
elhcrange = 'D3:E5'
elhcdata = xlsread(filename,hcsheet,elhcrange)
hdhwsheet = 13
elhdhwrange = 'D3:E5'
elhdhwdata = xlsread(filename,hdhwsheet,elhdhwrange)
nelhdhwrange = 'D11:E13'
nelhdhwdata = xlsread(filename,hdhwsheet,nelhdhwrange)
dhwsheet = 14
eldhwrange = 'D3:E5'
eldhwdata = xlsread(filename,dhwsheet,eldhwrange)
dhwsheet = 14
neldhwrange = 'D11:E13'
neldhwdata = xlsread(filename,dhwsheet,neldhwrange)
slcsheet = 15
slcrange = 'D2:G4'
slcdata = xlsread(filename,slcsheet,slcrange)
pvsheet = 16
pvrange = 'D2:G4'
pvdata = xlsread(filename,pvsheet,pvrange)
## Calculations for primary energy consumption
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
## Solution for minimizing primary energy consumption
#Table with for equality constraints#
Aeq = np.zeros((14,63))
Aeq[1,np.arange[1,3+1]] = 1
Aeq[2,np.arange[4,6+1]] = 1
Aeq[3,np.arange[7,9+1]] = 1
Aeq[4,np.arange[10,12+1]] = 1
Aeq[5,np.arange[13,15+1]] = 1
Aeq[6,np.arange[16,18+1]] = 1
Aeq[7,np.arange[19,21+1]] = 1
Aeq[8,np.arange[22,24+1]] = 1
Aeq[9,np.arange[25,27+1]] = 1
Aeq[10,np.arange[28,30+1]] = 1
Aeq[11,np.arange[31,33+1]] = 1
Aeq[12,np.arange[34,39+1]] = 1
Aeq[12,np.arange[43,51+1]] = 1
Aeq[13,np.arange[40,45+1]] = 1
Aeq[14,np.arange[46,57+1]] = 1
#Values of equality constraints
beq = np.ones((14,1))
#Table with inequality constraints#
A_ineq = np.zeros((2,63))
A_ineq[1,np.arange[58,60+1]] = 1
A_ineq[2,np.arange[61,63+1]] = 1
#Values of inequality constraints#
b_ineq = np.ones((2,1))
#lower and upper function bounds#
lb = np.zeros((63,1))
ub = np.ones((63,1))
#Creating integer variables and initial value of the solution
for j in np.arange(1,63+1).reshape(-1):
    int_var[1,j] = 0 + j
    x0[j,1] = 1

#Calling function for independent minimization of primary energy
#consumption

primary_energy_function = New_Building_Primary_Energy_Function
#Options and selection of algorithm#
opts = optiset('display','iter','warnings','all','solver','bonmin')
Opt = opti('fun',primary_energy_function,'eq',Aeq,beq,'ineq',A_ineq,b_ineq,'bounds',lb,ub,'int',int_var,'options',opts)
#solution for minimize primary energy consumption
x,fval,exitflag,info = solve(Opt,x0)
g1min = fval

x_energy_min = x

## Solution for minimizing acquisition cost
cost_function = New_Building_Cost_Function
Opt = opti('fun',cost_function,'eq',Aeq,beq,'ineq',A_ineq,b_ineq,'bounds',lb,ub,'int',int_var,'options',opts)
x,fval,exitflag,info = solve(Opt,x0)
g2min = fval

x_cost_min = x

## Multi-objective optimization with global criterion method

#Creating an array for the values of the global criterion function
Pareto_front = np.zeros((21,1))
#Creating an array for the x solutions for each case
x_min_global = np.zeros((63,21))
x_min_global[:,1] = x_energy_min(:,1)
x_min_global[:,21] = x_cost_min(:,1)
#Vectors for weight coefficients
weight_1 = np.arange(0,1+0.05,0.05)
weight_2 = 1 - weight_1
# An itterative procedure for solving the moo function for all weight
# coefficients and create the Pareto frontier

primary_energy = np.zeros((21,1))
primary_energy[1,1] = g1min
primary_energy[21,1] = New_Building_Primary_Energy_Function(x_min_global(:,21))
inv_cost = np.zeros((21,1))
inv_cost[21,1] = g2min
inv_cost[1,1] = New_Building_Cost_Function(x_min_global(:,1))
# Pay-off Table

g1max = primary_energy(21,1)
g2max = inv_cost(1,1)
for i in np.arange(1,19+1).reshape(-1):
    z = i + 1
    p1 = weight_2(z)
    p2 = weight_1(z)
    #Calling function and options for the multi objective optimization
    moo_function = New_Building_MOO_Function
    Opt = opti('fun',moo_function,'eq',Aeq,beq,'ineq',A_ineq,b_ineq,'bounds',lb,ub,'int',int_var,'options',opts)
    print('Iteration number: %g\\n' % (z))
    x,fval = solve(Opt,x0)
    primary_energy[z,1] = New_Building_Primary_Energy_Function(x)
    inv_cost[z,1] = New_Building_Cost_Function(x)
    x_min_global[:,z] = x(:,1)
    Pareto_front[z,1] = fval

p1_coef = transpose(weight_2)
p2_coef = transpose(weight_1)
#Exporting data to excel
sheet_exp = 1
x_min_global1 = transpose(x_min_global)
xlswrite(exp_filename,x_min_global1,sheet_exp,'f2:bp22')
xlswrite(exp_filename,inv_cost,sheet_exp,'e2:e22')
xlswrite(exp_filename,primary_energy,sheet_exp,'d2:d22')
xlswrite(exp_filename,p2_coef,sheet_exp,'c2:c22')
xlswrite(exp_filename,p1_coef,sheet_exp,'b2:b22')
xlswrite(exp_filename,Pareto_front,sheet_exp,'a2:a22')
print('\\n' % ())
print('\\nThe optimizations are finished and the results are located' % ())
print('\\nin the Excel File "Pareto Results".' % ())
print('\\n' % ())