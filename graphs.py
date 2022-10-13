import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from collections import Counter

# Function for graphs
@st.experimental_memo(persist="disk")
def transactionByMonth(df):
    st.line_chart(df.groupby("Mois").count()["id_mutation"])

@st.experimental_memo(persist="disk")
def valFonciereByPostalCode(df, code):
    df_user = df[df["code_postal"] == int(code)]
    st.bar_chart(df_user.groupby("Mois").mean()["valeur_fonciere"])

@st.experimental_memo(persist="disk")
def surfaceByLocal(df):
    fig = px.scatter(df, x="surface_terrain", y="type_local")
    st.plotly_chart(fig)

@st.experimental_memo(persist="disk")
def valFonciereByLocal(df, type_local, min_price, max_price):
    df_user = df[(df["type_local"] == type_local) & (df["valeur_fonciere"] > min_price) & (df["valeur_fonciere"] < max_price)]
    fig = px.scatter_mapbox(df_user, lat="latitude", lon="longitude", color="valeur_fonciere", zoom=10, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

@st.experimental_memo(persist="disk")
def mapLocal(df):
    df_local = df['type_local']
    r = Counter(df_local)
    df_local = pd.DataFrame.from_dict(r, orient='index').sort_values(by=0)
    df_local.columns = ['type_local']
    df_local.plot.pie(y='type_local',
                figsize=(8, 8),
                fontsize=16,
                autopct='%.2f',
                legend=False,)
    fig = plt.gcf()
    return fig

@st.experimental_memo(persist="disk")
def averageValeurByPostalCode(df, code_user):
    # We keep only the postal code chosen
    df2 = df[df["code_postal"] == int(code_user)]
    # create a dataframe that contains the average valeur fonciere for each type_local
    df2 = df2.groupby(["type_local"])["valeur_fonciere"].mean()
    # create a dataframe with the type_local and the average valeur fonciere
    df2 = pd.DataFrame({
        "type_local": df2.keys(),
        "valeur_fonciere": [i for i in df2]
    })
    # create a bar chart with plotly
    fig = px.bar(df2, x="type_local", y="valeur_fonciere")
    st.plotly_chart(fig)

@st.experimental_memo(persist="disk")
def nbrPiecePrincipalesMap(df, pieces):
    # create with st.map a map of all the sales that have at least the number of pieces
    # chosen by the user
    df_user = df[df["nombre_pieces_principales"] >= int(pieces)]
    st.map(df_user)