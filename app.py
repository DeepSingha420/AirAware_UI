import streamlit as st
import requests
from streamlit_javascript import st_javascript

st.title("AirAware")

# This script runs in the user's browser to find their public IP
# It uses a public API (ipify) to bypass local/proxy issues
js_code = 'await fetch("https://api.ipify.org?format=json").then(res => res.json())'
result = st_javascript(js_code)

if result:
    visitor_ip = result.get("ip")
    #st.write(f"Your Public IP is: **{visitor_ip}**")
else:
    st.write("Detecting IP...")

#visitor_ip = st.context.ip_address

#st.write(visitor_ip)

if not visitor_ip: visitor_ip = "8.8.8.8"

st.set_page_config(page_title="AirAware", page_icon="🌍")

API_URL = "https://air-aware-three.vercel.app/aqi"

st.title("Location-based AQI Service using FastAPI")

if st.button("Check My Local AQI"):
    st.warning(f"Detected IP: {visitor_ip}")
    with st.spinner("Fetching data from Vercel..."):
        try:
            if visitor_ip:
                response = requests.get(f"{API_URL}?ip={visitor_ip}")
            else:
                response = requests.get(API_URL)
            data = response.json()
            json_string = json.dumps(data, indent=4)

            if response.status_code == 200:
                # 3. Display the nested data you built
                loc = data["location"]
                aqi = data["aqi"]

                st.subheader(f"Location: {loc['city']}, {loc['country']}")
                
                # Big metric for AQI
                st.metric(label="AQI Value", value=aqi['value'], delta=aqi['category'], delta_color="inverse")

                st.success("Check / Download JSON:")
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button("Check", f"{API_URL}?ip={visitor_ip}")
                with col2:
                    st.download_button(
                        label="Download",
                        data=json_string,
                        file_name="data.json",
                        mime="application/json"
                    )
                
                # Show coordinates on a map
                st.map({"lat": [loc['lat']], "lon": [loc['lon']]})
                
                st.caption(f"Source: {data['source']} | IP: {data['ip']}")
            else:
                st.error("Backend returned an error.")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")
            st.error(visitor_ip)












