import streamlit as st
import pandas as pd
import requests
import datetime
import folium
from streamlit_folium import folium_static


st.set_page_config(
    page_title="DIViz"
    #page_icon="👋",
)

st.write("# Welcome to DIViz!")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This App will help you visualize Divvy's data as well as weather historical data

    **👈 Select the category from the sidebar**


    """
)
