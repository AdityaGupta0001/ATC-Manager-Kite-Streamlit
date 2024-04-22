import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
from streamlit_lottie import st_lottie
import pymysql
import string
from components import lotto_animation
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import time
import json

try:
    connection = pymysql.connect(host="localhost", user=st.secrets['MYSQL_ROOT'], password=st.secrets['MYSQL_PASSWORD'], database="Kite")
    with open('commands.sql', 'r') as file:
        sql_commands = file.read()
    commands = sql_commands.split(';')
    with connection.cursor() as cursor:
        for command in commands:
            cursor.execute(command)
    connection.commit()
    connection.close()
except:
    pass

with open("states.json", 'r') as file:
    data = json.load(file)

if data['page_state'] in ['airports','flightStatus','weather']:
    switch_page(data['page_state'])
else:
    if data['logged_in'] == "False":
        st.set_page_config(initial_sidebar_state="collapsed",layout='wide', page_title='Kite - ATC Simulator', page_icon=':kite:')
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

        @st.cache_resource
        def loading():
            airplane_anmation = lotto_animation.load_lottieurl("https://lottie.host/fa953ca5-223b-4f9e-8c2d-428db260d339/BRvqEffGFA.json")
            weather_animation = lotto_animation.load_lottieurl("https://lottie.host/2535f651-8531-417a-8af7-93cd47e14978/gbboOVNlBI.json")
            flight_status_animation = lotto_animation.load_lottieurl("https://lottie.host/179c4a3d-7d0b-4cae-8605-d9526aef0a82/ZWHlBF1U6H.json")
            return [airplane_anmation,weather_animation,flight_status_animation]

        # st.write("##")
        st.title("Kite :kite:")

        def stream_data():
            text = "Navigate the Skies with Kite: Your Flight Control Companion!"
            for word in text.split(" "):
                for i in word:
                    yield i
                    time.sleep(0.02)
                yield " "
                time.sleep(0.02)


        st.write_stream(stream_data)

        st.write("---")

        gifs = loading()
        col1,col2=st.columns(2)

        with col1:
            st_lottie(gifs[2],width=512,height=512)
            
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            
            st.markdown("<h1 style='text-align: left; color: white;'>Discover Our Expansive Airport Database!</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: left; color: white;'>Unlock a World of Airport Data! With a comprehensive database featuring 8000+ airports worldwide, Kite provides instant access to detailed airport information. Explore airports from every corner of the globe with ease!</p>", unsafe_allow_html=True)

            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")

            st_lottie(gifs[1],width=512,height=512)

        with col2:

            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")

            st.markdown("<h1 style='text-align: right; color: white;'>Track Your Flight in Real-Time!</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: right; color: white;'>Enter your flight ID and gain instant access to live updates on your flight's status. Whether it's departure, arrival, or any delays along the way, Kite keeps you informed with real-time flight tracking, ensuring a seamless travel experience from start to finish.</p>", unsafe_allow_html=True)

            st.write("##")
            st.write("##")
            st_lottie(gifs[0],width=720,height=720)

            st.markdown("<h1 style='text-align: right; color: white;'>Experience Real-Time Weather Updates!</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: right; color: white;'>With our dynamic real-time weather feature, stay informed about current weather conditions for any airport worldwide. From temperature and humidity to wind speed and precipitation, Kite provides up-to-date weather information to ensure you're always prepared for your journey.</p>", unsafe_allow_html=True)

            
        st.write("---")

        with st.container():
            selected = option_menu(
                menu_title=None,
                options=['Login','Sign Up'],
                icons = ['person-circle','person-add'],
                orientation='horizontal',
                default_index=0
            )

        if selected == 'Login':
            with st.container():
                col1,col2,col3 = st.columns(3)
                with col2:
                    def f(email_,password_):
                        try:
                            connection = pymysql.connect(host="localhost", user=st.secrets['MYSQL_ROOT'], password=st.secrets['MYSQL_PASSWORD'], database="Kite")
                            cur = connection.cursor()
                            query = f'SELECT password from users where email = "{email_}"'
                            cur.execute(query)
                            records = cur.fetchone()
                            if email_ == "" or password_ == "":
                                st.error("email & password required")
                            else:
                                if records:
                                    if records[0]==password_:
                                        with st.spinner('Please wait...'):
                                            time.sleep(4)
                                        st.success("Logged In")
                                        st.balloons()
                                        with open("states.json", 'r') as file:
                                            data = json.load(file)
                                            data["logged_in"] = "True"
                                        with open("states.json", 'w') as file:
                                            json.dump(data, file, indent=4)
                                        time.sleep(4)
                                        st.rerun()
                                    else: 
                                        st.error("Incorrect password entered")
                                else:
                                    st.error("User does not exist")

                            connection.close()
                        except Exception as e:
                            print(e)
                            st.error("Something wrong happened")

                    st.write("##")
                    with st.form("login_form"):
                        email = ui.input(default_value="", type='text', placeholder="email", key="input1")
                        password = ui.input(default_value="", type='text', placeholder="password", key="input2")
                        login_submitted = st.form_submit_button("Submit",use_container_width=True, type='primary',on_click=f(email,password))

        def valid_email(email):
            global mailcheck
            mailcheck=False
            validity_ctr=0
            domains=[".com",".co",".in",".co.in",".org",".net",".info"]
            attherate="@"
            email=str(email).lower()
            if attherate in email:
                validity_ctr+=1
            for i in domains:
                if i in email:
                    domain_location=i
                    validity_ctr+=1
                    if email.index(domain_location)==len(email)-len(domain_location):
                        validity_ctr+=1
                    break
            if validity_ctr==3:
                    mailcheck=True
            return mailcheck

        def valid_password(password):
            global passcheck
            passcheck=False
            specialChars=string.punctuation
            lower, upper, specialCount, digitCount = 0, 0, 0, 0
            if (len(password) >= 8):
                for i in password:
                    if (i.islower()):
                        lower+=1            
                    if (i.isupper()):
                        upper+=1            
                    if (i.isdigit()):
                        digitCount+=1            
                    if(i in specialChars):
                        specialCount+=1           
                if (lower>=1 and upper>=1 and specialCount>=1 and digitCount>=1 and lower+specialCount+upper+digitCount==len(password)):
                    passcheck=True
            return passcheck

        def existinguser(email_):
            connection = pymysql.connect(host="localhost", user=st.secrets['MYSQL_ROOT'], password=st.secrets['MYSQL_PASSWORD'], database="Kite")
            cur = connection.cursor()
            query = f'SELECT * from users where email = "{email_}"'
            cur.execute(query)
            records = cur.fetchall()
            connection.close()
            if len(records)>0:
                return True
            return False

        if selected == 'Sign Up':
            with st.container():
                col1,col2,col3 = st.columns(3)
                with col2:
                    def f2(email_,password_,username_):
                        global valid_email,valid_password,existinguser

                        if email_ == "" or password_ == "" or username_ == "":
                            st.error("email, password & username required")
                        else:
                            if valid_email(email_)==False:
                                st.error("Enter a valid email")
                            elif valid_password(password_)==False:
                                st.error("Enter a strong password")
                            else:
                                if existinguser(email_)==True:
                                    st.error("User already exists")
                                else:
                                    try:
                                        connection = pymysql.connect(host="localhost", user=st.secrets['MYSQL_ROOT'], password=st.secrets['MYSQL_PASSWORD'], database="Kite")
                                        cur = connection.cursor()
                                        query = f'INSERT INTO USERS(username,email,password) VALUES("{username_}","{email_}","{password_}")'
                                        cur.execute(query)
                                        connection.commit()
                                        connection.close()
                                        st.success("Signed up successfully")
                                        st.balloons()
                                        st.success("Please login with your credentials")
                                    except:
                                        st.error("Something wrong happened")
                    st.write("##")

                    with st.form("signup_form"):
                        username = ui.input(default_value="", type='text', placeholder="username", key="input0")
                        email = ui.input(default_value="", type='text', placeholder="email", key="input1")
                        password = ui.input(default_value="", type='text', placeholder="password", key="input2")
                        signup_submitted = st.form_submit_button("Submit",use_container_width=True, type='primary',on_click=f2(email,password,username))
        st.write("---")
        sub_col1,sub_col2,sub_col3,sub_col4 = st.columns(4)
        with sub_col1:
            st.markdown("<h2 style='text-align: center; color: white; padding-top: 50px'>Kite</h2>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: white; padding-top: 2px'>ATC Manager Team</h4>", unsafe_allow_html=True)
        with sub_col2:
            sub_col2_left,sub_col2_mid,sub_col2_right = st.columns(3)
            with sub_col2_left:
                st.markdown("""
                    <div style="border-left: 2px solid #3d4044; height: 215px;"></div>
                """, unsafe_allow_html=True)
            with sub_col2_mid:
                with stylable_container(
                    key="user_image",css_styles="""div[data-testid="stImage"] > img {
                        border-radius: 50%;
                    }"""
                ):
                    st.image("assets/AdityaGupta.jpg",clamp=False)
                st.markdown("<h6 style='text-align: center; color: white;'>Aditya Gupta</h6>", unsafe_allow_html=True)
                st.link_button(label="GitHub", url="https://github.com/AdityaGupta0001", use_container_width=True)
            
        with sub_col3:
            sub_col3_left,sub_col3_mid,sub_col3_right = st.columns(3)
            with sub_col3_left:
                st.markdown("""
                    <div style="border-left: 2px solid #3d4044; height: 215px;"></div>
                """, unsafe_allow_html=True)
            with sub_col3_mid:
                with stylable_container(
                    key="user_image",css_styles="""div[data-testid="stImage"] > img {
                        border-radius: 50%;
                    }"""
                ):
                    st.image("assets/ManayaPachpor.jpg",clamp=False)
                st.markdown("<h6 style='text-align: center; color: white;'>Manaya Pachpor</h6>", unsafe_allow_html=True)
                st.link_button(label="GitHub", url="https://github.com/Manaya20", use_container_width=True)
            
            with sub_col4:
                sub_col4_left,sub_col4_mid,sub_col4_right = st.columns(3)
                with sub_col4_left:
                    st.markdown("""
                        <div style="border-left: 2px solid #3d4044; height: 215px;"></div>
                    """, unsafe_allow_html=True)
                with sub_col4_mid:
                    with stylable_container(
                        key="user_image",css_styles="""div[data-testid="stImage"] > img {
                            border-radius: 50%;
                        }"""
                    ):
                        st.image("assets/YamikaChauhan.jpg",clamp=False)
                    st.markdown("<h6 style='text-align: center; color: white;'>Yamika Chauhan</h6>", unsafe_allow_html=True)
                    st.link_button(label="GitHub", url="https://github.com/yambamfam", use_container_width=True)
        st.write("---")
    else:
        st.set_page_config(initial_sidebar_state="collapsed",layout='wide', page_title='Kite - ATC Simulator', page_icon=':kite:')
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
        def f():
            with open("states.json", 'r') as file:
                data = json.load(file)
                data["logged_in"] = "False"
            with open("states.json", 'w') as file:
                json.dump(data, file, indent=4)
            st.rerun()
        
        col1,col2,col3 = st.columns([0.84,0.08,0.08])
        with col1:
            st.title("Kite :kite: - Dashboard")
        with col2:
            st.markdown('<div style="padding-top: 25px;"></div>', unsafe_allow_html=True)
            st.link_button(label="Github", url="https://github.com/AdityaGupta0001",type='secondary',use_container_width=True)
        with col3:
            st.markdown('<div style="padding-top: 25px;"></div>', unsafe_allow_html=True)
            st.button(label="Logout", on_click=f,type='secondary')

        st.write("---")
        st.markdown("<h2 style='text-align: left; color: white;'>Introducing Kite Dashboard!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: left; color: white;'>With access to over 8000 airports worldwide, real-time weather updates, and live flight tracking, planning your journey has never been easier. Explore detailed airport information, stay informed with up-to-the-minute weather forecasts, and track your flight's status effortlessly—all in one convenient platform.</p>", unsafe_allow_html=True)
        st.write("---")

        @st.cache_resource
        def dashboard_loading():
            airport_anmation = lotto_animation.load_lottieurl("https://lottie.host/99eeafd6-8ca5-49ee-91c4-6c99a38a48ac/ISSKtXmlGI.json")
            weather_forecast_animation = lotto_animation.load_lottieurl("https://lottie.host/4460bd6a-cce7-40e3-ab1d-e9170d215ac7/Klxsn2lb6g.json")
            flight_animation = lotto_animation.load_lottieurl("https://lottie.host/7c97e1aa-a3f1-41f6-9d41-dea6f8ca45c1/H615023gfL.json")
            return [airport_anmation,weather_forecast_animation,flight_animation]
        animations = dashboard_loading()

        feat_col1,feat_col2,feat_col3 = st.columns(3)
        with feat_col1:
            with st.container(border=True):
                def see_airports():
                    global page
                    time.sleep(0.5)
                    with open("states.json", 'r') as file:
                        data = json.load(file)
                        data["page_state"] = "airports"
                    with open("states.json", 'w') as file:
                        json.dump(data, file, indent=4)
                st.write("##")
                st.write("##")
                st.write("##")
                st.write("##")
                st.write("##")
                st_lottie(animations[0])
                st.write("##")
                st.markdown("<h2 style='text-align: left; color: white;'>Airports</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: left; color: white;'>With a comprehensive database featuring 8000+ airports worldwide, Kite provides instant access to detailed airport information. Explore airports from every corner of the globe with ease!</p>", unsafe_allow_html=True)
                st.button(label="Explore",on_click=see_airports,key="airports",use_container_width=True,type='primary')

        with feat_col2:
            with st.container(border=True):
                def see_weather():
                    global page
                    time.sleep(0.5)
                    with open("states.json", 'r') as file:
                        data = json.load(file)
                        data["page_state"] = "weather"
                    with open("states.json", 'w') as file:
                        json.dump(data, file, indent=4)
                st.write("##")
                st_lottie(animations[1],height=407)
                st.markdown("<h2 style='text-align: left; color: white;'>Weather</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: left; color: white;'>From temperature and humidity to wind speed and precipitation, explore real-time up-to-date weather information for your airport or location to ensure you're always prepared for your journey!</p>", unsafe_allow_html=True)
                st.button(label="Explore",on_click=see_weather,key="weather",use_container_width=True,type='primary')

        with feat_col3:
            with st.container(border=True):
                def see_flight_status():
                    global page
                    time.sleep(0.5)
                    with open("states.json", 'r') as file:
                        data = json.load(file)
                        data["page_state"] = "flightStatus"
                    with open("states.json", 'w') as file:
                        json.dump(data, file, indent=4)
                st.write("##")
                st_lottie(animations[2],height=407)
                st.markdown("<h2 style='text-align: left; color: white;'>Flight Status</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: left; color: white;'>Kite keeps you informed with real-time flight tracking, ensuring a seamless travel experience from start to finish. Just enter your flight ID and get up-to-date updates about your flight in real-time!</p>", unsafe_allow_html=True)
                st.button(label="Explore",on_click=see_flight_status,key="status",use_container_width=True,type='primary')