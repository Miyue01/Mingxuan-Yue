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
def state_abbreviation(fips_code):
    state = us.states.lookup(str(fips_code).zfill(2))
    return state.abbr if state else None

data['STATE_ABBR'] = data['STATE'].apply(state_abbreviation)
data = data.drop(columns=['STATE'])
print(data.head())
#in this question I use Chatgpt to search"how to use 
#us lirary to change fips codes to state abbreviations in python"

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
states_data = data[data['SUMLEV'] == 40]
selected_columns = ['STATE_ABBR', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']
state_population = states_data[selected_columns]
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

# Question 2.2: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 2.1 (without the POPCHANGE column).
if 'POPCHANGE' in state_population.columns:
    state_population = state_population.drop(columns='POPCHANGE')
state_population.reset_index(drop=True, inplace=True)
melted_population = pd.melt(state_population, id_vars=['STATE_ABBR'], value_vars=['POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022'],
                            var_name='YEAR', value_name='POPULATION')
melted_population['YEAR'] = melted_population['YEAR'].str.extract('(\d+)')
print(melted_population.head())

# Question 2.3: Open the state-visits.xlsx file in Excel, and fill in the VISITED
# column with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original wide-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.
visited_states = pd.read_excel('C:/Users/86181/Downloads/state-visits (1).xlsx')
merged_data = state_population.join(visited_states['VISITED'],how='outer')
merged_data['VISITED'] = merged_data['VISITED'].fillna(0)
unique_state_pop = state_population.index.difference(merged_data.index)
unique_visited = visited_states.index.difference(merged_data.index)



# Question 2.4: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state, beginning in different years for
# each state but ending in 2022 for all states.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.
policy=pd.read_excel('C:/Users/86181/Downloads/policy_uncertainty.xlsx') 
policy1=policy.copy()
policy1= policy1.groupby(['state', 'year'])['EPU_Composite'].sum().reset_index() 
print (policy1)

# Question 2.5) Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. 
policy2=policy.copy()
policy2=policy2[(policy2['year']>=2020) & (policy2['year']<=2022)]                                                 
policy2=policy2[['state','year','month','EPU_ Composite']]
policy2=policy2.groupby(['state','year'])['EPU_Composite'].sum().reset_index()                       
df_wide = policy2.pivot(index='state', columns='year', values='EPU_Composite')
print (df_wide)

# Question 2.6) Finally, merge this data into your merged data from question 2.3, 
# making sure the merge does what you expect.


# Question 2.7: Using groupby on the VISITED column in the dataframe resulting 
# from the previous question, answer the following questions and show how you  
# calculated them: a) what is the single smallest state by 2022 population  
# that you have visited, and not visited?  b) what are the three largest states  
# by 2022 population you have visited, and the three largest states by 2022 
# population you have not visited? c) do states you have visited or states you  
# have not visited have a higher average EPU-C value in 2022?


# Question 2.8: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 2.4 and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore.
