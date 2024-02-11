import numpy as np
import pandas as pd


## creating a fuction for showing data for a specific year and specific country
def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    flag=0
    if year=='Overall' and country =='Overall':
        temp_df=medal_df
    if year=='Overall' and country !='Overall':
        flag=1
        temp_df=medal_df[medal_df['region'] == country]
    if year!='Overall' and country =='Overall':
        temp_df=medal_df[medal_df['Year']==year]
    if year!='Overall' and country !='Overall':
        temp_df=medal_df[(medal_df['region']==country) &(medal_df['Year']==year)]
        
        
    # this if is not used because if we set a specific country and overall year then it will show the total
    # medals not but not year that is why we here group by Year
    if flag==1:
        # this
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:   
    # making a dataframe  on the basis of region
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']

     # convert the datatype of all columns into int
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')
    

    return x


    ## this function will show the normal view i.e. default
def medal_tally(df):
    
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    # medals by region
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    # adding a total column at the end 
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    # convert the datatype of all columns into int
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally
    
    
def country_year_list(df):
    ## for year wise selection of data
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    
    ## similarly for country wise selection of data
    # fetching the unique values of countries and converting into list
    country=np.unique(df['region'].dropna().values).tolist()
   # sorting the country values
    country.sort()
   # insert the Overall at index 0
    country.insert(0,'Overall')


    return years,country
 
def data_over_time(df,col):
    # no of events over the yea
    # Drop duplicates based on 'Year' and given column i.e. col, count occurrences of each unique 'Year' value and sort by year 
    col_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values(by=['Year'])
    
    # Rename columns
    col_over_time.rename(columns={'Year':'Edition','count': col}, inplace=True)

    # events_over_time.rename(columns={'index':'Edition','Year':'No. of Events'},inplace=True)
    return col_over_time


### finding the most successfull person as per the number of medals
def most_successfull(df,sport):
    # As we are finding the most successfull person as per the number of medals so
    #we can drop na values from medal

    temp_df=df.dropna(subset=["Medal"])
                      
    if sport !='Overall':
        ## if we want to find answer by sportswise else show overall
        temp_df=temp_df[temp_df['Sport']==sport]
    
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'Name':'Name','count':'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df,country):
    ## country Wise medal Tally per year(line plot)
    ## dropna where medals are NaN
    temp_df=df.dropna(subset=['Medal'])
    ##  we have data such that the medal are not correct as the medals are counted for each team member so we preform drop_duplicated 
    ## on some of the aggregated column i.e.
    temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    ## finding the number of medals of a specific country in a secific year to plot a line plot for showing 
    ## number of medals yearwise
    new_df=temp_df[temp_df['region']==country]
    final_df= new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def Country_event_heatmap(df,country):
    # plotting the heatmap for various years for various sports for a particular countries 
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    new1_df=temp_df[temp_df['region']==country]
    pt=new1_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successfull_atheletes_country_wise(df,country):
    # As we are finding the most successfull person as per the Country so
    # we can drop na values from medal
    temp_df=df.dropna(subset=["Medal"])
                      

        ## if we want to find answer by sportswise else show overall
    temp_df=temp_df[temp_df['region']==country]
    
    x=temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport',]].drop_duplicates('Name')
    x.rename(columns={'Name':'Name','count':'Medals'},inplace=True)
    return x

def weightvsheight(df,sport):
    ### dropping duplictes by region and by name
    Athlete_df=df.drop_duplicates(subset=['Name','region'])

    ## plot the scatter plot for showing the players with medal,no medal,sexwise for a particular sport
    Athlete_df['Medal'].fillna("No Medal",inplace=True)
    
    if sport!='Overall':
        temp_df=Athlete_df[Athlete_df['Sport']== sport ]
        return temp_df
    else :
        return Athlete_df

def men_vs_women(df):
    Athlete_df=df.drop_duplicates(subset=['Name','region'])
    ## finding the number of male and female participants over the year

    men=Athlete_df[Athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    women=Athlete_df[Athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    return final


    
   