import streamlit as st

def main_page():
    st.markdown("")

def DVF():
    st.markdown("")

def main():
    # Sidebar
    st.sidebar.markdown("# Choose a page 📚")

    # Main Page
    st.image("logo_efrei.png", use_column_width=True)
    st.markdown("# Data Visualization Project 📊")
    st.markdown("")
    st.markdown("")
    st.success("Go to the DVF exploration 📚 by clicking on the sidebar on the left")
    st.markdown("")
    st.write('*made by Louis Arbey.*')

    # It's freezing here
    st.snow()
    
if __name__ == "__main__":
    main()

