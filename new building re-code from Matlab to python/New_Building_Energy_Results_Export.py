##A script for the calculation of energy demand for a specific x solution
print('\\n' % ())
print('You can insert a x vector for the calculation of energy demand' % ())
print('\\nand primary energy consumption.' % ())
print('\\n' % ())
print('\\nThe x solutions are stored in the variable x_min_global' % ())
print('\\nand each column represents a vector, with the first being' % ())
print('\\nfor p1=1 and the last for p1=0' % ())
print('\\n' % ())
x_demand = input_('\\nInsert the x vector of the case you are interested: ')
#Calling the primary energy function
energy_demand = New_Building_Primary_Energy_Function(x_demand)
#File for exporting the results
exp_filename = 'Energy Consumption Results.xlsx'
#Exporting Data to Excel for analysis regarding the energy demand #
sheet_exp = 1
heat_dem = q_heat_dem * 3.6
xlswrite(exp_filename,heat_dem,sheet_exp,'b2:b13')
cool_dem = q_cool_dem_c * 3.6
xlswrite(exp_filename,cool_dem,sheet_exp,'c2:c13')
wat_dem = transpose(dq_wat_dem) * 3.6
xlswrite(exp_filename,wat_dem,sheet_exp,'d2:d13')
lighting_dem = transpose(light_dem) * 3.6
xlswrite(exp_filename,lighting_dem,sheet_exp,'e2:e13')
appliances_dem = transpose(app_cons) * 3.6
xlswrite(exp_filename,appliances_dem,sheet_exp,'f2:f13')
xlswrite(exp_filename,slc_gen,sheet_exp,'b18:b29')
xlswrite(exp_filename,pv_gen,sheet_exp,'c18:c29')
xlswrite(exp_filename,primary_heat_m,sheet_exp,'i2:i13')
xlswrite(exp_filename,primary_cool_m,sheet_exp,'j2:j13')
xlswrite(exp_filename,primary_dhw_m,sheet_exp,'k2:k13')
xlswrite(exp_filename,primary_light_m,sheet_exp,'l2:l13')
xlswrite(exp_filename,primary_app_m,sheet_exp,'m2:m13')
xlswrite(exp_filename,f_grid,sheet_exp,'f19')
xlswrite(exp_filename,f_pv,sheet_exp,'f20')