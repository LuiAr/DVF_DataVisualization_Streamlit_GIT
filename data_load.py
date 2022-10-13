import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import time
from collections import Counter

#? Function to load the data and store it in cache
@st.experimental_memo(persist="disk")
def load_data():
    data2019 = pd.read_csv("https://files.data.gouv.fr/geo-dvf/latest/csv/2019/full.csv.gz").sample(frac=0.2)
    data2020 = pd.read_csv("https://files.data.gouv.fr/geo-dvf/latest/csv/2020/full.csv.gz").sample(frac=0.2)

    return data2019, data2020

@st.experimental_memo(persist="disk")
def convert_df(df):
    return df.to_csv().encode('utf-8')

#? Function to import the dataset
def dataImport():
    # Import the Dataset
    entry_msg = st.error("*IMPORTING THE TWO DATASET MAY TAKE SOME TIME FIRST TIME*",icon="🚨")
    data2019, data2020 = load_data()
    entry_msg.empty()
    msg = st.success('DVF 2019 & 2020 imported')
    time.sleep(2)
    msg.empty()

    # Main Infos
    st.markdown("## Data Import 📥")    
    infos = pd.DataFrame({
            "2019" : [data2019.shape[0], data2019.shape[1]],
            "2020" : [data2020.shape[0], data2020.shape[1]]
        })
    infos.index = ["Rows", "Columns"]
    st.table(infos)
    st.info("It represents 20 % of the total data.")

    #! Of course we need to allow the user to download the dataset, of course ... :)
    # add a button to download the data
    if st.button('Download the data 🌐'):
        csv2019 = convert_df(data2019)
        csv2020 = convert_df(data2020)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Download the dataset -->**")
        with col2 :
            st.download_button(
                label="Download 2019 data",
                data=csv2019,
                file_name='data2019.csv',
                mime='text/csv',
            )
        with col3 :
            st.download_button(
                label="Download 2020 data",
                data=csv2020,
                file_name='data2020.csv',
                mime='text/csv',
            )
    else:
        st.markdown("")
    return data2019, data2020
