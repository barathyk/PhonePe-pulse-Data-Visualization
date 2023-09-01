import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import json
import os
from git.repo.base import Repo


#creation connection with mysql
mycon =mysql.connector.connect(host='localhost',
                               user='root',
                               password='Barathy@06',
                               database='phonepe_pulse')
mycursor=mycon.cursor(buffered=True)

#settting page configuration for webpage
st.set_page_config(page_title="phonepe Data visualisation",
                                        page_icon="🧊",
                                        layout="wide",
                                        initial_sidebar_state="expanded")

      
selected = option_menu("Welcome To PhonePe Dashboard", ["Home","Transaction and Users","Explore Map"], 
    icons=['house',"bar-chart-line",], 
    menu_icon='menu_button_wide', 
    default_index=0,
    orientation='horizontal',
    styles={"container": {"padding": "0!important", "background-color": "green"},
            "icon": {"color": "yellow", "font-size": "30px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "black"},})


if selected=="Home":
   st.markdown("# :yellow[Data Visualization and Exploration]")
   st.markdown("## :yellow[A User-Friendly Tool Using Streamlit and Plotly]")
   st.write(" ")
   st.write(" ")
   st.markdown("### :blue[Domain :] Fintech")
   st.markdown("### :blue[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
   st.markdown("### :blue[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")


if selected == "Transaction and Users":
   st.markdown("## :violet[Top Charts]")
   colum1,colum2= st.columns([1,1.5],gap="large")
   with colum1:
        Year = st.selectbox("Year", ['2018','2019','2020','2021','2022'])
        Quarter = st.selectbox("Quarter",['1','2','3','4'])
        Type = st.selectbox("Type", ["Transactions", "Users"])
   with colum2:
        st.info(
        """
        #### From this menu we can get insights like :
        - Overall ranking on a particular Year and Quarter.
        - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
        - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
        - Top 10 mobile brands and its percentage based on the how many people use phonepe.
        """,icon="🔍"
        )



   if Type == "Transactions":
        
        # this block will fetch us data based on state wise 
        st.markdown("### :violet[State]")
        mycursor.execute(f"select State, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from agg_transaction where year = {Year} and quarter = {Quarter} group by State order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_Count','Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                            names='State',
                            title='Top 10',
                            color_discrete_sequence=px.colors.qualitative.Light24,
                            hover_data=['Transaction_Count'],
                            labels={'Transaction_Count':'Transaction_Count'})

        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
            
        # this block will fetch us data based on district wise
        st.markdown("### :violet[District]")
        mycursor.execute(f"select Name , sum(Count) as Total_Count, sum(Amount) as Total from map_transaction where year = {Year} and quarter = {Quarter} group by Name order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Name', 'Transaction_Count','Total_Amount'])

        fig = px.pie(df, values='Total_Amount',
                            names='Name',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transaction_Count'],
                            labels={'Transaction_Count':'Transaction_Count'})

        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
            
        # this block will fetch us data based on pincode 
        st.markdown("### :violet[Pincode]")
        mycursor.execute(f"select Entityname, sum(Count) as Total_Transactions_Count, sum(Amount) as Total from top_transaction where year = {Year} and quarter = {Quarter} group by Entityname order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Entityname', 'Count','Amount'])
        fig = px.pie(df, values='Amount',
                            names='Entityname',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Plasma_r,
                            hover_data=['Count'],
                            labels={'Count':'Count'})

        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)


        # # Bar chart for top payment method
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_transaction where year= {Year} and quarter = {Quarter} group by Transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                    title='Transaction Types and Total_Transactions',
                    x="Transaction_type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_Transactions',
                    color_discrete_sequence=px.colors.qualitative.Light24)

        st.plotly_chart(fig,use_container_width=False)

        # Bar chart for district wise transactions
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("States",
                            ('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                              'Chandigargh','Chhattisgarh','Dadra and Nagar Haveli And Daman and diu','Delhi','Goa','Gujarat','Haryana',
                              'Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                              'Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                              'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                              'Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'),index=30)
        
        mycursor.execute(f"select State, Name,Year,Quarter, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, Name,Year,Quarter order by state,Name")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter','Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                    title=selected_state,
                    x="District",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
    
            
# Top Charts - USERS          
   if Type == "Users":
        # col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        # this block will fetch us data based on brand wise
        st.markdown("### :violet[Brands]")
        if Year == 2022 and Quarter in [2,3,4]:
            st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
        else:
            mycursor.execute(f"select Brand, sum(Count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by Brand order by Total_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
            fig = px.pie(df,
                            title='Top 10',
                            values="Total_Users",
                            names="Brand",
                            color='Avg_Percentage',
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            )


            fig.update_traces(textposition='outside', textinfo='percent+label')           
            st.plotly_chart(fig,use_container_width=True)   
    
        # this block will fetch us data based district wise
        st.markdown("### :violet[District]")
        mycursor.execute(f"select District, sum(Registered_User) as Total_Users, sum(App_open) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by District order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(float)
        fig = px.bar(df,
                        title='Top 10',
                        x="Total_Users",
                        y="District",
                        orientation='h',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
              
        # this block will fetch us data based on pincode 
        st.markdown("### :violet[Pincode]")
        mycursor.execute(f"select Name, sum(Registerd_user) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Name order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Name', 'Total_Users'])
        fig = px.pie(df,
                        values='Total_Users',
                        names='Name',
                        title='Top 10',
                        color_discrete_sequence=px.colors.qualitative.Dark24,
                        hover_data=['Total_Users'])
        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
            
        # this block will fetch us data based on state
        st.markdown("### :violet[State]")
        mycursor.execute(f"select State, sum(Registered_user) as Total_Users, sum(App_open) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by State order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        fig = px.pie(df, values='Total_Users',
                            names='State',
                            title='Top 10',
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data=['Total_Appopens'],
                            labels={'Total_Appopens':'Total_Appopens'})

        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

        ## BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("Select State",
                            ['Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                              'Chandigargh','Chhattisgarh','Dadra and Nagar Haveli And Daman and diu','Delhi','Goa','Gujarat','Haryana',
                              'Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                              'Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                              'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                              'Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'],index=30)
        
        # mycursor.execute(f"select State,District,sum(Registered_user) as Total_Users from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,Year,Quarter order by State,District")
        mycursor.execute(f"select  State,Year,Quarter,District,sum(Registered_user) as Total_users,sum(App_Open) as Total_Appopens from map_user where year={Year} and quarter={Quarter} and state='{selected_state}' group by District,State,Year,Quarter order by State,District ")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','Year','Quarter','District', 'Total_Users','Total'])

        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                    title=selected_state,
                    x="District",
                    y="Total_Users",
                    orientation='v',
                    color='Total_Users',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
   
# STATE WISE REPRESENTATION USING INDIA MAP 
if selected =="Explore Map":
   Year = st.selectbox("**Year**",['2018','2019','2020','2021','2022'])
   Quarter = st.selectbox("Quarter",['1','2','3','4'])
   Type = st.selectbox("**Type**", ["Transactions", "Users"])

    
# EXPLORE MAP - TRANSACTIONS
   if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 

        st.markdown("## :violet[Overall State Data - Transactions Amount]")
        mycursor.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by State order by State")
        df = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_amount',
                color_continuous_scale='fall')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
    
        st.markdown("## :violet[Overall State Data - Transactions Count]")
        mycursor.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by State order by State")
        df = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df.Total_Transactions = df.Total_Transactions.astype(int)
        

        fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_Transactions',
                color_continuous_scale='inferno')
        


        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True) 
                
            
# EXPLORE MAP - USERS      
   if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select State, sum(Registered_user) as Total_Users, sum(App_open) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by State order by State")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df.Total_Appopens = df.Total_Appopens.astype(float)
        
        
        fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_Appopens',
                color_continuous_scale='Viridis')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # Overall State Data - TOTAL USERS - INDIA MAP
        st.markdown("## :violet[Overall State Data - Total Users ]")
        mycursor.execute(f"select State, sum(Registered_user) as Total_Users, sum(App_open) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter}  group by State order by State")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df.Total_Appopens = df.Total_Appopens.astype(float)
        
        
        fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_Users',
                color_continuous_scale='Viridis')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        

        