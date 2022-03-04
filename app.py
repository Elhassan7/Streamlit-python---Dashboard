
import streamlit as st
import pandas as pd

st.set_page_config(page_title= "Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout='wide')

df= pd.read_csv("supermarkt_sales.csv")

#-----------SideBar-------------
st.sidebar.header("Filtering by :")
city= st.sidebar.multiselect("Select The City :",     
                        options=df["City"].unique(),
                        default=["Yangon"] )

customer_type= st.sidebar.multiselect("Select type of customer :",     
                        options=df["Customer_type"].unique(),
                        default=df["Customer_type"].unique())

Gender= st.sidebar.multiselect("Select The Gender :",     
                        options=df["Gender"].unique(),
                        default=df["Gender"].unique())


df_city= df.query("City== @city & Customer_type==@customer_type & Gender==@Gender")

st.dataframe(df_city)
