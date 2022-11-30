import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def country_year(df):
    # list of years and country
    years = df['Year'].unique()
    years.sort()
    years = years.tolist()
    years.insert(0, 'Overall')
    # same process for country
    country = df['Region'].unique().astype('str')
    country = country.tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


def fetch_medal(df, years, country):
    #graph requried almost same parameter with litle adjustments so graph dataframe work along with it
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp = df
    if years != 'Overall' and country == 'Overall':
        temp = df[df['Year'] == years]
    if years == 'Overall' and country != 'Overall':
        flag = 1
        temp = df[df['Region'] == country]
    if years != 'Overall' and country != 'Overall':
        flag = 1
        temp = df[(df['Region'] == country) & (df['Year'] == years)]
    temp = temp.drop_duplicates(subset=['Year', 'Sport', 'Games', 'Team', 'City', 'Event', 'Medal', 'Noc'])
    graph_df = temp

    if flag == 1:
        temp = temp.groupby('Year').sum()[
            ['Gold', 'Silver', 'Bronze']].sort_values('Year')
        graph_df = graph_df.groupby('Sport').sum()[
            ['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
        graph_df = graph_df.reset_index()
        graph_df = pd.melt(graph_df,id_vars=['Sport'],value_vars=['Gold','Silver','Bronze'])
    else:
        temp = temp.groupby('Region').sum()[
            ['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
        graph_df = graph_df.groupby('Region').sum()[
            ['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
        graph_df = graph_df.reset_index().head(10)
        graph_df = pd.melt(graph_df,id_vars=['Region'],value_vars=['Gold','Silver','Bronze'])
        
    temp['Total'] = temp['Gold'] + temp['Silver'] + temp['Bronze']
    return temp,graph_df


def pie_medal_tally(df,years,country):
    if years == 'Overall' and country == 'Overall':
        temp = df
    if years != 'Overall' and country == 'Overall':
        temp = df[df['Year'] == years]
    if years == 'Overall' and country != 'Overall':
        temp = df[df['Region'] == country]
    if years != 'Overall' and country != 'Overall':
        temp = df[(df['Region'] == country) & (df['Year'] == years)]
    temp = temp.groupby('Sport',as_index=False).count()[['Sport','Name']].drop_duplicates(subset=['Name'])
    temp = temp.rename(columns={'Name':'Nos of Players'})
    return temp


def Nations_year_graph(df):
    year_nations = df.drop_duplicates(['Year', 'Region'])[
        'Year'].value_counts().reset_index()
    year_nations = year_nations.rename(
        columns={'index': 'Year', 'Year': 'Nations'})
    year_nations = year_nations.sort_values('Year')
    return year_nations


def men_women(df):
    women = df[
        (df['Sex'] == 'F') & (df['Season'] == 'Summer')
    ].drop_duplicates(['Name', 'Region']).groupby('Year').count()['Name'].reset_index()
    men = df[
        (df['Sex'] == 'M') & (df['Season'] == 'Summer')
    ].drop_duplicates(['Name', 'Region']).groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left').fillna(0).astype('int')
    final = final.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'})
    return final


def country_sports_medal(df, country):
    # function to return table of medals win by particular country
    df1 = df
    df1 = df1[df1['Region'] == country]
    df1['Total_medal'] = df1['Gold'] + df1['Silver'] + df1['Bronze']
    
    df1 = df1.drop_duplicates(['Event', 'Year'])
    df1 = df1.groupby(['Sport', 'Sex']).sum(['Gold', 'Silver', 'Bronze']).astype('int').reset_index()[['Sport', 'Sex', 'Gold', 'Silver', 'Bronze', 'Total_medal']].sort_values(['Gold', 'Silver', 'Bronze'],ascending=False)
    return df1


def country_list(df):
    country = df['Region'].unique().astype('str')
    country = country.tolist()
    country.sort()
    country.insert(0, 'Select_Country')
    return country


def first_gold(df,country):
    first_gold = df[(df['Medal']=='Gold') & (df['Region']==country)].sort_values('Year').min()[['Sport','Year']]
    first_gold.tolist()
    event = df[df['Region']==country]['Sport'].unique().shape[0]
    return first_gold , event

def country_succesfull_athele(df,country):
    df = df[df['Region']==country].dropna(subset=['Medal'])[['Name','Sport','Medal']].value_counts().reset_index()
    df = df.drop_duplicates('Name')
    return df.head(10)


def men_women_country(df,country):
    women = df[
        (df['Sex'] == 'F') & (df['Season'] == 'Summer') & (df['Region']==country)
    ].drop_duplicates(['Name', 'Region']).groupby('Year').count()['Name'].reset_index()
    men = df[
        (df['Sex'] == 'M') & (df['Season'] == 'Summer') & (df['Region']==country)
    ].drop_duplicates(['Name', 'Region']).groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left').fillna(0).astype('int')
    final = final.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'})
    return final

def sports_list(df):
    df1 = df['Sport'].unique().astype('str')
    df1 = df1.tolist()
    df1.sort()
    df1.insert(0,'Overall')
    return df1

def successfull_athlete(df,sports):
    df1 = df.dropna(subset=['Medal'])
    if sports == 'Overall':
        df1 = df1['Name'].value_counts()
    else:
        df1= df1[df1['Sport']==sports]['Name'].value_counts()
        # df1 = df1['Name'].Value_counts()
    df1= df1.reset_index().head(10).merge(df,how='left',right_on='Name',left_on='index')[
        ['index','Name_x','Region','Sport']].drop_duplicates()
    df1= df1.rename(columns={'index':'Name','Name_x':'Medals'})
    return df1

def Age_height_graph(df):
    temp = df.dropna(subset=['Medal'])[['Age','Weight','Height','Medal']]
    overall_df = temp['Age']
    gold_df = temp[temp['Medal']=='Gold']['Age']
    silver_df = temp[temp['Medal']=='Silver']['Age']
    bronze_df = temp[temp['Medal']=='Bronze']['Age']
    hist_data =[overall_df,gold_df,silver_df,bronze_df]
    return hist_data,temp
