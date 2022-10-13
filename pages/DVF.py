import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import time
from collections import Counter

# We import the py file who contains the data load functions
from data_load import *

# We import the py file who contains the data cleaning functions
from data_clean import *

# We import the py file who contains the data visualization functions
from data_visualization import *

def main_page():
    st.markdown("")

def DVF():
    st.markdown("")

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

