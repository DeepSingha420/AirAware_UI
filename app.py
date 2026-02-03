import streamlit as st
import requests

# 1. Page Config
st.set_page_config(page_title="AirAware", page_icon="🌍")

# 2. Your Vercel URL
API_URL = "https://air-aware-three.vercel.app/aqi"

st.title("🌍 Real-time Air Quality")

if st.button("Check My Local AQI"):
    with st.spinner("Fetching data from Vercel..."):
        try:
            # We call your Vercel backend
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
