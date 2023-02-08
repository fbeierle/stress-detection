import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Stress Recognition - Dr. Felix Beierle",
    page_icon="👋",
    layout='wide'
)

st.title('Machine Learning Pipeline Infrastructure')

img_infra = Image.open('images/stress-recognition-infrastructure.png')

st.image(img_infra,
    width=850)
