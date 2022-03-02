# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:52:22 2022

@author: gkerhoas
"""






import streamlit as st
import pandas as pd
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Titre et sous-titre
st.title("Atelier Docker M2 SISE 2022 TEST ENCORE TEST")
st.subheader("Exploration des données des résultats des étudiants de deux écoles portuguaise")

file = st.file_uploader("Chargement du fichier")
                 
@st.cache(persist=True)
   
def upload(file):
    dataframe = pd.read_csv(file, sep = ';')
    return dataframe


def histchart(df):  
    result = df.groupby(['guardian','schoolsup']).size().reset_index(name='counts')
    fig = px.bar(result, x='guardian', y='counts', color='schoolsup', height=400)
    return fig


def piechart(df):       
    result1 = df.groupby(['reason']).size().reset_index(name='counts')
    result2 = df.groupby(['age']).size().reset_index(name='counts')   
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=result1.reason, values=result1.counts, name="Raison du choix de l'école"),
                  1, 1)
    fig.add_trace(go.Pie(labels=result2.age, values=result2.counts, name="Age de l'étudiant"),
                  1, 2)  
    
    fig.update_layout(
        title_text="Plus d'information sur l'étudiant")
    return fig


def boxplot(df):       
    categories_count = ['G1', 'G2', 'G3']
    chosen_count = st.selectbox(
       'Quel trimestre ?', categories_count)
    fig = px.box(df, x='studytime', y=chosen_count, color='schoolsup', notched=True)
    return fig
 

if file is not None:
    data = upload(file)
    ecole = st.sidebar.radio(
             "Ecole",
            ('Tout', 'GP', 'MS'))
    if ecole == 'GP':
        data = data.loc[data['school']=='GP',:]
    elif ecole == 'MS':
        data = data.loc[data['school']=='MS',:]  

    rel = st.sidebar.radio(
             "Relationavec les parents",
            ('Aucun', 'Très mauvaise', 'Mauvaise','Neutre','Bonne','Très bonne'))
    if rel == 'Très peu':
        data = data.loc[data['famrel']==1,:]
    elif rel == 'Peu':
        data = data.loc[data['famrel']==2,:]
    elif rel == 'Moyennement':
        data = data.loc[data['famrel']==3,:]
    elif rel == 'Souvent':
        data = data.loc[data['famrel']==4,:]
    elif rel == 'Très souvent':
        data = data.loc[data['famrel']==5,:]
    st.write(data)
    hist = histchart(data)
    st.write(hist)
    pie = piechart(data)
    st.write(pie)
    boxplot = boxplot(data)
    st.plotly_chart(boxplot)
    