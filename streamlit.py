import streamlit as st
from model import MovieRecommender
from data_loading_and_preprocessing import DataPreprocessor
obj=MovieRecommender()
st.header('Movie recommendation system')  #adding title
st.subheader('This recommender system is based on collaborative filtering techniques using cosine similarity')
gender=['M','F']
age=['Under 18', '56+', '25-34', '50-55', '18-24', '45-49', '35-44']
gender_selected=st.selectbox("select your gender",gender)
age_selected=st.selectbox("select your age bracket",age) 
user_id,data___=obj.get_data_with_user_ids(gender_selected,age_selected)

selected_user=st.selectbox("select your user_id",user_id[0])
if st.button('Show Recommendation'):
    movies=obj.recommend(gender_selected,age_selected,selected_user,data___)
    movies
