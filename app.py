
import streamlit as st
import pandas as pd

st.set_page_config(page_title= "Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout='wide')

df= pd.read_csv("supermarkt_sales.csv")
st.dataframe(df)

#-----------SideBar-------------
st.sidebar.header("Filtering by :")
city= st.sidebar.multiselect("Select The City :",     
                        options=df["City"].unique(),
                        default=["Yangon"] )

customer_type= st.sidebar.multiselect("Select The City :",     
                        options=df["Customer_type"].unique(),
                        default=df["Customer_type"].unique())
