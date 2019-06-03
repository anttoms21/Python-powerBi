import pickle
import pandas as pd
import json
from pandas.io.json import json_normalize
#time script
from datetime import datetime
import os
from pathlib import Path
startTime = datetime.now()


url = './simulations.json'
with open(url) as f:
    json_data = json.load(f)
print("Loaded Json file{url}")
print(datetime.now() - startTime)

with open('./json_data.pickle', 'wb') as handle:
    pickle.dump(json_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
print("Saved pickle Json file{url}")
print(datetime.now() - startTime)

with open('./json_data.pickle', 'rb') as handle:
    json_data = pickle.load(handle)
print("loaded pickle Json file{url}")
print(datetime.now() - startTime)

# #create top level dataframe
pd.set_option('display.max_columns', None)
# This creates the main table.
main_table = json_normalize(json_data)
print("Normalized JSON first level")
print(datetime.now() - startTime)

# reduce dataset by removing rows of buildings we dont want. For example we are removing Outpatient. Oddly in the
# simulations.json file I am using.. I am missing the Outpatient for 2015/17.. So I am removing it.
indexNames = main_table[(main_table['building_type'] == 'Outpatient') | (main_table['building_type'] == 'Hospital')].index
main_table.drop(indexNames, inplace=True)
print("Dropped buildings that are not needed from main_table")
print(datetime.now() - startTime)

main_table.to_pickle("./simulations.pickle")
print("Saved Normalized main_table to pickle")
print(datetime.now() - startTime)
# saved to pickle... if we wish to debug.. we can load the pickle file much faster than doing the above
# comment the above and uncommment the command below
# main_table = pd.read_pickle("c:/test/simulations.pickle")

# prints the current columns in main_table
print(list(main_table.columns.values))

#creates a lookup table that is a bit more lightweight with only the location, type, vintage and id. This may be better
# for joins. using the drop command to drop everything but was is in the difference argument.
look_up_table = main_table.copy()
look_up_table.drop(look_up_table.columns.difference(['building_type','geography.city','template','run_uuid']), 1, inplace=True)
print("Create lightweight lookup_table from main_table")
print(datetime.now() - startTime)

# Nested Array Data
# The relational key to the main_table is run_uuid.
# How does this work? The second argument is the json path to the array. The third argument adds columns from the parent..
# in this case the run_uuid, which is the primary key of the main_table. So all these tables *should* link together in PowerBI
# easily.
cost_construction_report_df = json_normalize(json_data, ['costing_information', 'envelope', 'construction_costs'], ['run_uuid'])
print("Created construction report")
print(datetime.now() - startTime)
cost_construction_report_df.to_pickle("./cost_construction_report_df.pickle") #optioanlly save df to pickle
print("saved construction report")
print(datetime.now() - startTime)
cost_lighting_fixtures_report_df = json_normalize(json_data, ['costing_information', 'lighting', 'fixture_report'], ['run_uuid'])
print("created lighting fixtures report")
print(datetime.now() - startTime)
cost_lighting_space_report_df = json_normalize(json_data, ['costing_information', 'lighting', 'space_report'], ['run_uuid'])
print("created lighting space report")
print(datetime.now() - startTime)

cost_plant_equipment_report_df = json_normalize(json_data, ['costing_information', 'heating_and_cooling', 'plant_equipment'], ['run_uuid'])
print("created plant cost report")
print(datetime.now() - startTime)

cost_zonal_systems_report_df = json_normalize(json_data, ['costing_information', 'heating_and_cooling', 'zonal_systems'], ['run_uuid'])
print("created zonal cost report")
print(datetime.now() - startTime)

space_report_df = json_normalize(json_data, ['spaces'],['run_uuid'])
print("created space  report")
print(datetime.now() - startTime)

air_loop_report = json_normalize(json_data, ['air_loops'], ['run_uuid'])
print("created lighting airloop report")
print(datetime.now() - startTime)

# reduce dataset by removing buildings we dont want. For example we are removing Outpatient. Oddly in the
# simulations.json file I am using.. I am missing the Outpatient for 2015/17.. So I am removing it.
indexNames = main_table[main_table['building_type'] == 'Outpatient'].index
main_table.drop(indexNames, inplace=True)
print("Dropped buildings that are not needed from main_table")
print(datetime.now() - startTime)


# Set print output to be wide for debugging.
pd.set_option('display.max_columns', None)
# create a subset of data
subset = main_table[['geography.city', 'building_type', 'template', 'end_uses_eui.total_end_uses_gj_per_m2']]
print("Subset table example completed")
print(datetime.now() - startTime)

# adding a column in dataframe
main_table['new_column'] = main_table[['end_uses_eui.total_end_uses_gj_per_m2']] * 2
print("Adding a new column example")
print(datetime.now() - startTime)

#  Example how to lookup a value(s)...may be other ways. in this case I am finding the row that has building/vintage and getting a value from that.
all_full_service_restaurants_2017 = (main_table.loc[(main_table['template'] == 'NECB2017') & (main_table['building_type'] == 'FullServiceRestaurant') ])
print("Find all FSR example.")
print(datetime.now() - startTime)


# apply a formula based on a lookup and set it to a new column
main_table['difference'] = main_table.apply(lambda row: row['end_uses_eui.total_end_uses_gj_per_m2'] - main_table.loc[
    (main_table['template'] == 'NECB2011') & (main_table['building_type'] == row['building_type']) & (
            main_table['geography.city'] == row['geography.city'])].iloc[0]['end_uses_eui.total_end_uses_gj_per_m2'],
                                            axis=1)
print("Lookup Example.")
print(datetime.now() - startTime)

# lets make a method out of the above...

def get_difference(row, vintage, variable, df):
    lookup_value_row = df.loc[
        (df['template'] == vintage) &
        (df['building_type'] == row['building_type']) &
        (df['geography.city'] == row['geography.city'])
        ]
    if (lookup_value_row.empty):
        print("DataFrame is empty!")
        print(row['building_type'])
        print(row['geography.city'])
    return row[variable] - lookup_value_row.iloc[0][variable]


# let make a percent diff method too.
def get_percent_difference(row, vintage, variable, df):
    lookup_value_row = df.loc[
        (df['template'] == vintage) &
        (df['building_type'] == row['building_type']) &
        (df['geography.city'] == row['geography.city'])
        ]
    if (lookup_value_row.empty):
        print("DataFrame is empty!")
        print(row['building_type'])
        print(row['geography.city'])
    return (row[variable] - lookup_value_row.iloc[0][variable]) / lookup_value_row.iloc[0][variable] * 100.0


# And now, use the method. This is cleaner and easier to apply to other vintages...

main_table['difference_necb2011.total_end_uses_gj_per_m2'] = main_table.apply(lambda row: get_difference(row,
                                                                                                         'NECB2011',
                                                                                                         'end_uses_eui.total_end_uses_gj_per_m2',
                                                                                                         main_table),
                                                                              axis=1)
print("Example difference_necb2011.total_end_uses_gj_per_m2")
print(datetime.now() - startTime)

main_table['difference_necb2015.total_end_uses_gj_per_m2'] = main_table.apply(lambda row: get_difference(row,
                                                                                                         'NECB2015',
                                                                                                         'end_uses_eui.total_end_uses_gj_per_m2',
                                                                                                         main_table),
                                                                              axis=1)
print("Example difference_necb2015.total_end_uses_gj_per_m2")
print(datetime.now() - startTime)

main_table['percent_difference_necb2017.total_end_uses_gj_per_m2'] = main_table.apply(
    lambda row: get_percent_difference(row,
                                       'NECB2017',
                                       'end_uses_eui.total_end_uses_gj_per_m2',
                                       main_table), axis=1)
print("Example percent_difference_necb2017.total_end_uses_gj_per_m2")
print(datetime.now() - startTime)
#print(main_table[['difference_necb2011.total_end_uses_gj_per_m2','difference_necb2015.total_end_uses_gj_per_m2','percent_difference_necb2017.total_end_uses_gj_per_m2']])
#print(main_table[['costing_information.envelope.construction_costs']])

print(datetime.now() - startTime)