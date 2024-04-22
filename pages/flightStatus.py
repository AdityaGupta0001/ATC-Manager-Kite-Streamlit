import datetime
from pyflightdata import FlightData
import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import json
import folium
import streamlit_folium
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
states_file_path = os.path.join(current_dir, '..', 'states.json')

with open(states_file_path, 'r') as file:
    data = json.load(file)
    data["page_state"] = ""
with open(states_file_path, 'w') as file:
    json.dump(data, file, indent=4)

st.set_page_config(initial_sidebar_state="collapsed",layout='wide', page_title='Kite - ATC Simulator', page_icon=':bar_chart:')
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
st.title(" :bar_chart: Flight Status")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

st.write("---")

global all_flight_data

input_value = st.text_input("Enter flight ID: ",key="input1", disabled=False)

if input_value=="":
    st.error("Please enter a flight ID")
    with open(states_file_path, 'r') as file:
                    data = json.load(file)
                    data["show_flight_status"] = "False"
    with open(states_file_path, 'w') as file:
        json.dump(data, file, indent=4)
else:
    current_date = str(datetime.date.today()).replace("-","")
    flight_dates = []
    try:
        f=FlightData()
        f.login(st.secrets['FLIGHT_DATA_API_USER'],st.secrets['FLIGHT_DATA_API_PASSWORD'])
        all_flight_data = f.get_all_available_history_by_flight_number(input_value)
        for i in all_flight_data:
            if i['time']['scheduled']['departure_date']>=current_date:
                flight_dates.append(i['time']['scheduled']['departure_date'])

        months = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        suffix = {"1":"st","2":"nd","3":"rd","11":"th", "12":"th", "13":"th"}
        formatted_flight_dates = []
        for i in flight_dates:
            month=i[4:6]
            day=i[6::]
            suf=i[-1]
            if suf in suffix:
                date_suffix = suffix[suf]
            if day in suffix:
                date_suffix = suffix[day]
            elif suf in suffix and day not in suffix:
                date_suffix = suffix[suf]
            else:
                date_suffix = "th"
            formatted_flight_dates.append(day+date_suffix+" "+months[month])

        if formatted_flight_dates==[]:
            date = st.selectbox("Select departure date", options=[])
            with open(states_file_path, 'r') as file:
                    data = json.load(file)
                    data["show_flight_status"] = "False"
            with open(states_file_path, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            date = st.selectbox("Select departure date", options=formatted_flight_dates)
    except:
        st.error("Please enter a valid flight ID")
def f():
    if input_value=="":
        st.error("Please enter a flight ID")
    global all_flight_data,filtered_flight
    flightDate = flight_dates[formatted_flight_dates.index(date)]
    for i in all_flight_data:
        if flightDate == i['time']['scheduled']['departure_date']:
            filtered_flight = i
            break
    
    with open("temp_status.json", 'w') as file:
        json.dump(filtered_flight, file, indent=4)

    with open(states_file_path, 'r') as file:
            data = json.load(file)
            data["show_flight_status"] = "True"
    with open(states_file_path, 'w') as file:
        json.dump(data, file, indent=4)

button = st.button("Submit", on_click=f, key='butt',type='primary')
st.write("---")

with open(states_file_path, 'r') as file:
    data = json.load(file)
    if data["show_flight_status"]=="True":
        with open("temp_status.json", 'r') as file:
            flight_data = json.load(file)
        def replaceNone(str):
            if str=="None":
                return "-"
            else:
                 return str
        
        airline_iata = flight_data['airline']['code']['iata']
        airline_icao = flight_data['airline']['code']['icao']
        airline_name = flight_data['airline']['name']

        dest_airport_iata = flight_data['airport']['destination']['code']['iata']
        dest_airport_icao = flight_data['airport']['destination']['code']['icao']
        dest_airport_name = flight_data['airport']['destination']['name']
        dest_airport_location = flight_data['airport']['destination']['position']['region']['city']+","+flight_data['airport']['destination']['position']['country']['name']
        dest_airport_lat = flight_data['airport']['destination']['position']['latitude']
        dest_airport_long = flight_data['airport']['destination']['position']['longitude']

        org_airport_iata = flight_data['airport']['origin']['code']['iata']
        org_airport_icao = flight_data['airport']['origin']['code']['icao']
        org_airport_name = flight_data['airport']['origin']['name']
        org_airport_location = flight_data['airport']['origin']['position']['region']['city']+","+flight_data['airport']['origin']['position']['country']['name']
        org_airport_lat = flight_data['airport']['destination']['position']['latitude']
        org_airport_long = flight_data['airport']['destination']['position']['longitude']

        estimated_arrival_time = flight_data['time']['estimated']['arrival']
        estimated_departure_time = flight_data['time']['estimated']['departure']
        scheduled_arrival_date = flight_data['time']['scheduled']['arrival_date']
        scheduled_arrival_time = flight_data['time']['scheduled']['arrival_time']
        scheduled_departure_date = flight_data['time']['scheduled']['departure_date']
        scheduled_departure_time = flight_data['time']['scheduled']['departure_time']
    
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Airline")
            airline_data_ = [
                {"Category": "Airline IATA Code", "Status": airline_iata},
                {"Category": "Airline ICAO Code", "Status": airline_icao},
                {"Category": "Airline Name", "Status": airline_name},
            ]

            airline_data = pd.DataFrame(airline_data_)
            ui.table(data=airline_data)

            st.write("##")

            st.subheader("Origin Airport")
            origin_airport_data_ = [
                {"Category": "IATA Code", "Status": org_airport_iata},
                {"Category": "ICAO Code", "Status": org_airport_icao},
                {"Category": "Aiport Name", "Status": org_airport_name},
                {"Category": "Aiport Location", "Status": org_airport_location},
            ]

            origin_airport_data = pd.DataFrame(origin_airport_data_)
            ui.table(data=origin_airport_data)

            st.write("##")

            st.subheader("Destination Airport")
            dest_airport_data_ = [
                {"Category": "IATA Code", "Status": dest_airport_iata},
                {"Category": "ICAO Code", "Status": dest_airport_icao},
                {"Category": "Aiport Name", "Status": dest_airport_name},
                {"Category": "Aiport Location", "Status": dest_airport_location},
            ]

            dest_airport_data = pd.DataFrame(dest_airport_data_)
            ui.table(data=dest_airport_data)

            st.write("##")

            st.subheader("Timings")
            timings_data_ = [
                {"Category": "Scheduled Departure Date", "Status": scheduled_departure_date[6::]+"/"+scheduled_departure_date[4:6]+"/"+scheduled_departure_date[0:4]},
                {"Category": "Scheduled Departure Time", "Status": scheduled_departure_time+" hrs"},
                {"Category": "Scheduled Arrival Date", "Status": scheduled_arrival_date[6::]+"/"+scheduled_arrival_date[4:6]+"/"+scheduled_arrival_date[0:4]},
                {"Category": "Scheduled Arrival Time", "Status": scheduled_arrival_time+" hrs"},
                {"Category": "Estimated Departure Time", "Status": replaceNone(estimated_departure_time)+" hrs"},
                {"Category": "Estimated Arrival Time", "Status": replaceNone(estimated_arrival_time)+" hrs"},
            ]

            timings_data = pd.DataFrame(timings_data_)
            ui.table(data=timings_data)

            st.write("##")

        with cols[1]:
            with st.container():
                st.write("##")
                
                if org_airport_lat is None or org_airport_long is None:
                    print("Error: Missing latitude or longitude for the origin airport.")
                    exit()

                if dest_airport_lat is None or dest_airport_long is None:
                    print("Error: Missing latitude or longitude for the destination airport.")
                    exit()

                # Create map with the location of the first airport
                center_lat = (org_airport_lat + dest_airport_lat) / 2
                center_long = (org_airport_long + dest_airport_long) / 2
                m = folium.Map(location=[center_lat, center_long], zoom_start=4, lang='en')
                
                fg = folium.FeatureGroup()
                # Add markers for both origin and destination airports
                folium.Marker([org_airport_lat, org_airport_long], popup=org_airport_name, tooltip=org_airport_name).add_to(fg)
                folium.Marker([dest_airport_lat, dest_airport_long], popup=dest_airport_name, tooltip=dest_airport_name).add_to(fg)

                m.add_child(fg)
                folium.TileLayer('openstreetmap').add_to(m)
                
                st_data = streamlit_folium.st_folium(m,width=700,height=1150)