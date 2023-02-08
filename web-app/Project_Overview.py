import streamlit as st
from PIL import Image
import json
import requests

st.set_page_config(
    page_title="Stress Recognition - Dr. Felix Beierle",
    page_icon="👋",
    #layout='wide'
)

st.title('Stress Recognition')

col1, col2 = st.columns(2)

with col1:

    st.write('### Problem')
    st.write('* Stress contributes to bad health and bad work performance')
    st.write('* Recognizing stress immediately can help implement countermeasures')
    st.write('### Solution')
    st.write('* Automatically recognize stress from wristband sensor data')


    st.write('Code is here: https://github.com/fbeierle/stress-recognition')

with col2:
    img_stress = Image.open('images/stress.png')
    st.image(img_stress,
        width=200)

    img_wristband = Image.open('images/wristband.png')
    st.image(img_wristband,
        width=200)
