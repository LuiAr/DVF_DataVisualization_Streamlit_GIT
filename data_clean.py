import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import time
from collections import Counter



@st.experimental_memo(persist="disk")
def modifyTypes(data2019, data2020):
    data2019["date_mutation"] = pd.to_datetime(data2019["date_mutation"])
    data2019["Mois"] = data2019["date_mutation"].dt.month
    data2019["Jour"] = data2019["date_mutation"].dt.day
    data2019["Année"] = data2019["date_mutation"].dt.year

    data2020["date_mutation"] = pd.to_datetime(data2020["date_mutation"])
    data2020["Mois"] = data2020["date_mutation"].dt.month
    data2020["Jour"] = data2020["date_mutation"].dt.day
    data2020["Année"] = data2020["date_mutation"].dt.year

    # We pars to int the column code_postal
    data2019["code_postal"] = data2019["code_postal"].astype(int)
    data2020["code_postal"] = data2020["code_postal"].astype(int)

    # same for valeur fonciere
    data2019["valeur_fonciere"] = data2019["valeur_fonciere"].astype(int)
    data2020["valeur_fonciere"] = data2020["valeur_fonciere"].astype(int)

    return data2019, data2020

    
# Function to clean the data, remove all missing data, remove columns we don't need etc...
def dataCleaning(data2019, data2020):
    st.write("---")
    st.markdown("## Data Cleaning 🧹")
    st.markdown("")

    st.markdown("We will look at each columns and see if we can drop some of them.")
    st.markdown("**Missing values for each column :**")

    #? We add radio buttons to allow user to interact with this little table
        
    # Store the initial value of widgets in session state
    if "vis_empty_col" not in st.session_state:
        st.session_state.disabled = False

    #? We create the dataframe that will hold the number of missing values for each column
    infos = pd.DataFrame({
            "2019" : data2019.isnull().sum(),
            "2020" : data2020.isnull().sum()
        })
    #? We add a variable to skip the table if user want
    skip_table = False

    #? We add a checkbox to allow the user to disable the table
    if st.checkbox("Disable the table"):
        st.session_state.disabled = True
        skip_table = True
    else:
        st.session_state.disabled = False

    if (skip_table == False): 
        st.table(infos)

    #? Now we remove all the columns that have more than 50% of missing values
    data2019 = data2019.dropna(axis=1, thresh=data2019.shape[0]*0.5)
    data2020 = data2020.dropna(axis=1, thresh=data2020.shape[0]*0.5)

    st.info("We delete all rows with no data")
    data2019 = data2019.dropna()
    data2020 = data2020.dropna()

    st.write("### Number of rows and columns after cleaning :")
    infos = pd.DataFrame({
            "2019" : [data2019.shape[0], data2019.shape[1]],
            "2020" : [data2020.shape[0], data2020.shape[1]]
        })
    infos.index = ["Rows", "Columns"]
    st.table(infos)

    # lastly we modify certain types, this will help us in data visualization
    # We add a column to have the month day and year of each transaction
    data2019, data2020 =  modifyTypes(data2019, data2020)

    return data2019, data2020