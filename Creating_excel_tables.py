import pickle
import pandas as pd
import json
from pandas.io.json import json_normalize
# time script
from datetime import datetime
import os
from pathlib import Path

startTime = datetime.now()


class TableMaker():
    # keep columns names here since they may change in the future and it is good to have only one place to change it.

    BUILDING_TYPE = 'building_type'
    CITY = 'geography.city'
    TEMPLATE = 'template'
    TOTAL_END_USES_GJ_PER_M2 = None
    TOTAL_END_USES_GJ_PER_YEAR = None

    def __init__(self, desired_values_gj_per_year, desired_values_gj_per_m2, url='C:/Users/thotran/Desktop/simulations.json'):
        self.TOTAL_END_USES_GJ_PER_M2 =desired_values_gj_per_m2
        self.TOTAL_END_USES_GJ_PER_YEAR = desired_values_gj_per_year
        pd.set_option('display.max_columns', None)
        with open(url) as f:
            self.json_data = json.load(f)
        # This creates the main table.
        self.main_table = json_normalize(self.json_data)

    def filter_out_rows_by_values(self, column=BUILDING_TYPE, values=['SmallOffice']):
        # reduce dataset by removing rows of buildings we dont want. For example we are removing Outpatient. Oddly in the
        # simulations.json file I am using.. I am missing the Outpatient for 2015/17.. So I am removing it.
        self.main_table.drop(self.main_table[(~self.main_table[column].isin(values))].index, inplace=True)
        return self

    def necb_comparison_table(self, columns=[TOTAL_END_USES_GJ_PER_YEAR ,TOTAL_END_USES_GJ_PER_M2],
                              templates=['NECB2015', 'NECB2017']):
        # https://stackoverflow.com/questions/35268817/unique-combinations-of-values-in-selected-columns-in-pandas-data-frame-and-count
        # Create a table just with cities and building types. Keeping 'count' for now for debugging.
        table = self.main_table.groupby([self.CITY, self.BUILDING_TYPE]).size().reset_index().rename(
            columns={0: 'count'})
        # apply a formula based on a lookup and set it to a new column
        for column in columns:
            for template in templates:
                new_column_name = f"{template}_{column}"
                table[new_column_name] = table.apply(
                    lambda row: self.main_table.loc[
                        (self.main_table[self.TEMPLATE] == template) &
                        (self.main_table[self.BUILDING_TYPE] == row[self.BUILDING_TYPE]) &
                        (self.main_table[self.CITY] == row[self.CITY])
                        ].iloc[0][column], axis=1)
        #print(table)
        return table

    def creating_tables(gj_per_year, gj_per_m2):
        tm = TableMaker(gj_per_year, gj_per_m2)
        #filters by cities you want
        tm.filter_out_rows_by_values(tm.BUILDING_TYPE, ['SmallOffice',
                                                        'MediumOffice',
                                                        'LargeOffice',
                                                        'RetailStandalone',
                                                        'RetailStripmall',
                                                        'MidriseApartment',
                                                        'HighriseApartment'
                                                        ])

        #Filters by buildings you want.
        tm.filter_out_rows_by_values(tm.CITY, ['Abbotsford Intl AP'])#replace with cities


        # This creates a table with necb201x values in columns rather than rows.
        # the first arguement is the column from the simulations.json top level down, you can add more as you need.. the second is the vintages you want in the table.
        # You can have a single vintage if you want to have a table like 4.3.3.a
        comparison_table = tm.necb_comparison_table(['end_uses_eui.total_end_uses_gj_per_m2'],['NECB2015', 'NECB2017'])
        # You should be able to rename the columns after the table is created to be pretty.
        return comparison_table

wanted_values_gj = []
wanted_values_gj_per_m2 = []

output = pd.ExcelWriter('C:/Users/thotran/Desktop/panda_simple.xlsx', engine = 'xlsxwriter')
my_file = Path('C:/Users/thotran/Desktop/panda_simple.xlsx')
if my_file.is_file():
    os.remove('C:/Users/thotran/Desktop/panda_simple.xlsx')
comparison_table.to_excel(output, sheet_name = 'NECB2011')
output.close()

