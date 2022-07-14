##A script for the calculation of energy demand for a specific x solution
print('\\n' % ())
print('You can insert a x vector for the calculation of energy demand.' % ())
print('\\nand primary energy consumption' % ())
print('\\n' % ())
print('\\nThe x solutions are stored in the variable x_min_global' % ())
print('\\nand each column represents a vector, with the first being' % ())
print('\\nfor p1=1 and the last for p1=0. For example if you want to' % ())
print('\\nto see the energy demand for p1=1 the x vector would be:' % ())
print('\\nx_min_global(:,1). The energy demand before the retrofit' % ())
print('\\nis already located in the export file.' % ())
print('\\n' % ())
x_demand = input_('\\nInsert the x vector of the case you are interested: ')
#Calling the primary energy function
energy_demand = Retrofit_Building_Primary_Energy_Function(x_demand)
#File for exporting the results
exp_filename = 'Energy Consumption Results.xlsx'
#Exporting Data to Excel for analysis regarding the energy demand #
sheet_exp = 1
heat_dem = q_heat_dem * 3.6
xlswrite(exp_filename,heat_dem,sheet_exp,'b20:b31')
cool_dem = q_cool_dem_c * 3.6
xlswrite(exp_filename,cool_dem,sheet_exp,'c20:c31')
wat_dem = transpose(dq_wat_dem)
xlswrite(exp_filename,wat_dem,sheet_exp,'d20:d31')
lighting_dem = transpose(light_dem) * 3.6
xlswrite(exp_filename,lighting_dem,sheet_exp,'e20:e31')
appliances_dem = transpose(app_cons) * 3.6
xlswrite(exp_filename,appliances_dem,sheet_exp,'f20:f31')
xlswrite(exp_filename,slc_gen,'b36:b47')
xlswrite(exp_filename,pv_gen,'c36:c47')
xlswrite(exp_filename,primary_heat_m,sheet_exp,'i20:i31')
xlswrite(exp_filename,primary_cool_m,sheet_exp,'j20:j31')
xlswrite(exp_filename,primary_dhw_m,sheet_exp,'k20:k31')
xlswrite(exp_filename,primary_light_m,sheet_exp,'l20:l31')
xlswrite(exp_filename,primary_app_m,sheet_exp,'m20:m31')
xlswrite(exp_filename,f_grid,sheet_exp,'f37')
xlswrite(exp_filename,f_pv,sheet_exp,'f38')