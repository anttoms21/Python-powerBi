#This code is the starting point for data manipulation
import pandas as pd
import json
from pandas.io.json import json_normalize

class Simulations:

    with open("./simulations.json") as my_file:
       file =json.load(my_file)
    #Parsed_data = json.loads("./simulations.json")
    json_normalize(file)
   # print(file[0])


    data = pd.DataFrame(file)
    #print(data.head(1))
    #print(Parsed_data)
    beautiful_data = json.dumps(file, indent=4, sort_keys=True)
    with open('new_sim.json', 'w') as outfile:
        #json.dump(file, indent=4, sort_keys=True)
        json.dump(beautiful_data, outfile)

    data.to_pickle("./simulations.pk1")