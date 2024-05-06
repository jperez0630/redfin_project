import duckdb
from pathlib import Path
import pandas as pd
import plotly.express as px

# def get_target_directory(target_directory):
#     current_directory = Path.cwd()
#     target_directory = f'{current_directory}\\{target_directory}'
#     return target_directory

# target_directory = get_target_directory('redfin_real_estate_data')




# con = duckdb.connect(f'{Path.cwd()}/redfin_real_estate_data.duckdb')
# local_con = con.cursor()
# local_con.query('INSTALL httpfs')
# local_con.query('LOAD httpfs')
# local_con.query('''
#                 CREATE TABLE housing_info AS SELECT
#                 period_end,
#                 region as "postal_code",
#                 state,
#                 state_code,
#                 property_type,
#                 median_sale_price,
#                 median_ppsf,
#                 homes_sold

#                 FROM read_csv_auto(
#                 'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz') 
#                 --WHERE period_end >= CURRENT_DATE - 365
#                 WHERE property_type != 'All Residential'
#                 ''')

con = duckdb.connect(f'{Path.cwd()}/redfin_real_estate_data.duckdb')
local_con = con.cursor()

#Importing CSV FILE
df = pd.read_csv(
    'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz', delimiter = '\t', 
    #'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/zip_code_market_tracker.tsv000.gz', delimiter = '\t',
    usecols=[
        'period_end',
        'state',
        'property_type',
        'median_sale_price',
        'median_ppsf',
        'homes_sold'
    ],
    parse_dates=['period_end', 'period_end']
)
 
#Filtering out All Residential
df_filtered = df.loc[df['property_type'] != 'All Residential'].copy()

#df_filtered['U.S_Median_Sale_Price'] = df_filtered.groupby(['period_end', 'property_type'])['median_sale_price'].transform('median')

#Grouping by median_sale_price
df_gb_state_median_sale_price = df_filtered.groupby([
    'period_end',
    'state',
    'property_type'
])['median_sale_price'].median().reset_index()


#Find the Median Sale Price of homes in the U.S per month
df_median_sale_price_US = df_filtered.groupby(['period_end','property_type'])['median_sale_price'].median().reset_index()
df_median_sale_price_US.insert(2,'state','United States')

#Integrate the U.S Homes Median Sale Price Per Month into the the U.S Median Home Sale Price per satate
df_final_median_sale_price = pd.concat([df_gb_state_median_sale_price, df_median_sale_price_US], axis=0)

#Grouping by ppsf
df_gb_state_median_ppsf = df_filtered.groupby([
    'period_end',
    'state',
    'property_type'
])['median_ppsf'].median().reset_index()

df_median_ppsf_US = df_filtered.groupby(['period_end','property_type'])['median_ppsf'].median().reset_index()
df_median_ppsf_US.insert(2,'state','United States')

#Integrate the U.S Homes Median PPSF Per Month into the the U.S Median PPSF per state data set
df_final_median_ppsf = pd.concat([df_gb_state_median_ppsf, df_median_ppsf_US], axis=0)

#Grouping by Homes sold
df_gb_state_homes_sold = df_filtered.groupby([
    'period_end',
    'state',
    'property_type'
])['homes_sold'].median().reset_index()

#Find the Median Homes Sold in the U.S per month
df_homes_sold_US = df_filtered.groupby(['period_end','property_type'])['homes_sold'].sum().reset_index()
df_homes_sold_US.insert(2,'state','United States')


#Integrate the U.S Median Homes Sold Per Month into the Median Home Sold Per state
df_final_homes_sold = pd.concat([df_gb_state_homes_sold, df_homes_sold_US], axis=0)

#Merge the median_price homes sold data set (Used for the scatter plot)
df_merge_price_homes_sold = pd.merge(
    left = df_final_median_sale_price,
    right = df_final_homes_sold,
    how = 'inner',
    left_on = ['period_end', 'state','property_type'],
    right_on = ['period_end', 'state','property_type']
)

#Filters the df_merge_price_homes_sold so that it only includes the most recent time period
df_merge_price_homes_sold_final = df_merge_price_homes_sold.loc[(
    df_merge_price_homes_sold[
        'period_end'
    ] == df_merge_price_homes_sold['period_end'].max()
)
&
(
    df_merge_price_homes_sold[
        'state'
    ] != 'United_States'
)
]


# fig = px.scatter(df_merge_price_homes_sold.loc[(df_merge_price_homes_sold['state']!='United States') & (df_merge_price_homes_sold['property_type'].str.contains('Single')) & (df_merge_price_homes_sold['period_end']==df_merge_price_homes_sold['period_end'].max())], x="median_sale_price", y="homes_sold", color="state", hover_name="state", facet_col="property_type", log_x=True)
# fig.update_layout(title='Median Sale Price vs. Median Homes Sold', xaxis_title='Median Sale Price', yaxis_title='Median Homes Sold')
# fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='black')
# fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
# fig.show()


# local_con.sql('''
# CREATE TABLE median_sale_price_per_state AS 
# SELECT * FROM df_final_median_sale_price
# ''')

# local_con.sql('''
# CREATE TABLE homes_sold_per_state AS 
# SELECT * FROM df_final_homes_sold
# ''')

# local_con.sql('''
# CREATE TABLE combined_price_homes_sold AS
# SELECT * FROM df_merge_price_homes_sold_final
# ''')

local_con.sql('''
CREATE TABLE median_ppsf_per_state AS
SELECT * FROM df_final_median_ppsf
''')


# local_con.sql('DROP median_sale_price_per_state')
# local_con.sql('Drop homes_sold_per_state)




df_filtered.to_parquet('redfin_real_estate_data.parquet', compression='gzip')

con = duckdb.connect(f'{Path.cwd()}/redfin_real_estate_data.duckdb')
local_con = con.cursor()
# local_con.query('INSTALL httpfs')
# local_con.query('LOAD httpfs')
local_con.query('''
                CREATE TABLE housing_info AS SELECT
                period_end,
                region as "postal_code",
                state,
                property_type,
                median_sale_price,
                median_ppsf,
                homes_sold

                FROM read_parquet(
                'C:\\Users\\jspre\\projects\\redfin_project\\sources\\redfin_real_estate_data\\redfin_real_estate_data.parquet'
                ) 
                WHERE period_end >= CURRENT_DATE - 365
                AND property_type != 'All Residential'

                ''')

