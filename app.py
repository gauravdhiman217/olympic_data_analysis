import plotly.express as px
import streamlit as st
from plotly import figure_factory as ff

import helper
import preprocessor

st.set_page_config(layout="wide")
st.sidebar.image('Olympic-Symbol.png')
df = preprocessor.preprocess()
st.sidebar.title("Olympic Analysis from 1896 to 2016")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis',
     'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':

    st.sidebar.title('Medal Tally')
    years, country = helper.country_year(df)
    selected_year = st.sidebar.selectbox('select year', years)
    selected_country = st.sidebar.selectbox('select country', country)
    medal_tally, graph = helper.fetch_medal(
        df, selected_year, selected_country)
    # dashboard look
    st.title("Countries Performace in Olympics")
    col1, col2 = st.columns(2, gap="small")
    with col1:
        temp = helper.pie_medal_tally(df, selected_year, selected_country)
        fig = px.pie(temp, values='Nos of Players', names='Sport', hole=0.3)
        fig.update_traces(textposition='inside', textinfo='percent+label',)
        fig.update_layout(margin=dict(t=25, b=0, l=0, r=0))
        fig.update(layout_title_text='Athelets Distribution Sports wise',
                   layout_showlegend=False)
        st.plotly_chart(fig)
        # df2 = helper.medal_tally_graph(graph,selected_year,selected_country)

    with col2:
        if selected_country != "Overall":

            fig = px.bar(graph, x='Sport', y='value', color='variable', labels={
                         'value': "No of Medals win"}, title=f"{selected_country} performace in different sports")
        if selected_country == "Overall":
            fig = px.bar(graph, x='Region', y='value', color='variable', labels={
                         'value': "No of Medals win"}, title="Top 10 countries from medal tally")
        fig.update(layout_showlegend=True)
        fig.update_layout(margin=dict(t=25, b=0, l=0, r=0))
        st.plotly_chart(fig)
    st.write(
        "Upper Chart's describe us athletes distribution in Games. Along with Chart show Top 10 countries in olympics.  ",
        "This charts are responsive to side bar widgets if user select specific counytry it will show Athelets distribution for specific country and Top 10 country bar chart wili show ",
        "Sports in which country participates. Same as if user select particular year it show top 10 country in that year along with athelets distributions ."
    )
    st.write("  below we have Medal Tally which is again Responsive to side widgets.")
    # medal tally code start
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(" Medal Tally in  " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Overall performance of " + selected_country + " Olympics")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " +
                 str(selected_year) + " Olympics")
    st.table(medal_tally)
    st.balloons()

if user_menu == 'Overall Analysis':
    st.title("Overall Olympic Analysis")
    # metric type show of data in
    editions = df['Year'].unique().shape[0] - 1
    event = df['Event'].unique().shape[0]
    athlets = df['Name'].unique().shape[0]
    # -1 for null value in region
    nations = df['Region'].unique().shape[0] - 1
    city = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", editions)
    col2.metric("Host Cities", city)
    col3.metric('Nations', nations)
    col1, col2, col3 = st.columns(3)
    col1.metric("Sports", Sports)
    col2.metric("Events", event)
    col3.metric('Athletes', athlets)

    st.write(
        f"there are {editions} editions happen from 1896 to 2016 and {nations} nations had participated it might be different from actual data"
        " as some nations change there name e.g. Russia is called Soviet union before. There are some sports which is included and excluded over the time by olympic authorites"
    )

    st.header("Nations in olympics year wise")
    st.write("This Graph help us to visualise No of participating nations in olympics over the years from 1896 "
             "to 2016. And it is clearly visual Participating nations are increasing Over the years"
             ". There is dip in 1980 olympic as In 1980, the United States led a boycott of the Summer Olympic Games in Moscow to protest the late 1979 Soviet invasion of Afghanistan."
             "In total, 65 nations refused to participate in the games, whereas 80 countries sent athletes to compete."
             )
    year_nations = helper.Nations_year_graph(df)
    fig = px.line(year_nations, x="Year", y="Nations",
                  title='No of Nations in Olympics')
    st.plotly_chart(fig)

    st.header('Mens and Women Participation over the years in olympic')
    st.write(
        "Intially in 1896 there is not women participant in olympic, first women contirbution done in 1900 and from 1900 to 2016 we can see women are now almost equal to men athelets."
        ". Even in some country contigents there are more women athelets than men athelets And in further analysis i found that women participation need to we increase if a country want to be in top 10 . as all top 10 countries have significant number of medals win by womens"
    )
    final = helper.men_women(df)
    fig = px.line(final, x='Year', y=[
                  'Men', 'Women'], title='Men and Women participants')
    st.plotly_chart(fig)
    st.write("Sports and year in which is was played first. "
    "some games introduced for boys very ealry and for women it was introduced later or still not included")
    col4, col5 = st.columns(2)
    with col4:
        st.title("Men's sports starting year")
        male_sports = df[df['Sex'] == 'M']
        male_sports = male_sports.groupby('Sport').min()['Year'].reset_index()
        st.table(male_sports)
    with col5:
        st.title("Women's sports starting year")
        female_sports = df[df['Sex'] == 'F']
        female_sports = female_sports.groupby(
            'Sport').min()['Year'].reset_index()
        st.table(female_sports)
if user_menu == 'Country-wise Analysis':
    # country list from above
    country = helper.country_list(df)
    selected_country = st.selectbox("Select Country for analysis", country)
    # with_out have value of women win medal expect selected country
    # with hold value of medal win by women from selected country
    if selected_country != "Select_Country":
        temp1 = helper.country_sports_medal(df, selected_country)
        men_gold = temp1[(temp1['Sex'] == 'M')].sum()['Gold']
        men_silver = temp1[(temp1['Sex'] == 'M')].sum()['Silver']
        men_bronze = temp1[(temp1['Sex'] == 'M')].sum()['Bronze']
        women_gold = temp1[(temp1['Sex'] == 'F')].sum()['Gold']
        women_silver = temp1[(temp1['Sex'] == 'F')].sum()['Silver']
        women_bronze = temp1[(temp1['Sex'] == 'F')].sum()['Bronze']
        fig = px.bar(temp1, x='Sport', y='Total_medal', color='Sex',
            title='Medals win in games in which country participate', hover_data=['Gold', 'Sex', 'Silver', 'Bronze', 'Total_medal'])
        st.plotly_chart(fig)
        first_gold, event = helper.first_gold(df, selected_country)
        col1, col2 = st.columns(2)
        with col1:
            st.header(
                f'First Gold in : {str(first_gold[0])} in year {str(first_gold[1])}')
        with col2:
            st.header(f'Events Played by Nation is {str(event)}')
        col1, col2, col3 = st.columns(3)
        col1.metric("Gold win by Men", men_gold)
        col2.metric("Silver win by Men", men_silver)
        col3.metric('Bronze win by Men', men_bronze)
        col1, col2, col3 = st.columns(3)
        col1.metric("Gold win by women", women_gold)
        col2.metric("Silver win by Women", women_silver)
        col3.metric('Bronze win by Women', women_bronze)
        men_women = helper.men_women_country(df, selected_country)
        st.write(
            "As Per Data if we See women contribution of top 10 nations we can clearly figure out,"
            " That there women contribution is atlest 30-40'%' of total medal win be nation and Women "
            "atheletes are more or nealy equal to men athelets."
        )
        fig = px.line(men_women, x='Year', y=[
                      'Men', 'Women'], title=f'Men and Women participants comparison for {str(selected_country)}')
        st.plotly_chart(fig)
        st.title(f'Sucessfull atheles from {str(selected_country)}')
        succefull_athele = helper.country_succesfull_athele(
            df, selected_country)
        st.table(succefull_athele)

    else:
        st.header("Select Country From list")

if user_menu == 'Athlete wise Analysis':
    
    # Age graph
    hist_data, temp = helper.Age_height_graph(df)
    group_labels = ['Overall Age', 'Gold Medlist',
                    'Silver Medlist', 'Bronze Medlist']
    fig = ff.create_distplot(hist_data, group_labels,
                             show_hist=False, show_rug=False)
    st.header("Chart to show Age distribution and medal winning chance at which age")
    st.plotly_chart(fig)
    st.write(
        "As per Data Age BTW 22 to 24 is consider as a GOLDEN Age for medal winners most of the medals are win at the age between 22 to 24 and after that medal winning chance are reducing. So if a nation want to choose athelets then they should be picked at the early age so they can perfom better at the age between 20 to 28 and contribute to there nation."
    )
    
    # scatter_matrix
    st.header("Heigh, weight and Age comparision")
    fig = px.scatter_matrix(temp,
    dimensions=["Age", "Height", "Weight"],
    color="Medal")
    st.plotly_chart(fig)
    st.write("As per Historical data of height, weight and age of atheletes and medals win by than"
            "we found that Height effect lot of chance to win medal if you have height greater than 170 cm you"
            " have great chance to win medeal, even in age of late 40's if your height is around 170cm winning medel is possible"
            ". Same for weight as per data 70kg or around 70 is considered as perfect weight but it might various as per requirments"
    )
    
    #succesfull athletes
    Sports_list = helper.sports_list(df)
    st.title("Athlete Wise Analysis")
    selected_sports = st.selectbox(
        "Select Game to see Top 10 athlete", Sports_list)
    succ_athlete = helper.successfull_athlete(df, selected_sports)
    st.table(succ_athlete)
    
    