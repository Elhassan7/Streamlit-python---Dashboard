
from matplotlib.pyplot import figure
from numpy import NaN, average
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title= "Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout='wide')

@st.cache
def get_data_from_csv():
    df= pd.read_csv("supermarkt_sales.csv")

    #------- Add hour's to dataframe ------------------
    df["hour"]= pd.to_datetime(df["Time"], format="%H:%M").dt.hour

    return df

df= get_data_from_csv()

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
if not df_selection.empty:
    total_sales= int(df_selection["Total"].sum())
    average_rating= round(df_selection["Rating"].mean(), 1)
    star_rating=" :star:" * int(round(average_rating,0))
    average_sales_trans= round(df_selection["Total"].mean(), 2)

else: 
    total_sales=0
    average_rating= 0
    star_rating=" :star:" * 1
    average_sales_trans= 0


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


# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

import plotly.graph_objects as go


fig_hourly_sales.add_trace(
    go.Scatter(
        x=sales_by_hour.index,
        y=sales_by_hour.Total,
        mode="lines",
        line=go.scatter.Line(color="#e3a812"),
        showlegend=False)
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#-------------------------
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
