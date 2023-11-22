import pandas as pd
import numpy as np
#import warnings
from utils import Utils
#import logging
from numpy.linalg import norm
#warnings.filterwarnings('ignore')
from dataclasses import dataclass


'''
DATASET : MOVIE LENS 1M -> CONTAINS 3 DATASETS (RATINGS,USERS,MOVIES).

PROBLEM STATEMENT : WE NEED TO RECOMMEND USER TO WATCH MOVIES WHICH HAVE BEEN LIKED BY USERS OF SIMILAR
KIND. 

'''


@dataclass
class DataLoader:
    ratings=pd.read_csv('https://raw.githubusercontent.com/AkshatSan/MovieRecomm/main/data/ratings.csv',sep='\t')
    users=pd.read_csv('https://raw.githubusercontent.com/AkshatSan/MovieRecomm/main/data/users.csv',encoding='cp1252',sep='\t')
    movies = pd.read_csv('movies.csv',sep='\t',encoding='latin-1', usecols=['movie_id', 'title', 'genres'])
       


class DataPreprocessor:

    def __init__(self):
        self.ingestion_config=DataLoader()

    def preprocessed_data(self):
        #logging.info('entered preprocessed block')
        #logging.info('started merging user and ratings')
        user_rating=self.ingestion_config.users.merge(self.ingestion_config.ratings,how='inner',on='user_id')
        #logging.info('started merging all three datasets')
        df=user_rating.merge(self.ingestion_config.movies,how='inner',on='movie_id')
        df.drop(columns=['user_id','timestamp','occ_desc','movie_id','zipcode'],axis=1,inplace=True)
        df.rename(columns={'user_emb_id':'user_id',
                   'movie_emb_id':'movie_id'},inplace=True)
        movies_with_rating_greater_than_100=df.groupby('title')['user_id'].count()>=100
        movies_to_consider=movies_with_rating_greater_than_100[movies_with_rating_greater_than_100]
        movies_to_consider=list(movies_to_consider.index)
        r=df['title'].isin(movies_to_consider)
        #logging.info('filtering the dataset required')
        df=df[r]

        return df

    def get_male_female_data(self):
        data=self.preprocessed_data()
        #logging.info('segregate data on basis of gender')
        df_female=data[data["gender"]=='F']
        df_male=data[data["gender"]=='M']
        # df_female.drop(columns=['age','gender','occupation'],axis=1,inplace=True)
        # df_male.drop(columns=['age','gender','occupation'],axis=1,inplace=True)
        #logging.info('creating dictionary for age_desc')
        d={}
        c=1
        for i in df_female['age_desc'].unique():
            d[i]=c
            c+=1

        df_female['age_desc']=df_female['age_desc'].map(d)
        df_male['age_desc']=df_male['age_desc'].map(d)   

        return (df_female,
                df_male) 
    
    def get_genres_into_numerical(self):
        df_female,df_male=self.get_male_female_data()
        df_female['genres']=df_female['genres'].apply(Utils.convert_into_list)
        df_male['genres']=df_male['genres'].apply(Utils.convert_into_list)
        df_female=df_female.explode('genres')
        df_male=df_male.explode('genres')
        #logging.info('convert genres column to numerical value')
        n_d={}
        for i,j in list(zip(df_male['genres'].value_counts().sort_values(ascending=False).index,np.linspace(5,1,18))):
            n_d[i]=j

        df_male['genres']=df_male['genres'].map(n_d)

        n_d_f={}
        for i,j in list(zip(df_female['genres'].value_counts().sort_values(ascending=False).index,np.linspace(5,1,18))):
            n_d_f[i]=j

        df_female['genres']=df_female['genres'].map(n_d_f)
        #logging.info('creating a new column for weighted average of genres and ratings')

        df_female['weighted_average']=(2*df_female['rating']+df_female['genres'])/3
        df_male['weighted_average']=(2*df_male['rating']+df_male['genres'])/3

        return (df_female,
                df_male)
        