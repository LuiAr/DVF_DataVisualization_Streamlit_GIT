import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import time
from collections import Counter

# We import the py file who contains all the graphs
from graphs import *

# Last part where we create all the visuals
def dataVisualization(data2019 , data2020):
    st.write("---")
    st.markdown("## Data Visualization 🔬")
    st.markdown("")

    # Add a selector to choose wich year user want to see
    year = st.selectbox("Select a year", ["2020", "2019"])
    if (year == "2020"):
        df = data2020
    else:
        df = data2019
    st.write("")

    # Simple line chart to represent the nbr of transaction by month
    st.write("### Number of transaction by month")
    transactionByMonth(df)
    
    # We let the user to select his postal code and will see the average valeur fonciere
    st.write("### Mean *Valeur Fonciere* by postal code")
    code = st.text_input("Entrez votre code postal", "18000")
    valFonciereByPostalCode(df, code)
    st.warning("the data is not very accurate, because we only have 20% of the data")

    # We allow the user to choose a number of *pieces principales*
    st.write("### Repartition in france of sales by number of *pieces principales*")
    pieces = st.slider("Select a minimum number of *pieces principales*", 1, 10, 1)
    nbrPiecePrincipalesMap(df, pieces)

    # Simple scatter with plotly to represent the surface by type of local
    st.write("### *Surface terrain* by the type of *local*")
    surfaceByLocal(df)

    st.write("### *Valeur fonciere* by the type of *local*")
    # We ask the user for infos to precise his search
    type_local = st.selectbox("Select a type of local", ["Appartement","Dépendance", "Local industriel. commercial ou assimilé", "Maison"])
    min_price, max_price = st.select_slider("Select a range of price", options=[0, 100000, 1000000, 5000000, 10000000],value=(0, 10000000))
    
    # Represent on a map the number of transaction following a city, type_local and price
    valFonciereByLocal(df, type_local, min_price, max_price)
    st.success("*Do not forget to zoom out 👀*")

    # We create a cheese to represent the repartition of types of local
    st.write("### Répartition of the type of local in France")
    fig = mapLocal(df)
    st.pyplot(fig)

    # We will let the user to see the average valeur fonciere for each type of local by postal_code
    st.write("### Average *Valeur Fonciere* by postal code")
    # We ask the user for infos to precise his search
    code_user = st.text_input("Code postal", "22100")
    averageValeurByPostalCode(df, code_user)

    if (st.button("Thank you !")):
        st.balloons()