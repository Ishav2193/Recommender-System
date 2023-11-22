import pandas as pd
import numpy as np
import warnings
from numpy.linalg import norm
from dataclasses import dataclass
#import logging
from data_loading_and_preprocessing import DataPreprocessor

obj=DataPreprocessor()

class MovieRecommender:

    '''

    THE BELOW FUNCTION IS USED TO GET FILTERED DATA ON BASIS OF GENDER AND AGE-BRACKET SELECTED

    '''
    def get_data_with_user_ids(self,gender:str,age:str):
        #logging.info('started with get_data_with_users_block')
        df_female,df_male=obj.get_genres_into_numerical()
        user_id=[]
        data___=pd.DataFrame()
        d={'Under 18': 1,'18-24': 2,'25-34': 3,'50-55': 4,'35-44': 5,'45-49': 6,'56+': 7}
        if gender=='M':
            data___=df_male[df_male['age_desc']==d[age]]
            user_id.append(data___['user_id'].unique())
            return user_id,data___
        else:
            data___=df_female[df_female['age_desc']==d[age]]
            user_id.append(data___['user_id'].unique()) 
            return user_id,data___

    '''

    THE BELOW FUNCTION IS USED TO GET TOP 5 USERS THAT HAVE SIMILAR TASTE TO PARTICULAR USER
    WHOSE GENDER,AGE,USER_ID IS GIVEN

    '''

    def recommend_users(self,gender,age,user_id,reqd_data):
        similar_user_ids=[]
        mapping_dict_for_age={'Under 18':1, '56+':7, '25-34':3, '50-55':4, '18-24':2, '45-49':6, '35-44':5} 
        age=pd.Series(age).map(mapping_dict_for_age).values[0]
        pt=reqd_data.pivot_table(values='weighted_average',index='user_id',columns='title').fillna(0)
        p=pd.DataFrame(pt)
        p=p.reset_index()
        cos_simi=[]
        ind=list(pt.index).index(user_id)
        lst=p[p["user_id"]==user_id].values[0][1:]
        for i in p.index:
            row_1=p.iloc[i].values[1:]
            cos_simi.append(np.dot(row_1,lst)/(norm(row_1)*norm(lst)))
        similar_items=sorted(list(enumerate(cos_simi)),key=lambda x:x[1],reverse=True)[1:6]    

        for i in similar_items:
            similar_user_ids.append(pt.index[i[0]])    

        return (similar_user_ids,
                pt,
                p) 
    
    '''

    THE BELOW FUNCTION HELP US GET THE LIST OF TOP 5 RECOMMENDED MOVIES FOR A PARTICULAR USER.
    
    '''

    def recommend(self,gender:str,age:str,user_id,reqd_data):
        similar_user_ids,pt,p=self.recommend_users(gender,age,user_id,reqd_data)
        movies_recommended=[]
        for i in similar_user_ids:
            get_row=p[p['user_id']==i]
            get_row_values=get_row.values[0][1:]
            get_col_ind=np.argmax(get_row_values,axis=0)        
            reqd_ind=get_col_ind+1
            movies_recommended.append(p.columns.tolist()[reqd_ind])
        return list(set(movies_recommended))
    

   

