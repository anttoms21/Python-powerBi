# This code is the starting point for data manipulation
#Thomas Tran
import pandas as pd
import json
from pandas.io.json import json_normalize
import xlsxwriter
import os
from pathlib import Path


def Traverse_for_GJ(variable_name_gj, variable_name_gj_per_m2):
    with open("./simulations.json") as my_file:
        file = json.load(my_file)

    json_normalize(file)
    data = pd.DataFrame(file)  # DataFrame for the entire simulations.json

    # starting to get information
    city = []
    template = []
    building_type = []
    energy_used_gj = []
    energy_used_gj_per_m2 = []
    # print(city)
    print(len(file))
    #raise ('hell')
    for i in range(0, len(file)):
        city.append(file[i]['geography']['city'])
        template.append(file[i]['template'])
        building_type.append(file[i]['measures'][0]['arguments']['building_type'])
        energy_used_gj.append(file[i]['end_uses'][variable_name_gj])
        energy_used_gj_per_m2.append(file[i]['end_uses_eui'][variable_name_gj_per_m2])

    wanted_data = pd.DataFrame({
        'city': city,
        'template': template,
        'building_type': building_type,
        str(variable_name_gj): energy_used_gj,
        str(variable_name_gj_per_m2): energy_used_gj_per_m2
    })
   # print(wanted_data)
    return wanted_data

# data.to_pickle("./simulations.pickle")


Heating = Traverse_for_GJ('heating_gj', "heating_gj_per_m2")
Cooling = Traverse_for_GJ('cooling_gj', 'cooling_gj_per_m2')
NECB2011 = Heating['template'] == 'NECB2011'
df2011 = Heating[NECB2011]
NECB2015 = Heating['template'] == 'NECB2015'
df2015 = Heating[NECB2015]
NECB2017 = Heating['template'] == 'NECB2017'
df2017 = Heating[NECB2017]
new_df= df2011.merge(df2015, left_on= 'city' & 'building_type', right_on= 'city' & 'building_type')
#print(df2011)
#raise('break')
#checking if file exists and creating a new file with the desired excel materials
output = pd.ExcelWriter('C:/Users/thotran/Desktop/panda_simple.xlsx', engine = 'xlsxwriter')
my_file = Path('C:/Users/thotran/Desktop/panda_simple.xlsx')
if my_file.is_file():
    os.remove('C:/Users/thotran/Desktop/panda_simple.xlsx')
df2011.to_excel(output, sheet_name = 'NECB2011')
df2015.to_excel(output, sheet_name = 'NECB2015')
df2017.to_excel(output, sheet_name = 'NECB2017')
output.close()