import streamlit as st
import streamlit_shadcn_ui as ui
import requests
import warnings
import geocoder
import json
import pymysql
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
states_file_path = os.path.join(current_dir, '..', 'states.json')

warnings.filterwarnings('ignore')

with open(states_file_path, 'r') as file:
    data = json.load(file)
    data["page_state"] = ""
with open(states_file_path, 'w') as file:
    json.dump(data, file, indent=4)

st.set_page_config(initial_sidebar_state="collapsed",layout='wide', page_title='Kite - ATC Simulator', page_icon=':sun_small_cloud:')
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
st.title(" :sun_small_cloud: Weather Data")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

st.write("---")

st.subheader("Enter location type: ")

switch_value = ui.switch(default_checked=True, label="Detect my location", key="switch1")

if switch_value==True:
    g = geocoder.ip('me')
    input_value = st.text_input("Location Input",value= g.city,key="input1", disabled=True)

else:
    input_value = st.text_input("Location Input",placeholder="Enter city",key="input1", disabled=False)


def f():
    if input_value=="":
        st.error("Please enter a city")
    CITY = input_value
    url = st.secrets['BASE_URL'] + "appid=" + st.secrets["API_KEY"] + "&q=" + CITY + "&units=metric"
    response = requests.get(url).json()
    if response['cod']=='404':
        st.error("City not found")
    else:
        with open(states_file_path, 'r') as file:
            data = json.load(file)
            data["show_metrics"] = "True"
        with open(states_file_path, 'w') as file:
            json.dump(data, file, indent=4)

button = st.button("Submit", on_click=f, key='butt',type='primary')

with open(states_file_path, 'r') as file:
    data = json.load(file)
    if data["show_metrics"]=="True":
        CITY = input_value
        url = st.secrets['BASE_URL'] + "appid=" + st.secrets["API_KEY"] + "&q=" + CITY + "&units=metric"
        weather_data = requests.get(url).json()
        try:
            cols = st.columns(5)
            with cols[0]:
                ui.metric_card(title="Feels like", content=str(weather_data['main']['feels_like'])+"°C", description="max: "+str(weather_data['main']['temp_max'])+" | "+"min: "+str(weather_data['main']['temp_min']), key="card1")
            with cols[1]:
                ui.metric_card(title="Humidity", content=str(weather_data['main']['humidity'])+" g/m³",description="Per meter cube", key="card2")
            with cols[2]:
                ui.metric_card(title="Pressure", content=str(weather_data['main']['humidity'])+" Hg",description="Measure of pressure", key="card3")
            with cols[3]:
                ui.metric_card(title="Visibility", content=str(weather_data['visibility'])+" m",description="Distance of clear visibility", key="card4")
            with cols[4]:
                ui.metric_card(title="Wind Speed", content=str(weather_data['wind']['speed'])+" kmph",description="Degree: "+ str(weather_data['wind']['deg']), key="card5")
        except:
            pass

st.write("---")

st.subheader("Select airport: ")

connection = pymysql.connect(host=st.secrets['MYSQL_HOST'], user=st.secrets['MYSQL_ROOT'], password=st.secrets['MYSQL_PASSWORD'], database=st.secrets['MYSQL_DATABASE'])
cur = connection.cursor()

query = "SELECT * from airports;"
cur.execute(query)
records = pd.read_sql(query, connection)

connection.close()

airport_options = records["airport"].unique()
airport = st.selectbox("Select airport", options=airport_options)

region_name = records.loc[records['airport']==airport,'region_name'].values[0]

def f2():
    if region_name=="":
        st.error("Please select an airport")
    CITY = region_name
    url = st.secrets['BASE_URL'] + "appid=" + st.secrets["API_KEY"] + "&q=" + CITY + "&units=metric"
    response = requests.get(url).json()
    if response['cod']=='404':
        st.error("City not found")
    else:
        with open(states_file_path, 'r') as file:
            data = json.load(file)
            data["show_airport_weather_metrics"] = "True"
        with open(states_file_path, 'w') as file:
            json.dump(data, file, indent=4)

button2 = st.button("Submit", on_click=f2, key='butt2',type='primary')

with open(states_file_path, 'r') as file:
    data = json.load(file)
    if data["show_airport_weather_metrics"]=="True":
        CITY = region_name
        url = st.secrets['BASE_URL'] + "appid=" + st.secrets["API_KEY"] + "&q=" + CITY + "&units=metric"
        weather_data2 = requests.get(url).json()
        try:
            cols = st.columns(5)
            with cols[0]:
                ui.metric_card(title="Feels like", content=str(weather_data2['main']['feels_like'])+"°C", description="max: "+str(weather_data2['main']['temp_max'])+" | "+"min: "+str(weather_data2['main']['temp_min']), key="card11")
            with cols[1]:
                ui.metric_card(title="Humidity", content=str(weather_data2['main']['humidity'])+" g/m³",description="Per meter cube", key="card21")
            with cols[2]:
                ui.metric_card(title="Pressure", content=str(weather_data2['main']['humidity'])+" Hg",description="Measure of pressure", key="card31")
            with cols[3]:
                ui.metric_card(title="Visibility", content=str(weather_data2['visibility'])+" m",description="Distance of clear visibility", key="card41")
            with cols[4]:
                ui.metric_card(title="Wind Speed", content=str(weather_data2['wind']['speed'])+" kmph",description="Degree: "+ str(weather_data['wind']['deg']), key="card51")
        except:
            pass
