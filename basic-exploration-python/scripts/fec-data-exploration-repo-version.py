#!/usr/bin/env python
"""
This file provides summaries and plots for the entire
2012 US Presidential donation dataset from the FEC.
The ultimate dataset contains data only from the
Obama and Romney campaigns.
Several summaries are produced,
including a dataset with geographic and 
demographic information in each row as well as
time series friendly datasets.


FEC data exploration and setup
1. importation of data
2. mapping useful values for summaries and CSV files
3. exploration of donations
4. exploration of expenditures
5. time series plots (interesting dates)
6. writing CSV files for importation into R:
   (breakout detection, time series plots, chloropleth maps with Google API)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os


#------------------------------------------------------------------------------ 
# import data from CSV files

# FEC donations and expenditure data

# file paths have been omitted (2012 FEC dat is on local drive)

fec_data_head = \
  pd.read_csv('P00000001-ALL.csv',  index_col = False, nrows = 10)
fec_data_cols = fec_data_head.columns.values.tolist()

fec_chunker = \
  pd.read_csv('/P00000001-ALL.csv', index_col = False, low_memory = False, 
              chunksize = 100000)

fec_data = pd.DataFrame()

for piece in fec_chunker:
    fec_data = fec_data.append(piece)

fec_data.shape
fec_data.head()

# 2010 census data;
# already downloaded to local drive

population_data = \
  pd.read_csv('pop_density.csv', index_col = False, skiprows = [0, 1, 2])

# popular vote totals by state
# entered manually from PDF
vote_total = pd.read_csv('popular-vote-totals.csv')

# census data
state_population_data = pd.read_csv('state-population-2010-census.csv')

elderly_population_data = pd.read_csv('elderly-population-state-2010.csv')

family_population_data = pd.read_csv('family-census-data-2010.csv')

#------------------------------------------------------------- 
# dicts to map descriptives

# name:party dict
parties = {"Romney, Mitt" : "Republican", "Obama, Barack" : "Democrat"}
           
# state:region dicts (census and economic bureau regions)

# census regions
census_regions = {'CT': 'Northeast', 'ME': 'Northeast', 'MA': 'Northeast',
                  'NH': 'Northeast', 'RI': 'Northeast', 'VT': 'Northeast',
                  'NJ': 'Northeast', 'NY': 'Northeast', 'PA': 'Northeast',
                  'IL':'Midwest', 'IN':'Midwest', 'MI':'Midwest', 'OH':'Midwest',
                  'WI':'Midwest', 'IA':'Midwest', 'KS':'Midwest', 'MN':'Midwest',
                  'NE':'Midwest', 'ND':'Midwest', 'SD':'Midwest', 'MO':'Midwest',
                  'DE':'South', 'FL':'South', 'GA':'South', 'MD':'South', 
                  'NC':'South', 'SC':'South', 'VA':'South', 'DC':'South',
                  'WV':'South', 'AL':'South', 'KY':'South', 'MS':'South', 
                  'TN':'South', 'AR':'South', 'LA':'South', 'OK':'South', 
                  'TX':'South','AZ':'West', 'CO':'West', 'ID':'West', 'MT':'West',
                  'NV':'West', 'NM':'West', 'UT':'West', 'WY':'West', 'AK':'West',
                  'CA':'West','HI':'West', 'OR':'West', 'WA':'West'}
           
economic_regions = {'CT': 'New England', 'ME': 'New England', 'MA': 'New England',
                  'NH': 'New England', 'RI': 'New England', 'VT': 'New England',
                  'NJ': 'Mideast', 'NY': 'Mideast', 'PA': 'Mideast', 'DE':'Mideast',
                  'DC':'Mideast', 'MD':'Mideast', 'IL':'Great Lakes', 
                  'IN':'Great Lakes', 'MI':'Great Lakes', 'OH':'Great Lakes',
                  'WI':'Great Lakes', 'IA':'Plains', 'KS':'Plains', 'MN':'Plains',
                  'MO':'Plains', 'NE':'Plains', 'ND':'Plains', 'SD':'Plains',
                  'FL':'Southeast', 'GA':'Southeast', 'AL':'Southeast', 
                  'AR':'Southeast',  'NC':'Southeast', 'SC':'Southeast', 
                  'VA':'Southeast', 'WV':'Southeast', 'KY':'Southeast',
                  'MS':'Southeast', 'TN':'Southeast', 'LA':'Southeast', 
                  'OK':'Southwest', 'TX':'Southwest', 'AZ':'Southwest',
                  'NM':'Southwest','CO':'Rocky Mountain', 'ID':'Rocky Mountain', 
                  'MT':'Rocky Mountain', 'UT':'Rocky Mountain', 'WY':'Rocky Mountain',
                  'NV':'Far West','AK':'Far West', 'CA':'Far West',
                  'HI':'Far West', 'OR':'Far West', 'WA':'Far West'}

# full names of states (for chloropleth map in R)
state_names = {'CT': 'Connecticut', 'ME': 'Maine', 'MA': 'Massachusetts',
                  'NH': 'New Hampshire', 'RI': 'Rhode Island', 'VT': 'Vermont',
                  'NJ': 'New Jersey', 'NY': 'New York', 'PA': 'Pennsylvania',
                  'IL':'Illinois', 'IN':'Indiana', 'MI':'Michigan', 'OH':'Ohio',
                  'WI':'Wisconsin', 'IA':'Iowa', 'KS':'Kansas', 'MN':'Minnesota',
                  'NE':'Nebraska', 'ND':'North Dakota', 'SD':'South Dakota', 
                  'MO':'Missouri','DE':'Delaware', 'FL':'Florida', 'GA':'Georgia',
                  'MD':'Maryland', 'NC':'North Carolina', 'SC':'South Carolina', 
                  'VA':'Virginia', 'WV':'West Virginia', 'AL':'Alabama',
                  'KY':'Kentucky', 'MS':'Mississippi', 
                  'TN':'Tennessee', 'AR':'Arkansas', 'LA':'Louisiana', 
                  'OK':'Oklahoma', 'TX':'Texas', 'AZ':'Arizona', 'CO':'Colorado',
                  'ID':'Idaho', 'MT':'Montana', 'NV':'Nevada', 'NM':'New Mexico',
                  'UT':'Utah', 'WY':'Wyoming', 'AK':'Alaska', 
                  'CA':'California', 'HI':'Hawaii', 'OR':'Oregon', 'WA':'Washington'}           
           
           
# number of electoral college votes by state
state_votes = {'CT': 7, 'ME': 4, 'MA': 11,'NH': 4, 'RI': 4, 'VT': 3,
                  'NJ': 14, 'NY': 29, 'PA': 20,'IL':20, 'IN':11, 'MI':16, 'OH':18,
                  'WI':10, 'IA':6, 'KS':6, 'MN':10,'NE':5, 'ND':3, 'SD':3, 'MO':10,
                  'DE':3, 'FL':29, 'GA':16, 'MD':10, 'NC':15, 'SC':9, 'VA':13,
                  'WV':5, 'AL':9, 'KY':8, 'MS':6,  'TN':11, 'AR':6, 'LA':8, 'OK':7, 
                  'TX':38, 'AZ':11, 'CO':9, 'ID':4, 'MT':3, 'NV':6, 'NM':5, 'UT':6, 
                  'WY':3, 'AK':3,'CA':55, 'HI':4, 'OR':7, 'WA':12}


# population by state (2010 census), votes and winner (mapped to fec_data)
population_data = \
  population_data[population_data.STATE_OR_REGION.isin(state_names.values())]

# set state names as indices in DataFrame
population_data.set_index(population_data.STATE_OR_REGION, \
                          inplace = True, drop = True)

vote_total.set_index(vote_total.State, inplace = True, drop = True)

state_population_data.set_index(state_population_data.State, \
                                inplace = True, drop = True)

elderly_population_data.set_index(elderly_population_data.State, \
                                  inplace = True, drop = True)

family_population_data.set_index(family_population_data.State, \
                                 inplace = True, drop = True)

# isolating 2010 population results
state_pop_dict = {}

for state in population_data.STATE_OR_REGION:
    state_pop_dict[state] = population_data.loc[state, '2010_POPULATION']
    
state_density_dict = {}

for state in population_data.STATE_OR_REGION:
    state_density_dict[state] = population_data.loc[state, '2010_DENSITY']
    
# mapping vote totals and winners to states
obama_vote_dict = {}
romney_vote_dict = {}
winner_dict = {}

vote_total.set_index(vote_total.State, inplace = True, drop = True)

for state in vote_total.State:
    obama_vote_dict[state] = vote_total.loc[state, 'Obama']
 
for state in vote_total.State:
    romney_vote_dict[state] = vote_total.loc[state, 'Romney']

for state in vote_total.State:
    winner_dict[state] = vote_total.loc[state, 'Winner']
    
# mapping population demographics to states

# creating dicts
male_pop = {}
female_pop = {}
sex_ratio = {}
under_18_count = {}
under_18_pct = {}
eighteen_to_forty_four_count = {}
eighteen_to_forty_four_pct = {}
forty_five_to_sixty_four_count = {}
forty_five_to_sixty_four_pct = {}
sixty_five_over_count = {}
sixty_five_over_pct = {}
median_age = {}

eighty_five_over_count = {}
eighty_five_over_pct = {}

total_households = {}
husband_wife = {}
husband_wife_child_under_18 = {}
female_household = {}
female_household_child_under_18 = {}
male_household = {}
male_household_child_under_18 = {}
one_person_non_family = {}
one_person_sixty_five_older = {}
one_person_at_least_two = {}
avg_per_household = {}
avg_per_family = {}

# putting state values in dicts
for state in state_population_data.State:
    male_pop[state] = state_population_data.loc[state, 'Male']
    
for state in state_population_data.State:
    female_pop[state] = state_population_data.loc[state, 'Female']

for state in state_population_data.State:
    sex_ratio[state] = state_population_data.loc[state, 'SexRatio']

for state in state_population_data.State:
    under_18_count[state] = state_population_data.loc[state, 'Under18Count']

for state in state_population_data.State:
    under_18_pct[state] = state_population_data.loc[state, 'Under18Pct']

for state in state_population_data.State:
    eighteen_to_forty_four_count[state] = \
    state_population_data.loc[state, 'EighteentoFortyFourCount']

for state in state_population_data.State:
    eighteen_to_forty_four_pct[state] = \
    state_population_data.loc[state, 'EighteentoFortyFourPct']

for state in state_population_data.State:
    forty_five_to_sixty_four_count[state] = \
    state_population_data.loc[state, 'FortyFivetoSixtyFourCount']

for state in state_population_data.State:
    forty_five_to_sixty_four_pct[state] = \
    state_population_data.loc[state, 'FortyFivetoSixtyFourPct']
    
for state in state_population_data.State:
    sixty_five_over_count[state] = \
    state_population_data.loc[state, 'SixtyFiveOverCount']
    
for state in state_population_data.State:
    sixty_five_over_pct[state] = \
    state_population_data.loc[state, 'SixtyFiveOverPct']

for state in state_population_data.State:
    median_age[state] = state_population_data.loc[state, 'MedianAge']
    
for state in elderly_population_data.State:
    eighty_five_over_count[state] = \
    elderly_population_data.loc[state, 'EightyFiveOverCount']

for state in elderly_population_data.State:
    eighty_five_over_pct[state] = \
    elderly_population_data.loc[state, 'EightyFiveOverPct']    

for state in family_population_data.State:
    total_households[state] = family_population_data.loc[state, 'TotalHouseholds']

for state in family_population_data.State:
    husband_wife[state] = family_population_data.loc[state, 'HusbandWifeHousehold']

for state in family_population_data.State:
    husband_wife_child_under_18[state] = \
    family_population_data.loc[state, 'HusbandWifeUnder18Children']
    
for state in family_population_data.State:
    female_household[state] = family_population_data.loc[state, 'FemaleHousehold']

for state in family_population_data.State:
    female_household_child_under_18[state] = \
    family_population_data.loc[state, 'FemaleHouseholdUnder18']

for state in family_population_data.State:
    male_household[state] = \
    family_population_data.loc[state, 'MaleHousehold']

for state in family_population_data.State:
    male_household_child_under_18[state] = \
    family_population_data.loc[state, 'MaleHouseholdUnder18']


for state in family_population_data.State:
    one_person_non_family[state] = \
    family_population_data.loc[state, 'OnePersonNonFamily']

for state in family_population_data.State:
    one_person_sixty_five_older[state] = \
    family_population_data.loc[state, 'OnePersonSixtyFiveOlder']

for state in family_population_data.State:
    one_person_at_least_two[state] = \
    family_population_data.loc[state, 'OnePersonTwoOrMore']

for state in family_population_data.State:
    avg_per_household[state] = family_population_data.loc[state, 'AvgPerHousehold']

for state in family_population_data.State:
    avg_per_family[state] = family_population_data.loc[state, 'AvgPerFamily']

#------------------------------------------------------------------------------ 
# mapping data using above dictionaries (new columns created)
         
fec_data['party'] = fec_data.cand_nm.map(parties)
fec_data['census_region'] = fec_data.contbr_st.map(census_regions)
fec_data['economic_region'] = fec_data.contbr_st.map(economic_regions)
fec_data['state_name'] = fec_data.contbr_st.map(state_names)
fec_data['electoral_votes'] = fec_data.contbr_st.map(state_votes)
fec_data['population'] = fec_data.state_name.map(state_pop_dict)
fec_data['pop_density'] = fec_data.state_name.map(state_density_dict)
fec_data['winner'] = fec_data.contbr_st.map(winner_dict)
fec_data['obama_total'] = fec_data.contbr_st.map(obama_vote_dict)
fec_data['romney_total'] = fec_data.contbr_st.map(romney_vote_dict)

fec_data['males'] = fec_data.state_name.map(male_pop)
fec_data['females'] = fec_data.state_name.map(female_pop)
fec_data['sex_ratio'] = fec_data.state_name.map(sex_ratio)
fec_data['under_18_count'] = fec_data.state_name.map(under_18_count)
fec_data['under_18_pct'] = fec_data.state_name.map(under_18_pct)
fec_data['eighteen_to_forty_four_count'] = fec_data.state_name.map(eighteen_to_forty_four_count)
fec_data['eighteen_to_forty_four_pct'] = fec_data.state_name.map(eighteen_to_forty_four_pct)
fec_data['forty_five_to_sixty_four_count'] = fec_data.state_name.map(forty_five_to_sixty_four_count)
fec_data['forty_five_to_sixty_four_pct'] = fec_data.state_name.map(forty_five_to_sixty_four_pct)
fec_data['sixty_five_over_count'] = fec_data.state_name.map(sixty_five_over_count)
fec_data['sixty_five_over_pct'] = fec_data.state_name.map(sixty_five_over_pct)
fec_data['median_age'] = fec_data.state_name.map(median_age)

fec_data['total_households'] = fec_data.state_name.map(total_households)
fec_data['husband_wife_household'] = fec_data.state_name.map(husband_wife)
fec_data['husband_wife_child_under_18'] = fec_data.state_name.map(husband_wife_child_under_18)
fec_data['female_household'] = fec_data.state_name.map(female_household)
fec_data['female_child_under_18'] = fec_data.state_name.map(female_household_child_under_18)
fec_data['male_household'] = fec_data.state_name.map(male_household)
fec_data['male_child_under_18'] = fec_data.state_name.map(male_household_child_under_18)
fec_data['one_person_nonfamily'] = fec_data.state_name.map(one_person_non_family)
fec_data['one_person_sixty_five_older'] = fec_data.state_name.map(one_person_sixty_five_older)
fec_data['one_person_at_least_two'] = fec_data.state_name.map(one_person_at_least_two)
fec_data['avg_per_family'] = fec_data.state_name.map(avg_per_family)
fec_data['avg_per_household'] = fec_data.state_name.map(avg_per_household)

fec_data['eighty_five_over_count'] = fec_data.state_name.map(eighty_five_over_count)
fec_data['eighty_five_over_pct'] = fec_data.state_name.map(eighty_five_over_pct)



# converting date to y-m-d format
fec_data['contb_receipt_dt_format'] = \
  pd.to_datetime(fec_data.contb_receipt_dt, format = '%d-%b-%y')

#------------------------------------------------------------------------------ 
# create final datasets

# restrict to obama and romney and 50 states + DC
states = census_regions.keys()
fec_final = fec_data[fec_data.contbr_st.isin(states)]
fec_final = fec_final[fec_final.cand_nm.isin(['Obama, Barack','Romney, Mitt'])]


# free up memory
del fec_data 
del population_data

# donation data (positive amounts)
donations = fec_final[fec_final.contb_receipt_amt > 0]

# expenditures (negative amounts)
expenditures = fec_final[fec_final.contb_receipt_amt < 0]


#------------------------------------------------------------------------------ 
# donation summary statistics

# cut into discrete groups based on amount contributed
donations['donor_size'] = \
pd.cut(donations.loc[:,'contb_receipt_amt'], right = True, include_lowest = True,
       bins = np.array([0, 1e2, 1e3, 1e4, 1e5]),
       labels = np.array(['micro', 'small', 'medium', 'large']))

# summaries and plots for each group and interaction

# by census region
cand_census_size = \
  donations.groupby(['cand_nm', 'census_region']).size().unstack(0)
  
cand_census_pct = cand_census_size.div(cand_census_size.sum(axis = 1), axis = 0)

pylab.show(cand_census_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of donations by Census Bureau region'))

# by economic region
cand_economic_size = \
  donations.groupby(['cand_nm', 'economic_region']).size().unstack(0)
  
cand_economic_pct = cand_economic_size.div(cand_economic_size.sum(axis = 1), 
                                           axis = 0)
                                           
pylab.show(cand_economic_pct.plot(kind = 'barh', stacked = False, 
      title = 'Proportion of donations by Bureau of Economic Analysis region'))

# by state
cand_state_size = \
  donations.groupby(['cand_nm', 'contbr_st']).size().unstack(0)
  
cand_state_pct = cand_state_size.div(cand_state_size.sum(axis = 1), axis = 0)

pylab.show(cand_state_pct.plot(kind = 'bar', stacked = False, 
                     title = 'Proportion of donations by state'))

# by donor size
cand_donor_size = \
  donations.groupby(['cand_nm', 'donor_size']).size().unstack(0)
  
cand_donor_pct = cand_donor_size.div(cand_donor_size.sum(axis = 1), axis = 0)

pylab.show(cand_donor_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of donations by Donor group'))

# census by state
census_state_size = \
  donations.groupby(['census_region', 'contbr_st']).size().unstack(0)
  
census_state_pct = census_state_size.div(census_state_size.sum(axis = 1), axis = 0)

pylab.show(census_state_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of donations by Census Bureau region'))

# economic by state
economic_region_state_size = \
  donations.groupby(['economic_region', 'contbr_st']).size().unstack(0)
  
economic_state_pct = \
economic_region_state_size.div(economic_region_state_size.sum(axis = 1), axis = 0)

pylab.show(economic_region_state_size.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of donations by Economic region'))

# donor by state
donor_state_size = \
  donations.groupby(['donor_size', 'contbr_st']).size().unstack(0)
  
donor_state_pct = \
donor_state_size.div(donor_state_size.sum(axis = 1), axis = 0)

# donor by census
donor_census_region_size = \
  donations.groupby(['donor_size', 'census_region']).size().unstack(0)
  
donor_census_region_pct = \
donor_census_region_size.div(donor_census_region_size.sum(axis = 1), axis = 0)

pylab.show(donor_census_region_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Donor size distribution by Census region'))
                     
# donor by economic
donor_economic_region_size = \
  donations.groupby(['donor_size', 'economic_region']).size().unstack(0)
  
donor_economic_region_pct = \
donor_economic_region_size.div(donor_economic_region_size.sum(axis = 1), axis = 0)

pylab.show(donor_economic_region_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Donor size distribution by Economic region'))


# candidate, donor, economic region
cand_donor_economic_region_size = \
  donations.groupby(['cand_nm','donor_size', 'economic_region']).size().unstack(0)
  
cand_donor_economic_region_pct = \
cand_donor_economic_region_size.div(cand_donor_economic_region_size.sum(axis = 1), axis = 0)

# candidate, donor, census region
cand_donor_census_region_size = \
  donations.groupby(['cand_nm','donor_size', 'census_region']).size().unstack(0)
  
cand_donor_census_region_pct = \
cand_donor_census_region_size.div(cand_donor_census_region_size.sum(axis = 1), axis = 0)


#------------------------------------------------------------------------------ 
#expenditure summary statistics

# get absolute value of expenditures
expenditures['expend_amt'] = expenditures['contb_receipt_amt'].abs()

# cut into discrete groups based on amount contributed
expenditures.loc[:,'payment_size'] = \
pd.cut(expenditures['expend_amt'], right = True, include_lowest = True,
       bins = np.array([0, 1e2, 1e3, 1e4, 1e5]),
       labels = np.array(['micro', 'small', 'medium', 'large']))

# summaries and plots for each group and interaction
# want histograms and summaries

# by census region
expend_cand_census_size = \
  expenditures.groupby(['cand_nm', 'census_region']).size().unstack(0)
  
expend_cand_census_pct = \
expend_cand_census_size.div(expend_cand_census_size.sum(axis = 1), axis = 0)

pylab.show(expend_cand_census_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of expenditures by Census Bureau region'))

# by economic region
expend_cand_economic_size = \
  expenditures.groupby(['cand_nm', 'economic_region']).size().unstack(0)
  
expend_cand_economic_pct = \
expend_cand_economic_size.div(expend_cand_economic_size.sum(axis = 1), axis = 0)
                                           
pylab.show(expend_cand_economic_pct.plot(kind = 'barh', stacked = False, 
      title = 'Proportion of expenditures by Bureau of Economic Analysis region'))

# by state
expend_cand_state_size = \
  expenditures.groupby(['cand_nm', 'contbr_st']).size().unstack(0)
  
expend_cand_state_pct = \
expend_cand_state_size.div(expend_cand_state_size.sum(axis = 1), axis = 0)

pylab.show(expend_cand_state_pct.plot(kind = 'bar', stacked = False, 
                     title = 'Proportion of expenditures by state'))

# by payment size
cand_payment_size = \
  expenditures.groupby(['cand_nm', 'payment_size']).size().unstack(0)
  
cand_payment_pct = cand_payment_size.div(cand_payment_size.sum(axis = 1), axis = 0)

pylab.show(cand_payment_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of expenditures by payment group'))

# census by state
expend_census_state_size = \
  expenditures.groupby(['census_region', 'contbr_st']).size().unstack(0)
  
expend_census_state_pct = \
expend_census_state_size.div(expend_census_state_size.sum(axis = 1), axis = 0)

pylab.show(expend_census_state_pct.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of expenditures by Census Bureau region'))

# economic by state
expend_economic_region_state_size = \
  expenditures.groupby(['economic_region', 'contbr_st']).size().unstack(0)
  
expend_economic_state_pct = \
expend_economic_region_state_size.div(expend_economic_region_state_size.sum(axis = 1), axis = 0)

pylab.show(expend_economic_region_state_size.plot(kind = 'barh', stacked = False, 
                     title = 'Proportion of expenditures by Economic region'))

# payment by state
payment_state_size = \
  expenditures.groupby(['payment_size', 'contbr_st']).size().unstack(0)
  
payment_state_pct = \
payment_state_size.div(payment_state_size.sum(axis = 1), axis = 0)

# payment by census
payment_census_region_size = \
  expenditures.groupby(['payment_size', 'census_region']).size().unstack(0)
  
payment_census_region_pct = \
payment_census_region_size.div(payment_census_region_size.sum(axis = 1), axis = 0)

pylab.show(payment_census_region_pct.plot(kind = 'barh', stacked = False, 
                     title = 'payment size distribution by Census region'))
                     
# payment by economic
payment_economic_region_size = \
  expenditures.groupby(['payment_size', 'economic_region']).size().unstack(0)
  
payment_economic_region_pct = \
payment_economic_region_size.div(payment_economic_region_size.sum(axis = 1), axis = 0)

pylab.show(payment_economic_region_pct.plot(kind = 'barh', stacked = False, 
                     title = 'payment size distribution by Economic region'))


# candidate, payment, economic region
cand_payment_economic_region_size = \
  expenditures.groupby(['cand_nm','payment_size', 'economic_region']).size().unstack(0)
  
cand_payment_economic_region_pct = \
cand_payment_economic_region_size.div(cand_payment_economic_region_size.sum(axis = 1), axis = 0)

# candidate, payment, census region
cand_payment_census_region_size = \
  expenditures.groupby(['cand_nm','payment_size', 'census_region']).size().unstack(0)
  
cand_payment_census_region_pct = \
cand_payment_census_region_size.div(cand_payment_census_region_size.sum(axis = 1), axis = 0)

#------------------------------------------------------------------------------ 
# time series plots

# donations

# by candidate
donation_size_cand_time_series = \
donations.groupby(['cand_nm', 'contb_receipt_dt_format']).size().unstack(0)

donation_size_cand_time_series.plot(title = 'Donations during election cycle')
plt.xlabel('Date')
plt.ylabel('Number of donations')
pylab.show()



# since most activity is after the conventions, zoom in from july to november

# census region
donation_size_census_time_series = \
donations.groupby(['census_region', 'contb_receipt_dt_format']).size().unstack(0)

donation_size_census_time_series.ix['07-2012':'12-2012'].plot()
plt.title('Donations during election cycle: census region')
plt.ylabel('Number of donations')
plt.xlabel('Date')
pylab.show()

# economic region
donation_size_economic_time_series = \
donations.groupby(['economic_region', 'contb_receipt_dt_format']).size().unstack(0)

donation_size_economic_time_series.ix['07-2012':'12-2012'].plot()
plt.title('Donations during election cycle: economic region')
plt.ylabel('Number of donations')
plt.xlabel('Date')
pylab.show()

# donor size
donation_size_donor_time_series = \
donations.groupby(['donor_size', 'contb_receipt_dt_format']).size().unstack(0)

donation_size_donor_time_series.ix['07-2012':'12-2012'].plot()
plt.title('Donations during election cycle: donor size')
plt.ylabel('Number of donations')
plt.xlabel('Date')
pylab.show()

# expenditures
# by candidate
expenditure_size_cand_time_series = \
expenditures.groupby(['cand_nm', 'contb_receipt_dt_format']).size().unstack(0)

expenditure_size_cand_time_series.plot()
plt.title('Expenditures during election cycle')
plt.ylabel('Number of expenditures')
plt.xlabel('Date')
pylab.show()

# census region
expenditure_size_census_time_series = \
expenditures.groupby(['census_region', 'contb_receipt_dt_format']).size().unstack(0)

expenditure_size_census_time_series.ix['07-2012':'12-2012'].plot()
plt.title('Expenditures during election cycle: census region')
plt.ylabel('Number of expenditures')
plt.xlabel('Date')
pylab.show()


# economic region
expenditure_size_economic_time_series = \
expenditures.groupby(['economic_region', 'contb_receipt_dt_format']).size().unstack(0)

expenditure_size_economic_time_series.ix['07-2012':'12-2012'].plot()
plt.title('Expenditures during election cycle: economic region')
plt.ylabel('Number of expenditures')
plt.xlabel('Date')
pylab.show()

# payment size
expenditure_size_donor_time_series = \
expenditures.groupby(['payment_size', 'contb_receipt_dt_format']).size().unstack(0)

expenditure_size_donor_time_series.ix['07-2012':'12-2012'].plot()
plt.title('Expenditures during election cycle: payment size')
plt.ylabel('Number of expenditures')
plt.xlabel('Date')
pylab.show()


#------------------------------------------------------------------------------ 
# R-style data frame export: summary with state data for chloropleth plots

state_data_columns = \
['cand_nm', 'contb_receipt_dt_format', 'contbr_st', 'state_name', 'census_region',
 'economic_region','population', 'pop_density', 'winner', 'obama_total', 
 'romney_total', 'electoral_votes', 'males', 'females', 'sex_ratio', 
 'under_18_count', 'under_18_pct', 'eighteen_to_forty_four_count',
 'eighteen_to_forty_four_pct', 'forty_five_to_sixty_four_count',
 'forty_five_to_sixty_four_pct', 'sixty_five_over_count', 'sixty_five_over_pct',
 'median_age', 'total_households', 'husband_wife_household', 'husband_wife_child_under_18',
 'female_household', 'female_child_under_18', 'male_household', 'male_child_under_18',
 'one_person_nonfamily', 'one_person_sixty_five_older', 'one_person_at_least_two',
 'avg_per_family', 'avg_per_household', 'eighty_five_over_count', 'eighty_five_over_pct']

fec_net_money_state = \
fec_final.groupby(state_data_columns, as_index = False)[['contb_receipt_amt']].sum()


fec_census_net_money_state = \
fec_final.groupby(state_data_columns, as_index = False)[['contb_receipt_amt']].sum()
                  
                
fec_economic_net_money_state = \
fec_final.groupby(state_data_columns, as_index = False)[['contb_receipt_amt']].sum()


# donation sums
donations_cand_sum_state = \
donations.groupby(state_data_columns, 
                  as_index = False)[['contb_receipt_amt']].sum()

donations_cand__census_sum_state = \
donations.groupby(state_data_columns,
                   as_index = False)[['contb_receipt_amt']].sum()

donations_cand__economic_sum_state = \
donations.groupby(state_data_columns,
                   as_index = False)[['contb_receipt_amt']].sum()

# expenditure sums
expenditures_cand_sum_state = \
expenditures.groupby(state_data_columns, 
                     as_index = False)[['contb_receipt_amt']].sum()

expenditures_cand__census_sum_state = \
expenditures.groupby(state_data_columns, as_index = False)[['contb_receipt_amt']].sum()

expenditures_cand__economic_sum_state = \
expenditures.groupby(state_data_columns,as_index = False)[['contb_receipt_amt']].sum()


# writing files for importation into R

fec_net_money_state.to_csv('fec-data-net-contributions-state.csv')
fec_census_net_money_state.to_csv('fec-data-census-regions-net-contributions-state.csv')
fec_economic_net_money_state.to_csv('fec-data-economic-regions-net-contributions-state.csv')

donations_cand_sum_state.to_csv('donation-data-candidate-idx-state.csv')
donations_cand__census_sum_state.to_csv('donation-data-census-regions-candidate-idx-state.csv')
donations_cand__economic_sum_state.to_csv('donation-data-economic-regions-candidate-idx-state.csv')

expenditures_cand_sum_state.to_csv('expenditure-data-candidate-idx-state.csv')
expenditures_cand__census_sum_state.to_csv('expenditure-data-census-regions-candidate-idx-state.csv')
expenditures_cand__economic_sum_state.to_csv('expenditure-data-economic-regions-candidate-idx-state.csv')


#------------------------------------------------------------------------------ 
# R-style data frame export: candidate and amount data (breakout detection)

fec_net_money = \
fec_final.groupby(['cand_nm', 'contb_receipt_dt_format'], 
                  as_index = False)[['contb_receipt_amt']].sum()


fec_census_net_money = \
fec_final.groupby(['cand_nm', 'census_region', 'contb_receipt_dt_format'], 
                  as_index = False)[['contb_receipt_amt']].sum()
                  
                
fec_economic_net_money = \
fec_final.groupby(['cand_nm', 'economic_region', 'contb_receipt_dt_format'], 
                  as_index = False)[['contb_receipt_amt']].sum()


# donation sums
donations_cand_sum = \
donations.groupby(['cand_nm', 'contb_receipt_dt_format'], 
                  as_index = False)[['contb_receipt_amt']].sum()

donations_cand__census_sum = \
donations.groupby(['cand_nm', 'census_region','contb_receipt_dt_format'],
                   as_index = False)[['contb_receipt_amt']].sum()

donations_cand__economic_sum = \
donations.groupby(['cand_nm', 'economic_region','contb_receipt_dt_format'],
                   as_index = False)[['contb_receipt_amt']].sum()

# expenditure sums
expenditures_cand_sum = \
expenditures.groupby(['cand_nm', 'contb_receipt_dt_format'], 
                     as_index = False)[['contb_receipt_amt']].sum()

expenditures_cand__census_sum = \
expenditures.groupby(['cand_nm', 'census_region','contb_receipt_dt_format'], 
                     as_index = False)[['contb_receipt_amt']].sum()

expenditures_cand__economic_sum = \
expenditures.groupby(['cand_nm', 'economic_region','contb_receipt_dt_format'],
                      as_index = False)[['contb_receipt_amt']].sum()


# writing files for importation into R

fec_net_money.to_csv('fec-data-net-contributions.csv')
fec_census_net_money.to_csv('fec-data-census-regions-net-contributions.csv')
fec_economic_net_money.to_csv('fec-data-economic-regions-net-contributions.csv')

donations_cand_sum.to_csv('donation-data-candidate-idx.csv')
donations_cand__census_sum.to_csv('donation-data-census-regions-candidate-idx.csv')
donations_cand__economic_sum.to_csv('donation-data-economic-regions-candidate-idx.csv')

expenditures_cand_sum.to_csv('expenditure-data-candidate-idx.csv')
expenditures_cand__census_sum.to_csv('expenditure-data-census-regions-candidate-idx.csv')
expenditures_cand__economic_sum.to_csv('expenditure-data-economic-regions-candidate-idx.csv')
