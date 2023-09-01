import json
import pandas as pd
import os

# opening the localy saved file 
data =r"D:/pulse/data/aggregated/transaction/country/india/state/"
aggregate_transactions =os.listdir(data)
# function to get aggregate trasanction data
def aggregate_transaction(filename,filepath):

    trans_a = {'State':[],'Year':[],'Quarter':[],'Transaction_type':[],'Transaction_count':[],'Transaction_amount':[]}
    
    for state in aggregate_transactions:
        cur_state = data + state + "/"
        agg_year_list = os.listdir(cur_state)

        for year in agg_year_list:
            cur_year = cur_state + year + "/"
            agg_file_list = os.listdir(cur_year)

            for file in agg_file_list:
                cur_file = cur_year + file
                datas = open(cur_file, 'r')
                A = json.load(datas)

                for i in A['data']['transactionData']:
                    name = i['name']
                    count = i['paymentInstruments'][0]['count']
                    amount = i['paymentInstruments'][0]['amount']
                    trans_a['Transaction_type'].append(name)
                    trans_a['Transaction_count'].append(count)
                    trans_a['Transaction_amount'].append(amount)
                    trans_a['State'].append(state)
                    trans_a['Year'].append(year)
                    trans_a['Quarter'].append(int(file.strip('.json')))
                
    return pd.DataFrame(trans_a)
filename=aggregate_transactions
filepath=data
df_trans=aggregate_transaction(filename,filepath)  

# this mapping function is unique method in pandas as it will allow to change/replace existing name with new name.
mappings={'andaman-&-nicobar-islands':'Andaman & Nicobar',
  'andhra-pradesh':'Andhra Pradesh',
   'arunachal-pradesh':'Arunachal Pradesh',
   'assam':'Assam',
   'bihar':'Bihar',
   'chandigarh':'Chandigargh',
   'chhattisgarh':'Chhattisgargh',
   'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu',
   'delhi':'Delhi',
   'goa':'Goa',
   'gujarat':'Gujarat',
   'haryana':'Haryana',
   'himachal-pradesh':'Himachal Pradesh',
   'jammu-&-kashmir':'Jammu & Kashmir',
   'jharkhand':'Jharkhand',
   'karnataka':'Karnataka',
   'kerala':'Kerala',
   'ladakh':'Ladakh',
   'lakshadweep':'Lakshadweep',
   'madhya-pradesh':'Madhya Pradesh',
   'maharashtra':'Maharashtra',
   'manipur':'Manipur',
   'meghalaya':'Meghalaya',
   'mizoram':'Meghalaya',
   'nagaland':'Nagaland',
   'odisha':'Odisha',
   'puducherry':'Puducherry',
   'punjab':'Punjab',
   'rajasthan':'Rajasthan',
   'sikkim':'sikkim',
   'tamil-nadu':'Tamil Nadu',
   'telangana':'Telangana',
   'tripura':'Trippura',
   'uttar-pradesh':'Uttar Pradesh',
   'uttarakhand':'Uttarakhand',
   'west-bengal':'West Bengal'}
dff=df_trans['State'].map(mappings)
df_trans['State']=dff


# checking null values
df =df_trans.isnull().sum()

# opening the localy saved file 
data2=r"D:/pulse/data/aggregated/user/country/india/state/"
aggregate_users =os.listdir(data2)
# function to get data from aggregate user
def aggregate_user(filename,filepath):
    
    user_a={'State':[],'Year':[],'Quarter':[],'Brand':[],'Count':[],'Percentage':[]}
    
    for state in aggregate_users:
        State = data2 + state + "/"
        agg_users = os.listdir(State)

        for year in agg_users:
            Year = State + year + "/"
            agg_file_list = os.listdir(Year)

            for file in agg_file_list:
                File = Year + file
                datas = open(File, 'r')
                B= json.load(datas)
                try:
                    for i in B['data']['usersByDevice']:
                        brand = i['brand']
                        count = i['count']
                        percentage = i['percentage']
                        user_a['Brand'].append(brand)
                        user_a['Count'].append(count)
                        user_a['Percentage'].append(percentage)
                        user_a['State'].append(state)
                        user_a['Year'].append(year)
                        user_a['Quarter'].append(int(file.strip('.json')))
                except:
                    pass
                
    return pd.DataFrame(user_a)

filename=aggregate_users
filepath=data2
df_user=aggregate_user(filename,filepath)

# to get data from map transaction from local directory
data3 =r"D:/pulse/data/map/transaction/hover/country/india/state/"
map_trans =os.listdir(data3)

# function to get map trasanction data
def map_transaction(filename,filepath):
    
    map_t ={'State':[],'Year':[],'Quarter':[],'Name':[],'Count':[],'Amount':[]}
    for state in map_trans:
        State =data3 + state +"/"
        map_year =os.listdir(State)
        
        for year in map_year:
            Year =State + year + "/"
            map_file =os.listdir(Year)
            
            for file in map_file:
                File = Year + file
                datas =open(File,'r')
                map_data =json.load(datas)
                
                for i in map_data['data']['hoverDataList']:
                    name =i['name']
                    count =i['metric'][0]['count']
                    amount =i['metric'][0]['amount']
                    map_t['Name'].append(name)
                    map_t['Count'].append(count)
                    map_t['Amount'].append(amount)
                    map_t['State'].append(state)
                    map_t['Year'].append(year)
                    map_t['Quarter'].append(int(file.strip('.json')))
                    
    return pd.DataFrame(map_t)

filename =map_trans
filepath =data3
df_mt=map_transaction(filename,filepath)


# to get data from map user from local directory
data4=r"D:/pulse/data/map/user/hover/country/india/state/"
map_users =os.listdir(data4)

# function to get map user data
def map_user(filename,filepath):
    map_u ={'State':[],'Year':[],'Quarter':[],'District':[],'Registered_user':[],'App_open':[]}
    for state in map_users:
        State = data4 + state +"/"
        map_year =os.listdir(State)
        
        for year in map_year:
            Year = State + year + "/"
            map_file =os.listdir(Year)
            
            for file in map_file:
                File = Year + file 
                datas =open(File,'r')
                user_data=json.load(datas)
                
                for i in user_data['data']['hoverData'].items():
                    district = i[0]
                    registered =i[1]['registeredUsers']
                    apps =i[1]['appOpens']
                    map_u['District'].append(district)
                    map_u['Registered_user'].append(registered)
                    map_u['App_open'].append(apps)
                    map_u['State'].append(state)
                    map_u['Year'].append(year)
                    map_u['Quarter'].append(int(file.strip('.json')))
                    
    return pd.DataFrame(map_u)

filename=map_users
filepath=data4
df_mu =  map_user(filename,filepath)


# to get data from top transaction from local directory
data5 =r"D:/pulse/data/top/transaction/country/india/state/"
top_trans=os.listdir(data5)


# function to get top transaction data
def top_transactions(filename,filepath):
    
    top_t ={'State':[],'Year':[],'Quarter':[],'Entityname':[],'Count':[],'Amount':[]}
    for state in top_trans:
        State = data5 + state + "/"
        top_year =os.listdir(State)
        
        for year in top_year:
            Year = State + year + "/"
            top_file =os.listdir(Year)
            
            for file in top_file:
                File = Year + file
                datas =open(File,'r')
                top_data =json.load(datas)
                
                for i in top_data['data']['pincodes']:
                    entityname = i['entityName']
                    count =i['metric']['count']
                    amount =i['metric']['amount']
                    top_t['Entityname'].append(entityname)
                    top_t['Count'].append(count)
                    top_t['Amount'].append(amount)
                    top_t['State'].append(state)
                    top_t['Year'].append(year)
                    top_t['Quarter'].append(int(file.strip('.json')))
                    
    return pd.DataFrame(top_t)

filename =top_trans
filepath =data5
df_tt= top_transactions(filename,filepath)

# null value imputation
df =df_tt.fillna(method='ffill')


# to get data from top user from local directory
data6 =r"D:/pulse/data/top/user/country/india/state/"
top_users=os.listdir(data6)

# function to get top transaction data
def top_user(filename,filepath):
    
    top_u ={'State':[],'Year':[],'Quarter':[],'Name':[],'Registerd_user':[]}
    
    for state in top_users:
        State = data6 + state +"/" 
        top_year =os.listdir(State)
        
        for year in top_year:
            Year = State + year +"/"
            top_file=os.listdir(Year)
            
            for file in top_file:
                File=Year + file
                datas =open(File,'r')
                user_data=json.load(datas)
                
                for i in user_data['data']['pincodes']:
                    name =i['name']
                    user =i['registeredUsers']
                    top_u['Name'].append(name)
                    top_u['Registerd_user'].append(user)
                    top_u['State'].append(state)
                    top_u['Year'].append(year)
                    top_u['Quarter'].append(int(file.strip('.json')))
                    
        
    return pd.DataFrame(top_u)

filename =top_users
filepath =data6
df_tu=top_user(filename,filepath)

#  comverting dataframes to csv file
df_trans.to_csv('agg_transaction.csv',index=False) 
df_user.to_csv('agg_user.csv',index=False) 
df_mt.to_csv('map_transaction.csv',index=False) 
df_mu.to_csv('map_user.csv',index=False) 
df.to_csv('top_transaction.csv',index=False) 
df_tu.to_csv('top_user.csv',index=False)

# creating connection to mysql
import mysql.connector

mycon =mysql.connector.connect(host='localhost',
                              user='root',
                              password='password',
                              database='phonepe_pulse')

mycursor =mycon.cursor()

# creating tables in mysql
mycursor.execute("create table agg_transaction(State varchar(150),Year int,Quarter int,Transaction_type varchar(200),Transaction_count int,Transaction_amount double)")
mycursor.execute("create table agg_user(State varchar(200),Year int,Quarter int,Brand varchar(150),Count int,Percentage double)")
mycursor.execute("create table map_transaction(State varchar(200),Year int,Quarter int,Name varchar(150),Count int,Amount double)")
mycursor.execute("create table map_user(State varchar(200),Year int,Quarter int,District varchar(200),Registered_user int,App_open int) ")
mycursor.execute("create table top_transaction(State varchar(200),Year int,Quarter int,Entityname int,Count int,Amount double)")
mycursor.execute("create table top_user(State varchar(200),Year int,Quarter int,Name int,Registerd_user int)")
mycon.commit()

# inserting into tables 
data = pd.read_csv('agg_transaction.csv')

for i in data.itertuples(index=False):
    insert_t=tuple(i)
    qry ="insert into agg_transaction values(%s,%s,%s,%s,%s,%s)"
    mycursor.execute(qry,insert_t)
    mycon.commit()

# inserting into tables 
data1 =pd.read_csv('agg_user.csv')

for i in data1.itertuples(index=False):
    insert_u=tuple(i)
    qry1="insert into agg_user values(%s,%s,%s,%s,%s,%s)"
    mycursor.execute(qry1,insert_u)
    mycon.commit()

# inserting into tables 
data2 =pd.read_csv('map_transaction.csv')

for i in data2.itertuples(index=False):
    insert_mt=tuple(i)
    qry2="insert into map_transaction values(%s,%s,%s,%s,%s,%s)"
    mycursor.execute(qry2,insert_mt)
    mycon.commit()

# inserting into tables 
data3 =pd.read_csv('map_user.csv')

for i in data3.itertuples(index=False):
    insert_mu=tuple(i)
    qry3="insert into map_user values(%s,%s,%s,%s,%s,%s)"
    mycursor.execute(qry3,insert_mu)
    mycon.commit()

# inserting into tables 
data4 =pd.read_csv('top_transaction.csv')

for i in data4.itertuples(index=False):
    insert_tt=tuple(i)
    qry4="insert into top_transaction values(%s,%s,%s,%s,%s,%s)"
    mycursor.execute(qry4,insert_tt)
    mycon.commit()

# inserting into tables 
data5 =pd.read_csv('top_user.csv')

for i in data5.itertuples(index=False):
    insert_tu=tuple(i)
    qry5="insert into top_user values(%s,%s,%s,%s,%s)"
    mycursor.execute(qry5,insert_tu)
    mycon.commit()

# commamd to check list of that created 
mycursor.execute("show tables")
mycursor.fetchall()



