
from matplotlib.pyplot import figure
from numpy import average
import streamlit as st
import plotly.express as px
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


df_selection= df.query("City== @city & Customer_type==@customer_type & Gender==@Gender")



#---------------Main Page-------------------

st.title(":bar_chart:Sales Dashboard")
st.markdown("##")

#--------TOP KPI's ------------
total_sales= int(df_selection["Total"].sum())
average_rating= round(df_selection["Rating"].mean(), 1)
star_rating=" :star:" * int(round(average_rating,0))

average_sales_trans= round(df_selection["Total"].mean(), 2)

left_column, midle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales : ")
    st.subheader(f"US $ {total_sales:,}")

with midle_column:
    st.subheader("Average Rating : ")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales per transaction : ")
    st.subheader(f"US $ {average_sales_trans}")

st.markdown("---")

#------ Sale by product line [line Chart] -------------
sales_by_product= (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_product_sales= px.bar(
    sales_by_product,
    x= "Total",
    y= sales_by_product.index,
    orientation= 'h',
    title= "<b>Sales by Product Line</b>",
    color_discrete_sequence= ["#0083B8"] * len(sales_by_product),
    template= "plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales)