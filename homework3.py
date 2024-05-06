# PPHA 30537
# Spring 2024
# Homework 3

# YOUR NAME HERE
#Mingxuan Yue
# YOUR CANVAS NAME HERE
# YOUR GITHUB USER NAME HERE

# Due date: Sunday May 5th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

#NOTE: All of the plots the questions ask for should be saved and committed to
# your repo under the name "q1_1_plot.png" (for 1.1), "q1_2_plot.png" (for 1.2),
# etc. using fig.savefig. If a question calls for more than one plot, name them
# "q1_1a_plot.png", "q1_1b_plot.png",  etc.

# Question 1.1: With the x and y values below, create a plot using only Matplotlib.
# You should plot y1 as a scatter plot and y2 as a line, using different colors
# and a legend.  You can name the data simply "y1" and "y2".  Make sure the
# axis tick labels are legible.  Add a title that reads "HW3 Q1.1".

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf

x = pd.date_range(start='1990/1/1', end='1991/12/1', freq='MS')
y1 = np.random.normal(10, 2, len(x))
y2 = [np.sin(v)+10 for v in range(len(x))]

plt.figure(figsize=(10, 6))
plt.scatter(x, y1, color='blue', label='y1') 
plt.plot(x, y2, color='red', label='y2')      
plt.legend()                                 
plt.xticks(rotation=45)                       
plt.title('HW3 Q1.1')                        
plt.xlabel('Date')                            
plt.ylabel('Values')                         
plt.tight_layout()
plt.show()
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Q1.1.png')

# Question 1.2: Using only Matplotlib, reproduce the figure in this repo named
# question_2_figure.png.
x = np.linspace(10, 20, 11)
y1 = 30-x  
y2 = x    

plt.figure(figsize=(8, 6))
plt.plot(x, y1, label='Red', color='red')
plt.plot(x, y2, label='Blue', color='blue')
plt.legend()
plt.title('X marks the spot')
plt.xlabel('X')
plt.ylabel('Y')
plt.ylim(10, 20)  
plt.xlim(10, 20)
plt.show()
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Q1.2.png')

# Question 1.3: Load the mpg.csv file that is in this repo, and create a
# plot that tests the following hypothesis: a car with an engine that has
# a higher displacement (i.e. is bigger) will get worse gas mileage than
# one that has a smaller displacement.  Test the same hypothesis for mpg
# against horsepower and weight.
mpg = pd.read_csv('C:/Users/86181/Downloads/mpg.csv')
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].scatter(mpg['displacement'], mpg['mpg'])
axs[0].set_title('Displacement vs. MPG')
axs[0].set_xlabel('Displacement')
axs[0].set_ylabel('MPG')

axs[1].scatter(mpg['horsepower'], mpg['mpg'])
axs[1].set_title('Horsepower vs. MPG')
axs[1].set_xlabel('Horsepower')

axs[2].scatter(mpg['weight'], mpg['mpg'])
axs[2].set_title('Weight vs. MPG')
axs[2].set_xlabel('Weight')

plt.tight_layout()
plt.show()
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Q1.3.png')
#In this question I asked Chatgpt "How to create a subplot with three scatter plots."

# Question 1.4: Continuing with the data from question 1.3, create a scatter plot 
# with mpg on the y-axis and cylinders on the x-axis.  Explain what is wrong 
# with this plot with a 1-2 line comment.  Now create a box plot using Seaborn
# that uses cylinders as the groupings on the x-axis, and mpg as the values
# up the y-axis.
plt.figure(figsize=(8, 6))
sns.scatterplot(x=mpg['cylinders'], y=mpg['mpg'])
plt.title('MPG vs. Cylinders Scatter Plot')
plt.xlabel('Cylinders')
plt.ylabel('MPG')
plt.show()
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Q1.4.png')

#A scatter plot may not clearly show the distribution or variation of mpg 
#within each cylinder category because the points may overlap. 
#This can cause us to have trouble evaluating the density or distribution 
#of data within each category.
plt.figure(figsize=(8, 6))
sns.boxplot(x='cylinders', y='mpg', data=mpg)
plt.title('MPG by Cylinders Box Plot')
plt.xlabel('Cylinders')
plt.ylabel('MPG')
plt.show()
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Q1.4.2.png')

# Question 1.5: Continuing with the data from question 1.3, create a two-by-two 
# grid of subplots, where each one has mpg on the y-axis and one of 
# displacement, horsepower, weight, and acceleration on the x-axis.  To clean 
# up this plot:
#   - Remove the y-axis tick labels (the values) on the right two subplots - 
#     the scale of the ticks will already be aligned because the mpg values 
#     are the same in all axis.  
#   - Add a title to the figure (not the subplots) that reads "Changes in MPG"
#   - Add a y-label to the figure (not the subplots) that says "mpg"
#   - Add an x-label to each subplot for the x values
# Finally, use the savefig method to save this figure to your repo.  If any
# labels or values overlap other chart elements, go back and adjust spacing.
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Changes in MPG')

sns.scatterplot(ax=axs[0, 0], x='displacement', y='mpg', data=mpg)
axs[0, 0].set_title('Displacement vs. MPG')
axs[0, 0].set_xlabel('Displacement')
axs[0, 0].set_ylabel('MPG')

sns.scatterplot(ax=axs[0, 1], x='horsepower', y='mpg', data=mpg)
axs[0, 1].set_title('Horsepower vs. MPG')
axs[0, 1].set_xlabel('Horsepower')
axs[0, 1].set_ylabel('')
axs[0, 1].tick_params(labelleft=False)  # Remove y-axis tick labels

sns.scatterplot(ax=axs[1, 0], x='weight', y='mpg', data=mpg)
axs[1, 0].set_title('Weight vs. MPG')
axs[1, 0].set_xlabel('Weight')
axs[1, 0].set_ylabel('MPG')

sns.scatterplot(ax=axs[1, 1], x='acceleration', y='mpg', data=mpg)
axs[1, 1].set_title('Acceleration vs. MPG')
axs[1, 1].set_xlabel('Acceleration')
axs[1, 1].set_ylabel('')
axs[1, 1].tick_params(labelleft=False)  

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Changes_in_MPG.png')  
plt.show()

# Question 1.6: Are cars from the USA, Japan, or Europe the least fuel
# efficient, on average?  Answer this with a plot and a one-line comment.
avg_mpg_by_country = mpg.groupby('origin')['mpg'].mean().sort_values()
avg_mpg_by_country.plot(kind='bar', color=['red', 'blue', 'green'])
plt.title('Average MPG by Country')
plt.xlabel('Country')
plt.ylabel('Average MPG')
plt.show()
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Q1.6.png')
#Cars in the U.S. are the least fuel efficient, according to plot.


# Question 1.7: Using Seaborn, create a scatter plot of mpg versus displacement,
# while showing dots as different colors depending on the country of origin.
# Explain in a one-line comment what this plot says about the results of 
# question 1.6.
plt.figure(figsize=(10, 6))
sns.scatterplot(x='displacement', y='mpg', hue='origin', data=mpg, palette='bright')
plt.title('MPG vs. Displacement by Country of Origin')
plt.xlabel('Displacement')
plt.ylabel('MPG')
plt.show()
plt.savefig('C:/Users/86181/Desktop/Uchicago/Quarter3/python/Q1.7.png')
#As the displacement distance increases, MPG shows a downward trend.
#In this question I asked Chatgpt how to create a scatter plot.

# Question 2: The file unemp.csv contains the monthly seasonally-adjusted unemployment
# rates for US states from January 2020 to December 2022. Load it as a dataframe, as well
# as the data from the policy_uncertainty.xlsx file from homework 2 (you do not have to make
# any of the changes to this data that were part of HW2, unless you need to in order to 
# answer the following questions).
#    2.1: Merge both dataframes together
unemp = pd.read_csv('C:/Users/86181/Downloads/unemp.csv')
policy = pd.read_excel('C:/Users/86181/Downloads/policy_uncertainty.xlsx')
policy['DATE'] = pd.to_datetime(policy[['year', 'month']].assign(day=1))
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
policy['STATE'] = policy['state'].map(state_abbrev)
unemp['DATE'] = pd.to_datetime(unemp['DATE'])
merged = pd.merge(unemp, policy, on=['DATE', 'STATE'], how='inner')
print(merged.head())
#In this question, when I merged two files, I found that the format of the date 
#and state in the files were different, so I used Chatgpt. 
#Chatgpt told me that I should convert the contents of the two files to the same 
#format before merging them. Since the format of the Data in the two files does not match, 
#I converted the Data in the two files to datetime64[ns] format under the guidance 
#of Chatgpt.

#    2.2: Calculate the log-first-difference (LFD) of the EPU-C data
#    2.2: Select five states and create one Matplotlib figure that shows the unemployment rate
#         and the LFD of EPU-C over time for each state. Save the figure and commit it with 
#         your code.
unemp['DATE'] = pd.to_datetime(unemp['DATE'])
merged = pd.merge(unemp, policy, on=['DATE', 'STATE'], how='inner')
merged['EPU_Composite_log'] = np.log(merged['EPU_Composite'])
merged['EPU_Composite_LFD'] = merged.groupby('STATE')['EPU_Composite_log'].diff()

#    2.3: Using statsmodels, regress the unemployment rate on the LFD of EPU-C and fixed
#         effects for states. Include an intercept.
regression = merged.dropna(subset=['EPU_Composite_LFD'])
model = smf.ols('unemp_rate ~ EPU_Composite_LFD + C(STATE)', data=regression).fit()
print(model.summary())
#In this question I used Chatgpt to query how to use "statsmodels" in Python.

#    2.4: Print the summary of the results, and write a 1-3 line comment explaining the basic
#         interpretation of the results (e.g. coefficient, p-value, r-squared), the way you 
#         might in an abstract.

#The dependent variable in this model is the unemployment rate. 
#The R-squared is 0.171, which indicates that the model explains 
#approximately 17.1% of the variability in the unemployment rate.

