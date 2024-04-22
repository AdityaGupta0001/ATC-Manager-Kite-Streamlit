import streamlit as st
import plotly.express as px
import json
import pandas as pd
import warnings
import pymysql
import streamlit_shadcn_ui as ui
import os

warnings.filterwarnings('ignore')

current_dir = os.path.dirname(os.path.abspath(__file__))
states_file_path = os.path.join(current_dir, '..', 'states.json')

st.set_page_config(initial_sidebar_state="collapsed",layout='wide', page_title='Kite - ATC Simulator', page_icon=':airplane_departure:')
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

with open(states_file_path, 'r') as file:
    data = json.load(file)
    data["page_state"] = ""
with open(states_file_path, 'w') as file:
    json.dump(data, file, indent=4)

st.title(" :airplane_departure: Airport Data")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

connection = pymysql.connect(host="localhost", user=st.secrets['MYSQL_ROOT'], password=st.secrets['MYSQL_PASSWORD'], database="Kite")
cur = connection.cursor()

query = "SELECT airports.*, countries.* FROM airports JOIN countries ON airports.country_code = countries.code;"
cur.execute(query)
records = pd.read_sql(query, connection)

connection.close()

st.write("Choose your filter:")

st.write("---")

country_code_options = records["country_code"].unique()
region_name_options = records["region_name"].unique()
iata_options = records["iata"].unique()
icao_options = records["icao"].unique()

country_code = st.multiselect("Select Country", options=country_code_options)
region_name = st.multiselect("Select Region", options=region_name_options)
iata = st.multiselect("Select IATA Code", options=iata_options)
icao = st.multiselect("Select ICAO Code", options=icao_options)

st.write("---")

filtered_data = records.copy()
if country_code:
    filtered_data = filtered_data[filtered_data['country_code'].isin(country_code)]
if region_name:
    filtered_data = filtered_data[filtered_data['region_name'].isin(region_name)]
if iata:
    filtered_data = filtered_data[filtered_data['iata'].isin(iata)]
if icao:
    filtered_data = filtered_data[filtered_data['icao'].isin(icao)]


with st.expander("Airports"):
    showData = st.multiselect("Table Data   Filter: ", filtered_data.columns, default=['country_code','region_name','iata','icao','airport','latitude','longitude'])
    ui.table(data=filtered_data[showData],maxHeight=400)
