import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import time
from collections import Counter


def main_page():
    st.markdown("")

def DVF():
    st.markdown("")

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
    data2019, data2020 = load_data()
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


# Main function that will call all the other functions
def main():
    # Sidebar
    st.sidebar.markdown("# Choose a page 📚")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.warning("if you'r having issues running the app, try to delete the cache")

    # Main Page
    st.markdown("# DVF exploration 📊")
    st.markdown("---")

    # DataImport
    data2019, data2020 = dataImport()

    # DataCleaning
    data2019, data2020 = dataCleaning(data2019, data2020)

    # DataVisualization
    dataVisualization(data2019, data2020)
    

# We run the main function on start
if __name__ == "__main__":
    main()

