# PPHA 30537
# Spring 2024
# Homework 4

# YOUR NAME HERE

# YOUR CANVAS NAME HERE
# YOUR GITHUB USER NAME HERE

# Due date: Sunday May 12th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

# Question 1: Explore the data APIs available from Pandas DataReader. Pick
# any two countries, and then 
#   a) Find two time series for each place
#      - The time series should have some overlap, though it does not have to
#        be perfectly aligned.
#      - At least one should be from the World Bank, and at least one should
#        not be from the World Bank.
#      - At least one should have a frequency that does not match the others,
#        e.g. annual, quarterly, monthly.
#      - You do not have to make four distinct downloads if it's more appropriate
#        to do a group of them, e.g. by passing two series titles to FRED.
#   b) Adjust the data so that all four are at the same frequency (you'll have
#      to look this up), then do any necessary merge and reshaping to put
#      them together into one long (tidy) format dataframe.
#   c) Finally, go back and change your earlier code so that the
#      countries and dates are set in variables at the top of the file. Your
#      final result for parts a and b should allow you to (hypothetically) 
#      modify these values easily so that your code would download the data
#      and merge for different countries and dates.
#      - You do not have to leave your code from any previous way you did it
#        in the file. If you did it this way from the start, congrats!
#      - You do not have to account for the validity of all the possible 
#        countries and dates, e.g. if you downloaded the US and Canada for 
#        1990-2000, you can ignore the fact that maybe this data for some
#        other two countries aren't available at these dates.
#   d) Clean up any column names and values so that the data is consistent
#      and clear, e.g. don't leave some columns named in all caps and others
#      in all lower-case, or some with unclear names, or a column of mixed 
#      strings and integers. Write the dataframe you've created out to a 
#      file named q1.csv, and commit it to your repo.

import pandas as pd
import pandas_datareader.data as web
from pandas_datareader import wb
import datetime
import requests
from bs4 import BeautifulSoup
import csv

gdp_us = wb.download(indicator='NY.GDP.MKTP.CD', country='US', start=2000, end=2020)
gdp_us = gdp_us.reset_index()
gdp_us.drop(columns = ['country'], inplace=True)
population_ind = wb.download(indicator='SP.POP.TOTL', country='IN', start=2000, end=2020)
population_ind = population_ind.reset_index()
population_ind.drop(columns=['country'], inplace=True)

start_date = 2000
end_date = 2020
unemployment_us = web.DataReader('UNRATE', 'fred', start_date, end_date)
unemployment_us.index = pd.to_datetime(unemployment_us.index)
unemployment_us_annual = unemployment_us.groupby(unemployment_us.index.year)['UNRATE'].mean()
unemployment_us_annual = unemployment_us_annual.to_frame().rename_axis('year').reset_index()
gdp_ind = web.DataReader('MKTGDPINA646NWDB', 'fred', start_date, end_date)
gdp_ind.index = pd.to_datetime(gdp_ind.index)
gdp_ind_annual = gdp_ind.groupby(gdp_ind.index.year)['MKTGDPINA646NWDB'].mean()
gdp_ind_annual = gdp_ind_annual.to_frame().rename_axis('year').reset_index()

data = pd.concat([gdp_us, unemployment_us_annual, gdp_ind_annual, population_ind], axis=1)
data = data.loc[:,~data.columns.duplicated()]
data.columns = ['Year', 'GDP-US', 'Unemployment-US', 'GDP-IN', 'Population-IN']
data.to_csv('q1.csv')
print(data.head())




# Question 2: On the following Harris School website:
# https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics
# There is a list of six bullet points under "Required courses" and 12
# bullet points under "Elective courses". Using requests and BeautifulSoup: 
#   - Collect the text of each of these bullet points
#   - Add each bullet point to the csv_doc list below as strings (following 
#     the columns already specified). The first string that gets added should be 
#     approximately in the form of: 
#     'required,PPHA 30535 or PPHA 30537 Data and Programming for Public Policy I'
#   - Hint: recall that \n is the new-line character in text
#   - You do not have to clean up the text of each bullet point, or split the details out
#     of it, like the course code and course description, but it's a good exercise to
#     think about.
#   - Using context management, write the data out to a file named q2.csv
#   - Finally, import Pandas and test loading q2.csv with the read_csv function.
#     Use asserts to test that the dataframe has 18 rows and two columns.

url = "https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics"

response = requests.get(url)
response.raise_for_status() 

soup = BeautifulSoup(response.text, 'html.parser')

div = soup.find('div', class_="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item")
li = div.find_all('li')

csv_doc = [['type', 'course']]  


if li:
    
    for i in range(len(li)):
        if 5 <= i <= 10:  
            description = ['required', li[i].text.strip().replace('\n', ' ')]
        elif 11 <= i <= 22:  
            description = ['elective', li[i].text.strip().replace('\n', ' ')]
        else:
            continue 
        csv_doc.append(description)
else:
    print("No list items found in the specified div.")

with open('q2.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_doc)

df = pd.read_csv('q2.csv')
print(df)

assert df.shape[0] == 18, "The DataFrame should have 18 rows"
assert df.shape[1] == 2, "The DataFrame should have 2 columns"