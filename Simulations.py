# This code is the starting point for data manipulation
import pandas as pd
import json
from pandas.io.json import json_normalize


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
    for i in file.size:
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
    print(wanted_data)


# data.to_pickle("./simulations.pickle")


Heating = Traverse_for_GJ('heating_gj', "heating_gj_per_m2")
Cooling = Traverse_for_GJ('cooling_gj', 'cooling_gj_per_m2')
