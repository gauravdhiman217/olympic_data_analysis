import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

oly = pd.read_csv('athlete_events.csv')
noc_data = pd.read_csv('noc_regions.csv')


def preprocess():
    global oly, noc_data
    # Merging Two Data Frame
    oly_data = oly.merge(noc_data, how='left', on='NOC')
    # making column name constant as rest have first letter capital
    oly_data = oly_data.rename(columns={'region': 'Region', 'notes': 'Notes', 'NOC': 'Noc'})
    #droping duplicate by name so we have one person at once only
    temp = oly_data.drop_duplicates('Name')[['Age','Height','Weight']]

    #zscore value 
    """
    formula of zscore is (selected value - mean of column)/ standard deviation 
    """
    temp['zscore_height'] = ((temp.Height - temp.Height.mean())/temp.Height.std())
    temp['zscore_age'] = ((temp.Age - temp.Age.mean())/temp.Age.std())
    temp['zscore_weight'] = ((temp.Weight - temp.Weight.mean())/temp.Weight.std())
    temp =temp[
            (temp['zscore_height']> -3) & 
            (temp['zscore_height']< 3)  &
            (temp['zscore_weight']> -3) & 
            (temp['zscore_weight']< 3)  &
            (temp['zscore_age']> -3) & 
            (temp['zscore_age']< 3)   
            ]
    Age_mean = temp['Age'].mean()
    Height_mean = temp['Height'].mean()
    Weight_mean = temp['Weight'].mean()
    #adding values into main dataset
    values = {'Age':Age_mean,'Height':Height_mean,'Weight':Weight_mean}
    oly_data = oly_data.fillna(value=values)
    # filtering only summer set
    summer = oly_data[oly_data['Season'] == 'Summer']
    summer_medal = summer.drop_duplicates()
    # one hot encoding medals
    medal_tally = pd.concat([summer_medal, pd.get_dummies(summer_medal['Medal'])], axis=1)
    # summer_medal = medal_tally(20)
    return medal_tally



