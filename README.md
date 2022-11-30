<h1 align="center">Olympic Data Analysis</h1>
<hr>
LIVE LINK : https://gauravdhiman217-olympic-data-analysis-app-7tkrifi.streamlit.app/ 
<hr>
<h2>Project Overview</h2> 
<p>  
In this Project I analysis Historical data of Olympic from 1896 to 2016. and try to answer some question on the behalf of nation. One cou ranking and performace in Olympic so the assign a task to data analyst to find insights which will help them to choose write athelets for </D>
<h3> Question to Answer </h3>
<ol>
<li>What should be ratio of male and female in overall squad</li>
  <ul>
    <li>
        As per data all top 10 performing nation they have atlest 40% or more females even in some nations females are more than males particip should be increased if            nation want to be in top perfroming nation
    </li>
  </ul>
<li>what should be age group of athelets </li>
  <ul>
    <li>
        As per Data Gold Age of winning medal is 22-24. if athelet start participation early in his/her life there is bright chance of winning medal . Nation should              permote sports in youngers athelets.
    </li>
  </ul>
  <li>Is Height and Weight of athelets Matters.</li>
<ul>
  <li>
        As per data we absorbe, most medals winners are more than height of 180cm and even in older age if you have height more than 170cm there is great chance of winning medal. As of weight it is depend as per game to game some games have there Categories in which athelets divided on the basis of weight. but most medal winners are weight between 60-70kg.
  </li>
  </ul>
  </ol>
  <hr>
  <h3>Data Cleaning </h3>
  Data cleaning is one of the important step of data analysis in our dataset there are null values in height weight and age. this columns are important for analysis so we fill this null values but before fill null we have deal with outliers, so for identify outlier we use zscale method and remove those values which are Out of 3rd STD and fill null by taking mean of only valid value
  
 <hr>
 <h3>Resources</h3>
 Kaggle data Frame :https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
 Hosting : @streamlit.io
 libraries: Pandas,Numpy,seaborn,Matplotlib
 all code writen in notebook and main data displayed in app.py , all functions writen in hepler.py and preprocesser use for dataframe loading 
