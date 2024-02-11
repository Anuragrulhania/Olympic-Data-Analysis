import streamlit as st 
import pandas as pd 
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.figure_factory as ff
import plotly.graph_objects as go


df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympic Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete wise Analysis')
)


## for showing Medal Tally

if user_menu =='Medal Tally':
    ## showing header as Medal Tally

    st.sidebar.header("Medal Tally")
    ## fetching the year,country from the df(athelete_Events.csv)
    years,country=helper.country_year_list(df)
    # adding a sidebar or selectbox
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox('Select Country',country)


    medal_tally =helper.fetch_medal_tally(df,selected_year,selected_country)
    ## for showing heading
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in " + str(selected_year)+ " Olympics")

    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country + " Overall Performance")

    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country + " Overall Performance in " + str(selected_year)+ " Olympics")
    st.table(medal_tally)

if user_menu =='Overall Analysis':
    # No. of Editions
   editions=df['Year'].unique().shape[0] -1
   # No. of cities
   cities=df['City'].unique().shape[0]
   # No.of sports
   sports=df['Sport'].unique().shape[0]
   # No. of different Events
   events=df['Event'].unique().shape[0]
   # No. of athletes
   athletes=df['Name'].unique().shape[0]
   # No.of Participating Nations
   nations=df['region'].unique().shape[0]

   st.title("Top Statistics")
   col1,col2,col3=st.columns(3)
   with col1:
       st.header("Editions")
       st.title(editions)
   with col2:
       st.header("Hosts")
       st.title(cities)
   with col3:
       st.header("Sports")
       st.title(sports)

   col1,col2,col3=st.columns(3)
   with col1:
       st.header("Events")
       st.title(events)
   with col2:
       st.header("Nations")
       st.title(nations)
   with col3:
       st.header("Athletes")
       st.title(athletes)

    # importing the  data_over_time function from helper.py to see region over time as col 
   regions_over_time=helper.data_over_time(df,'region')

   fig=px.line(regions_over_time,x="Edition",y="region")
   fig.update_layout(xaxis_title='Edition', yaxis_title='No. of Country')
   st.title("Participating Nations Over The Year")
 
   st.plotly_chart(fig)



   # importing the data_over_time function from helper.py  to see the Event over time

   Events_over_time=helper.data_over_time(df,'Event')

   fig=px.line(Events_over_time,x="Edition",y="Event")
   fig.update_layout(xaxis_title='Edition', yaxis_title='No. of Events')

   st.title("Number of Events Over The Year")
 
   st.plotly_chart(fig)


   #  importing the data_over_time function from helper.py  to see the Number of Athletes over time

   athletes_over_time=helper.data_over_time(df,'Name')

   fig=px.line(athletes_over_time,x="Edition",y="Name")
   fig.update_layout(xaxis_title='Edition', yaxis_title='No. of Athletes')

   st.title("Number of Athletes Over The Year")
 
   st.plotly_chart(fig)

   # plotting heatmap for seeing the number of event of a particular sport  in paticular year
   st.title("No. of Events Over Time (Every Sport)")
   fig,ax =plt.subplots(figsize=(20,20))
   x=df.drop_duplicates(['Sport','Year','Event'])
   ax =sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
   st.pyplot(fig)

   ## showing the sports list dropdown
   sports_list=df['Sport'].unique().tolist()
   sports_list.sort()
   sports_list.insert(0,'Overall')
   
   selected_sport=st.selectbox('Select a Sport',sports_list)

   
   st.title('Most Successful Athletes')
   x=helper.most_successfull(df,selected_sport)
   st.table(x)

if user_menu =='Country-wise Analysis':
    
    st.sidebar.title('Country-wise Analysis')
    ## showing the country dropdown
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a country',country_list)
    
    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig=px.line(country_df,x='Year',y='Medal')
    st.plotly_chart(fig)   

    ## plotting the heatmap
    st.title(selected_country+" exels in following sports")
    pt=helper.Country_event_heatmap(df,selected_country)
    fig,ax =plt.subplots(figsize=(20,20))
    ax =sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    ## top 10 athletes countrywise
    st.title("Top 10 Athletes  of {}" .format(selected_country))
    top10_df=helper.most_successfull_atheletes_country_wise(df,selected_country)
    st.table(top10_df)

if user_menu =='Athelete wise Analysis':
    # remove duplicates from name as players played in more than one olympic Event
    Athlete_df=df.drop_duplicates(subset=['Name','region'])
    a1=Athlete_df['Age'].dropna()
   # age distribution of player who won GOLD,Silver,Bronze Medal
    a2=Athlete_df[Athlete_df['Medal']=='Gold']['Age'].dropna()
    a3=Athlete_df[Athlete_df['Medal']=='Silver']['Age'].dropna()
    a4=Athlete_df[Athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([a1,a2,a3,a4],['Age Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=900,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)



## finding the age distribution for a specific sport
    x=[]
    Name=[]
    famous_sport=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
       'Cricket', 'Ice Hockey']
    for sport in famous_sport:
        temp_df=Athlete_df[Athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        Name.append(sport)
    fig=ff.create_distplot(x,Name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=900,height=600)
    st.title('Age Distribution wrt Sport(Gold Medalist')
    st.plotly_chart(fig)


   ## showing height vs weight distribution  of player for a particular sport
    sports_list=df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    
 
    # st.title('Height VS Weight Distribution of Participants for {}'.format(selected_sport))
    st.title("Height VS Weight Distribution of Participants")
    selected_sport=st.selectbox('Select a Sport',sports_list)
    hvw=helper.weightvsheight(df,selected_sport)
     # Define the custom color palette with specific colors for each medal
    custom_palette = {'Gold': 'red', 'Silver': 'orange', 'Bronze': 'green', 'No Medal': 'skyblue'}

     # Plot the scatter plot with Seaborn, specifying the custom palette
    fig,ax =plt.subplots(figsize=(15,15))
 
    ax=sns.scatterplot(data=hvw, x='Weight', y='Height', hue='Medal', palette=custom_palette,style='Sex',s=80)
    
    st.pyplot(fig)
    ## finding the number of male and female participants over the years
    menvswomen=helper.men_vs_women(df)
    fig=px.line(menvswomen,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False,width=900,height=600)
    st.title("Men VS Women Participation Over the Years")
    st.plotly_chart(fig)

  
     


