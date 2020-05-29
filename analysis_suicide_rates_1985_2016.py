#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
License
-------
    The MIT License (MIT)
    Copyright (c) 2020 omancommunity
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
Created on Sat Dec 16 22:46:28 2017
@author: Sami Mohsin 
"""

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

COLUMNS = [
    'country',
    'year',
    'sex',
    'age',
    'suicides_no',
    'population',
    'suicides/100k pop',
    'country-year',
    'HDI_for_year',
    'gdp_for_year($)',
    'gdp_per_capita($)',
    'generation',

]

COLUMNS_NEW_NAMES = ['country',
                     'year',
                     'sex',
                     'age',
                     'suicides_no',
                     'population',
                     'suicides_100k_pop',
                     'country_year',
                     'HDI_for_year',
                     'gdp_for_year',
                     'gdp_per_capita',
                     'generation'
                     ]

# step One
df = pd.read_csv('data/master.csv',
                 usecols=COLUMNS,
                 sep=',')
# rename columns using the .columns attribute or
# df.rename(columns={old_name:new_name})
df.columns = COLUMNS_NEW_NAMES
# save renam file
df.to_csv('data/out.csv',
          columns=COLUMNS_NEW_NAMES,
          index=False)

# step Two
dff = pd.read_csv('data/out.csv',
                  usecols=COLUMNS_NEW_NAMES)

# replace field that's entirely space (or empty) with NaN
# print(dff.replace(r'^\s*$', np.nan, regex=True)


# change nan/NaN to 0
dff[COLUMNS_NEW_NAMES] = dff[COLUMNS_NEW_NAMES].fillna(value=0)

# extract unique countries in csv file to numpy array
# or simply use
# ```countries = dff['country'].unique()```
countries = np.array([cou for cou in dff['country'].unique()])


def find_country_position(name, dic=None):
    if dic is not None:
        return int(list(dic).index(name))


def get_all_countries_from_index(data,
                                 col_country='country',
                                 name=None,
                                 dic_list: np.array = None):
    """
    get all data about one specific country,
    there also another way to do with pandas
    data will be return as pd.DataFrame
    :type dic_list: np.array
    :type data: pd.DataFrame
    :param col_country :
    :param name:
    :param dic:
    :return:
    """
    if name is not None:
        return data[data[col_country].str.contains(countries[int(list(dic_list).index(name))])]
    raise ValueError('Please insert name and countries dic .')


# find all Oman  from csv file (you can use mask in pandas)
oman_df = get_all_countries_from_index(dff,
                                       name='Oman',
                                       dic_list=countries)
print(oman_df.sample(10))

# save oman data to new csv file
# making index=False is to except id from our file
oman_df.to_csv('data/oman_suicide.csv', columns=COLUMNS_NEW_NAMES, index=False)

# Step Three

oman_df = pd.read_csv('data/oman_suicide.csv', usecols=COLUMNS_NEW_NAMES, index_col=0)

# convert male to 1 & female to 0
# oman_df['sex'] = oman_df['sex'].apply(lambda x: 1 if x == 'male' else 0)

print(oman_df)






# Step four
"""
Making Simple Graphs
"""

###Let's check for country
# alpha = 0.7
# plt.figure(figsize=(10,19))
# sns.countplot(y='year', data=oman_df, alpha=alpha)
# plt.title('Data by year in Oman')
# plt.show()


### Set figure size
plt.figure(figsize=(16,7))
###Let's plot the barplot
bar_age = sns.barplot(x = 'sex', y = 'suicides_no', hue = 'age',data =oman_df)


age_5 = oman_df.loc[oman_df.loc[:, 'age']=='5-14 years',:]
age_15 = oman_df.loc[oman_df.loc[:, 'age']=='15-24 years',:]
age_25 = oman_df.loc[oman_df.loc[:, 'age']=='25-34 years',:]
age_35 = oman_df.loc[oman_df.loc[:, 'age']=='35-54 years',:]
age_55 = oman_df.loc[oman_df.loc[:, 'age']=='55-74 years',:]
age_75 = oman_df.loc[oman_df.loc[:, 'age']=='75+ years',:]

### Set figure size
plt.figure(figsize=(16,7))
####Now lets plot a line plot
age_5_lp = sns.lineplot(x='year', y='suicides_no', data=age_5)
age_15_lp = sns.lineplot(x='year', y='suicides_no', data=age_15)
age_25_lp = sns.lineplot(x='year', y='suicides_no', data=age_25)
age_35_lp = sns.lineplot(x='year', y='suicides_no', data=age_35)
age_55_lp = sns.lineplot(x='year', y='suicides_no', data=age_55)
age_75_lp = sns.lineplot(x='year', y='suicides_no', data=age_75)

##Now make the legend
leg = plt.legend(['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years'])
plt.show()


# for more training go : https://www.kaggle.com/kageyama/exploratory-data-analysis-using-seaborn
# a nice post using jupyter notebook
