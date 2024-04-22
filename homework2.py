# PPHA 30537
# Spring 2024
# Homework 2

# YOUR NAME HERE
#Mingxuan Yue
# YOUR GITHUB USER NAME HERE
#Miyue
# Due date: Sunday April 21st before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.  Using functions for organization will be rewarded.

##################

# To answer these questions, you will use the csv document included in
# your repo.  In nst-est2022-alldata.csv: SUMLEV is the level of aggregation,
# where 10 is the whole US, and other values represent smaller geographies. 
# REGION is the fips code for the US region. STATE is the fips code for the 
# US state.  The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2022/NST-EST2022-ALLDATA.pdf
# Note that each question will build on the modified dataframe from the
# question before.  Make sure the SettingWithCopyWarning is not raised.

# PART 1: Macro Data Exploration
import pandas as pd
import os
import us
# Question 1.1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.
data_path = 'C:/Users/86181/Downloads'
ALLDATA = 'NST-EST2022-ALLDATA.csv'
file_path = os.path.join(data_path, ALLDATA)
data = pd.read_csv(file_path)


# Question 1.2: Your data only includes fips codes for states (STATE).  Use 
# the us library to crosswalk fips codes to state abbreviations.  Drop the
# fips codes.

#def state_abbreviation(fips_code):
#    state = us.states.lookup(str(fips_code).zfill(2))
#    return state.abbr if state else None

#data['STATE_ABBR'] = data['STATE'].apply(state_abbreviation)
#data = data.drop(columns=['STATE'])
#print(data.head())

fips_to_state = { 1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 
                 9: 'CT', 10: 'DE', 11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 
                 17: 'IL', 18: 'IN', 19: 'IA', 20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 
                 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN', 28: 'MS', 29: 'MO', 30: 'MT', 
                 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM', 36: 'NY', 37: 'NC', 
                 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI', 45: 'SC', 
                 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA', 
                 54: 'WV', 55: 'WI', 56: 'WY', 72: 'PR' }
data['STATE_ABBR'] = data['STATE'].map(fips_to_state)
data = data.drop(columns=['STATE'])
print(data.head())
#in this question I use Chatgpt to search"how to use 
#us lirary to change fips codes to state abbreviations in python"
#But I can't solve this problem using us library. 
#I cannot convert Fips11 to DC when using us Library. 
#So I found another way to solve this problem using Chatgpt.

# Question 1.3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize for them.  Do not 
# create plots or use groupby; we will do that in future homeworks.  
# Show the relevant exploration output with print() statements.
print("Shape:", data.shape)
print("Column names:", data.columns.tolist())
print(data.dtypes)
print(data.describe())
print(data.isnull().sum())
#in this question I use Chatgpt to search
#"What should some basic exploration of a data frame include?"

# Question 1.4: Subset the data so that only observations for individual
# US states remain, and only state abbreviations and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.
state_population = data[data['SUMLEV'] == 40][['STATE_ABBR', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']]
print(state_population.head())

# Question 1.5: Show only the 10 largest states by 2021 population estimates,
# in decending order.
decending_2021 = state_population.sort_values(by='POPESTIMATE2021', ascending=False)
top_10_2021 = decending_2021.head(10)
print(top_10_2021)

# Question 1.6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?
state_population['POPCHANGE'] = state_population['POPESTIMATE2022'] - state_population['POPESTIMATE2020']
states_gained = state_population[state_population['POPCHANGE'] > 0].shape[0]
states_lost = state_population[state_population['POPCHANGE'] < 0].shape[0]
print(states_gained)
print(states_lost)

# Question 1.7: Show all the states that had an estimated change in either
# direction of smaller than 1000 people. 
small_than1000 = state_population[abs(state_population['POPCHANGE']) < 1000]
print(small_than1000)

# Question 1.8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.
std_change = state_population['POPCHANGE'].std()
significant_states = state_population[abs(state_population['POPCHANGE']) > std_change]
states_sort = significant_states.sort_values(by='POPCHANGE', key=abs, ascending=False)
print(states_sort)

#PART 2: Data manipulation

# Question 2.1: Reshape the data from wide to long, using the wide_to_long function,
# making sure you reset the index to the default values if any of your data is located 
# in the index.  What happened to the POPCHANGE column, and why should it be dropped?
# Explain in a brief (1-2 line) comment.
df_dropped = state_population.drop(columns=['POPCHANGE'])
df_dropped.reset_index(drop=True)
population_long = pd.wide_to_long(df_dropped, stubnames='POPESTIMATE', i='STATE_ABBR', j='YEAR', sep='', suffix='\d+').reset_index()
print(population_long.head())
#Because "POPCHANGE" does not correspond to any single year like the other columns. 
#Including it in the data package will result in inconsistent time ordering.

#Since my code wasn't running, I used Chatgpt for diagnostics. 
#It was found that my us packet could not convert fips11 to DC. 
#After diagnosis by Chatgpt, it was found that there may be a problem with the code in the first question.

# Question 2.2: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 2.1 (without the POPCHANGE column).
if 'POPCHANGE' in state_population.columns:
    state_population1 = state_population.drop(columns='POPCHANGE')
state_population1.reset_index(drop=True, inplace=True)
melted_population = pd.melt(state_population1, id_vars=['STATE_ABBR'], value_vars=['POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022'],
                            var_name='YEAR', value_name='POPULATION')
melted_population['YEAR'] = melted_population['YEAR'].str.extract('(\d+)')
print(melted_population.head())

#My old code was "state_population = state_population.drop(columns='POPCHANGE')"
#This caused me to find that no "POPCHANGE" could be dropped when running. 
#So I used Chatgpt to ask the reason.
#Modify the code to "state_population1 = state_population.drop(columns='POPCHANGE')" with the help of Chatgpt.

# Question 2.3: Open the state-visits.xlsx file in Excel, and fill in the VISITED
# column with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original wide-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.
visited_states = pd.read_excel('C:/Users/86181/Desktop/Uchicago/Quarter3/python/hw2/state-visits.xlsx')
visited_states.rename(columns={'STATE': 'STATE_ABBR'}, inplace=True)
merged_data = pd.merge(state_population.drop(columns=['POPCHANGE']), visited_states, on='STATE_ABBR', how='inner')
all_states = set(state_population['STATE_ABBR'])
visited_states = set(visited_states['STATE_ABBR'])
print("Dropped:", all_states.difference(visited_states))

#When I run my code, the system prompts "Keyerror: STATE_ABBR".
#I added rename with the help of Chatgpt.

# Question 2.4: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state, beginning in different years for
# each state but ending in 2022 for all states.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.
policy=pd.read_excel('C:/Users/86181/Downloads/policy_uncertainty.xlsx') 
policy1= policy.groupby(['state', 'year'])['EPU_Composite'].mean().reset_index() 
print (policy1)


# Question 2.5) Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. 
policy_wide = policy1.pivot(index='state', columns='year', values='EPU_Composite')
policy_wide = policy_wide[[2020, 2021, 2022]]
print(policy_wide.head())

# Question 2.6) Finally, merge this data into your merged data from question 2.3, 
# making sure the merge does what you expect.
if policy_wide.index.name == 'state':
    policy_wide.reset_index(inplace=True)
state_map = {state.name: state.abbr for state in us.states.STATES_AND_TERRITORIES}
policy_wide['state'] = policy_wide['state'].map(state_map)
final_merged_data = pd.merge(merged_data, policy_wide, left_on='STATE_ABBR', right_on='state', how='inner')
final_merged_data.drop(columns=['state'], inplace=True, errors='ignore')  # Cleanup if 'state' column still exists
print(final_merged_data.head())
#Since my personal code shows blank results. 
#I asked Chatgpt for troubleshooting methods. 
#Found because of a mismatch between state abbreviations and full words. 
#I modified the code via Chatgpt's suggestion.

# Question 2.7: Using groupby on the VISITED column in the dataframe resulting 
# from the previous question, answer the following questions and show how you  
# calculated them: a) what is the single smallest state by 2022 population  
# that you have visited, and not visited?  b) what are the three largest states  
# by 2022 population you have visited, and the three largest states by 2022 
# population you have not visited? c) do states you have visited or states you  
# have not visited have a higher average EPU-C value in 2022?
final_merged_data['POPESTIMATE2022'] = pd.to_numeric(final_merged_data['POPESTIMATE2022'], errors='coerce')
smallest_states = final_merged_data.groupby('VISITED').apply(lambda x: x.nsmallest(1, 'POPESTIMATE2022'))
print("Smallest state in 2022:\n", smallest_states[['STATE_ABBR', 'POPESTIMATE2022', 'VISITED']])
largest_states = final_merged_data.groupby('VISITED').apply(lambda x: x.nlargest(3, 'POPESTIMATE2022'))
print("Three largest states in 2022:\n", largest_states[['STATE_ABBR', 'POPESTIMATE2022', 'VISITED']])
final_merged_data[2020] = pd.to_numeric(final_merged_data[2020], errors='coerce')
average_epu_c = final_merged_data.groupby('VISITED')[2020].mean()
print("Average value in 2022:\n", average_epu_c)

#I cannot run the function "final_merged_data[2020]". 
#I asked Chatgpt why. 
#It is known that if Column is a number, it needs to be written differently.
#For example:['POPESTIMATE2022'] and [2020].

# Question 2.8: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 2.4 and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore.
def zscore(x):
    return (x - x.mean()) / x.std()
policy1['EPU_C_zscore'] = policy1.groupby('state')['EPU_Composite'].transform(zscore)
print(policy1.head())
state_check = 'California'
mean_z = policy1[policy1['state'] == state_check]['EPU_C_zscore'].mean()
std_z = policy1[policy1['state'] == state_check]['EPU_C_zscore'].std()
print(f"Mean of Z-scores for {state_check}: {mean_z}")
print(f"Standard Deviation of Z-scores for {state_check}: {std_z}")
