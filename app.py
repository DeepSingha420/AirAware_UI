import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval


visitor_ip = streamlit_js_eval(
    js_expressions='await fetch("https://api.ipify.org").then(res => res.json()).then(data => data.ip)',
    key = 'IP_DETECTOR'
)

st.set_page_config(page_title="AirAware", page_icon="🌍")

API_URL = "https://air-aware-three.vercel.app/aqi"

st.title("🌍 Real-time Air Quality")

if st.button("Check My Local AQI"):
    st.warning(visitor_ip)
    with st.spinner("Fetching data from Vercel..."):
        try:
            if visitor_ip:
                response = requests.get(f"{API_URL}?ip={visitor_ip}")
            else:
                response = requests.get(API_URL)
            data = response.json()

            if response.status_code == 200:
                # 3. Display the nested data you built
                loc = data["location"]
                aqi = data["aqi"]

                st.subheader(f"Location: {loc['city']}, {loc['country']}")
                
                # Big metric for AQI
                st.metric(label="US AQI Value", value=aqi['value'], delta=aqi['category'], delta_color="inverse")
                
                # Show coordinates on a map
                st.map({"lat": [loc['lat']], "lon": [loc['lon']]})
                
                st.caption(f"Source: {data['source']} | IP: {data['ip']}")
            else:
                st.error("Backend returned an error.")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")
            st.error(visitor_ip)





