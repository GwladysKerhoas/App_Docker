# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:02:25 2022

@author: gkerhoas
"""

# Question 1
import pandas as pd
import streamlit as st
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.title("Atelier Docker M2 SISE")

st.subheader("Exploration des données des résultats des étudiants de dexux écoles portugaises")

# Question 2
file_path = st.file_uploader("Chargement des données")

# Question 3
st.cache(persist=True)

# Question 4
def upload(file):
    dataframe = pd.read_csv(file, sep=";")
    return dataframe

# Question 5
data = upload(file_path)
st.write(data)

# Question 6

def histchart(df):  
    result = df.groupby(['guardian','schoolsup']).size().reset_index(name='counts')
    fig = px.bar(result, x='guardian', y='counts', color='schoolsup', height=400)
    return fig

st.write(histchart(data))

# Question 7
def piechart(df):       
    result1 = df.groupby(['reason']).size().reset_index(name='counts')
    result2 = df.groupby(['age']).size().reset_index(name='counts')   
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=result1.reason, values=result1.counts, name="Raison"),
                  1, 1)
    fig.add_trace(go.Pie(labels=result2.age, values=result2.counts, name="Age"),
                  1, 2)  
    
    fig.update_layout(
        title_text="Profession des parents")
    return fig




def boxplot(df):       
    categories_count = ['G1', 'G2', 'G3']
    chosen_count = st.selectbox(
       'Quel trimestre ?', categories_count)
    fig = px.box(df, x='studytime', y=chosen_count, color='schoolsup', notched=True)
    return fig


if file_path is not None:
   data = upload(file_path)
   genre = st.sidebar.radio(
       "Genre",
       ('Tout', 'Homme', 'Femme'))
   if genre == 'Femme':
       data = data.loc[data['sex']=='F',:]
   elif genre == 'Homme':
       data = data.loc[data['sex']=='M',:]  

   sorti = st.sidebar.radio(
             "Temps passé avec les amis",
            ('Aucun', 'Très peu', 'Peu','Moyennement','Souvent','Très souvent'))
   if sorti == 'Très peu':
       data = data.loc[data['goout']==1,:]
   elif sorti == 'Peu':
       data = data.loc[data['goout']==2,:]
   elif sorti == 'Moyennement':
       data = data.loc[data['goout']==3,:]
   elif sorti == 'Souvent':
       data = data.loc[data['goout']==4,:]
   elif sorti == 'Très souvent':
       data = data.loc[data['goout']==5,:]

   st.write(data)
   hist = histchart(data)
   st.write(hist)
   pie = piechart(data)
   st.write(pie)
   boxplot = boxplot(data)
   st.plotly_chart(boxplot)