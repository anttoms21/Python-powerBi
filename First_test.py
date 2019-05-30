# This code is used to test if python will work with power BI (It was a sucess)
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import json

#def Calculations(input_JSON_FILE):
#    with open(input_JSON_FILE) as my_file:
#        file =json.load(my_file)
#    print(file)
#    with open ('Output.json', 'w') as outfile:
#        json.dump(file, outfile, sort_keys=True, indent= 4)


#x = Calculations('btap-tester.json')


data = pd.DataFrame({
   'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ],
   'Days in Month': ['31', '28' , '31' , '30', '31', '30', '31','31', '30', '31', '30', '31']
})

print(data)