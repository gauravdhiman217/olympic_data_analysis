import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import plotly.express as px

st.sidebar.image('Olympic-Symbol.png')
df = preprocessor.preprocess()
st.sidebar.title("Olympic Analysis from 1896 to 2016")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.title('Medal Tally')
    years, country = preprocessor.country_year(df)
    selected_year = st.sidebar.selectbox('select year', years)
    selected_country = st.sidebar.selectbox('select country', country)
    medal_tally = preprocessor.fetch_medal(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(" Medal Tally in  " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Overall performance of " + selected_country + " Olympics")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title("Overall Olympic Analysis")
    editions = df['Year'].unique().shape[0] - 1
    event = df['Event'].unique().shape[0]
    athlets = df['Name'].unique().shape[0]
    # -1 for null value in region
    nations = df['Region'].unique().shape[0] - 1
    city = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Host Cities')
        st.title(city)
    with col3:
        st.header('Nations')
        st.title(nations)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Sports')
        st.title(Sports)
    with col2:
        st.header('Events')
        st.title(event)
    with col3:
        st.header('Athletes')
        st.title(athlets)

    col4, col5 = st.columns(2)
    with col4:
        st.title("Men's sports starting year")
        male_sports = df[df['Sex'] == 'M']
        male_sports = male_sports.groupby('Sport').min()['Year'].reset_index()
        st.table(male_sports)
    with col5:
        st.title("Women's sports starting year")
        female_sports = df[df['Sex'] == 'F']
        female_sports = female_sports.groupby('Sport').min()['Year'].reset_index()
        st.table(female_sports)
    st.header("Nations in olympics year wise")
    st.text("This Graph help us to visualise No of participating nations in olympics over the years from 1896"
            "to 2016")
    year_nations = preprocessor.Nations_year_graph(df)
    fig = px.line(year_nations, x="Year", y="Nations", title='No of Nations in Olympics')
    st.plotly_chart(fig)

    st.header('Mens and Women Participation over the years in olympic')
    final = preprocessor.men_women(df)
    fig = px.line(final, x='Year', y=['Men', 'Women'], title='Men and Women participants')
    st.plotly_chart(fig)

if user_menu == 'Country-wise Analysis':
    # country list from above
    selected_country = st.sidebar.selectbox('select country', country)
    # with_out have value of women win medal expect selected country
    # with hold value of medal win by women from selected country
    with_out,with_in = preprocessor.women_country(df,selected_country)
    col1,col2,col3,col4 = st.columns(4)
    