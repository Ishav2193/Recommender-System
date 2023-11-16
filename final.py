import pandas as pd
import numpy as np
import warnings
import streamlit as st
from numpy.linalg import norm
warnings.filterwarnings('ignore')

ratings=pd.read_csv('https://raw.githubusercontent.com/AkshatSan/MovieRecomm/main/data/ratings.csv',sep='\t')
users=pd.read_csv('https://raw.githubusercontent.com/AkshatSan/MovieRecomm/main/data/users.csv',encoding='cp1252',sep='\t')
movies = pd.read_csv('movies.csv',sep='\t',encoding='latin-1', usecols=['movie_id', 'title', 'genres'])

users.drop(columns='Unnamed: 0',axis=1,inplace=True)
ratings.drop(columns='Unnamed: 0',axis=1,inplace=True)
user_rating=users.merge(ratings,how='inner',on='user_id')
df=user_rating.merge(movies,how='inner',on='movie_id')
df.drop(columns=['user_id','timestamp','occ_desc','movie_id'],axis=1,inplace=True)
df.rename(columns={'user_emb_id':'user_id',
                   'movie_emb_id':'movie_id'},inplace=True)
a=df.groupby('title')['user_id'].count()>=100
movies_to_consider=a[a]
movies_to_consider=list(movies_to_consider.index)
r=df['title'].isin(movies_to_consider)
df=df[r]

df_female=df[df["gender"]=='F']
df_male=df[df["gender"]=='M']

df_female.drop(columns='gender',axis=1,inplace=True)
df_male.drop(columns='gender',axis=1,inplace=True)

df_female.drop(columns='zipcode',axis=1,inplace=True)
df_male.drop(columns='zipcode',axis=1,inplace=True)

d={}
c=1
for i in df_female['age_desc'].unique():
    d[i]=c
    c+=1

df_female['age_desc']=df_female['age_desc'].map(d)
df_male['age_desc']=df_male['age_desc'].map(d)

df_female.drop(columns=['age','occupation'],axis=1,inplace=True)
df_male.drop(columns=['age','occupation'],axis=1,inplace=True)

def convert_into_list(obj):
    l=[]
    s= str(obj)
    if s.count('|')==0:
        l.append(s)
    else:
        l.append(s.split('|'))
        l=[i for t in l for i in t]
    return l 

df_female['genres']=df_female['genres'].apply(convert_into_list)
df_male['genres']=df_male['genres'].apply(convert_into_list)

df_female=df_female.explode('genres')
df_male=df_male.explode('genres')

n_d={}
for i,j in list(zip(df_male['genres'].value_counts().sort_values(ascending=False).index,np.linspace(5,1,18))):
    n_d[i]=j

df_male['genres']=df_male['genres'].map(n_d)

n_d_f={}
for i,j in list(zip(df_female['genres'].value_counts().sort_values(ascending=False).index,np.linspace(5,1,18))):
    n_d_f[i]=j

df_female['genres']=df_female['genres'].map(n_d_f)

df_female['weighted_average']=(2*df_female['rating']+df_female['genres'])/3
df_male['weighted_average']=(2*df_male['rating']+df_male['genres'])/3

f_age_1=df_female[df_female['age_desc']==1]
f_age_2=df_female[df_female['age_desc']==2]
f_age_3=df_female[df_female['age_desc']==3]
f_age_4=df_female[df_female['age_desc']==4]
f_age_5=df_female[df_female['age_desc']==5]
f_age_6=df_female[df_female['age_desc']==6]
f_age_7=df_female[df_female['age_desc']==7]

m_age_1=df_male[df_male['age_desc']==1]
m_age_2=df_male[df_male['age_desc']==2]
m_age_3=df_male[df_male['age_desc']==3]
m_age_4=df_male[df_male['age_desc']==4]
m_age_5=df_male[df_male['age_desc']==5]
m_age_6=df_male[df_male['age_desc']==6]
m_age_7=df_male[df_male['age_desc']==7]

def drop(data,col):
    return data.drop(columns=col,axis=1,inplace=True)

drop(f_age_1,'age_desc')
drop(f_age_2,'age_desc')
drop(f_age_3,'age_desc')
drop(f_age_4,'age_desc')
drop(f_age_5,'age_desc')
drop(f_age_6,'age_desc')
drop(f_age_7,'age_desc')

drop(m_age_1,'age_desc')
drop(m_age_2,'age_desc')
drop(m_age_3,'age_desc')
drop(m_age_4,'age_desc')
drop(m_age_5,'age_desc')
drop(m_age_6,'age_desc')
drop(m_age_7,'age_desc')

from typing import List           


#"""
#THE BELOW FUNCTION WILL GOING TO RETURN SIMILAR USERS THAT WE HAVE SELECTED
#"""
def recommend_users(gender,age,user_id,reqd_data):
    similar_user_ids=[]
    mapping_dict_for_age={'Under 18':1, '56+':7, '25-34':3, '50-55':4, '18-24':2, '45-49':6, '35-44':5} 
    age=pd.Series(age).map(mapping_dict_for_age).values[0]
    pt=reqd_data.pivot_table(values='weighted_average',index='user_id',columns='title').fillna(0)
    pt1=pt
    p=pd.DataFrame(pt)
    p=p.reset_index()
    cos_simi=[]
    #ind=p.index[p['user_id']==user_id][0]
    ind=list(pt.index).index(user_id)
    lst=p[p["user_id"]==user_id].values[0][1:]
    for i in p.index:
        row_1=p.iloc[i].values[1:]
        cos_simi.append(np.dot(row_1,lst)/(norm(row_1))*norm(lst))
    similar_items=sorted(list(enumerate(cos_simi)),key=lambda x:x[1],reverse=True)[1:6]    

    for i in similar_items:
        similar_user_ids.append(pt.index[i[0]])    

    return (similar_user_ids,
            pt,
            p)   

def recommend(gender,age,user_id,reqd_data):
    similar_user_ids,pt,p=recommend_users(gender,age,user_id,reqd_data)
    # dd={}
    # for i in list(enumerate(pt.index)):      #pt.index contains users ids
    #     dd[i[1]]=i[0]
    # new_l=[]   #new_l contains index of user_ids 
    # for i in similar_user_ids:
    #     new_l.append(dd[i])     
    # movies_recommended=[]
    # for i in new_l:
    #     ind_for_row=pt.index[i]
    #     ind_for_col=np.argmax(pt[pt.index==pt.index[ind_for_row]],axis=1)
    #     movies_recommended.append(pt.columns[ind_for_col])
    movies_recommended=[]
    for i in similar_user_ids:
        get_row=p[p['user_id']==i]
        get_row_values=get_row.values[0][1:]
        get_col_ind=np.argmax(get_row_values,axis=0)
        
        reqd_ind=get_col_ind+1
        movies_recommended.append(p.columns.tolist()[reqd_ind])
    return list(set(movies_recommended))


import streamlit as st
st.header('Movie recommendation system')  #adding title
st.subheader('This recommender system is based on collaborative filtering techniques using cosine similarity')
gender=df['gender'].unique()
age=['Under 18', '56+', '25-34', '50-55', '18-24', '45-49', '35-44']
gender_selected=st.selectbox("select your gender",gender)
user_id=[]
age_selected=st.selectbox("select your age bracket",age) 
data___=pd.DataFrame()
if gender_selected=='M':
    if age=='Under 18':
        user_id.append(m_age_1['user_id'].unique())
        data___=m_age_1
    elif age=='18-24':
        user_id.append(m_age_2['user_id'].unique())
        data___=m_age_2
    elif age=='25-34':
        user_id.append(m_age_3['user_id'].unique())
        data___=m_age_3
    elif age=='50-55':
        user_id.append(m_age_4['user_id'].unique())
        data___=m_age_4
    elif age=='35-44':
        user_id.append(m_age_5['user_id'].unique())
        data___=m_age_5
    elif age=='45-49':
        user_id.append(m_age_6['user_id'].unique())
        data___=m_age_6
    else:
        user_id.append(m_age_7['user_id'].unique())
        data___=m_age_7
else:
    if age=='Under 18':
        user_id.append(f_age_1['user_id'].unique())
        data___=f_age_1
    elif age=='18-24':
        user_id.append(f_age_2['user_id'].unique())
        data___=f_age_2
    elif age=='25-34':
        user_id.append(f_age_3['user_id'].unique())
        data___=f_age_3
    elif age=='50-55':
        user_id.append(f_age_4['user_id'].unique())
        data___=f_age_4
    elif age=='35-44':
        user_id.append(f_age_5['user_id'].unique())
        data___=f_age_5
    elif age=='45-49':
        user_id.append(f_age_6['user_id'].unique())
        data___=f_age_6
    else:
        user_id.append(f_age_7['user_id'].unique()) 
        data___=f_age_7

selected_user=st.selectbox("select your user_id",user_id[0])
if st.button('Show Recommendation'):
    movies=recommend(gender_selected,age_selected,selected_user,data___)
    movies
