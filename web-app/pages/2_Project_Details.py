import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Stress Recognition - Dr. Felix Beierle",
    page_icon="👋",
    #layout='wide'
)

st.title('Project Details')

#col1, col2 = st.columns(2)

#with col1:

st.write('### The WESAD Dataset')
st.write('* The WESAD dataset contains sensor data for stress and affect detection, recorded in a lab setting.')
st.write('* In this project, we are using only the sensor data from the wristband, and focus on stress detection.')
st.write('* There are data about 15 participants in the dataset.')

st.write('Reference:')
st.write('Philip Schmidt, Attila Reiss, Robert Duerichen, Claus Marberger and Kristof Van Laerhoven. 2018. Introducing WESAD, a multimodal dataset for Wearable Stress and Affect Detection. In 2018 International Conference on Multimodal Interaction (ICMI 18). ACM, New York, NY, USA.')
st.write('https://ubicomp.eti.uni-siegen.de/home/datasets/icmi18/')

#Details:
#data set; link

st.write('### The Device: Empatica E4')

st.write('Sensors:')
st.write('* ACC - Accelerometer - 32 Hz')
st.write('* BVP - Blood volume pulse - 64 Hz')
st.write('* EDA - Electrodermal activity - 4 Hz')
st.write('* TEMP - Temperature - 4 Hz')


img_empatica = Image.open('images/EmpaticaE4.jpg')
st.image(img_empatica,
    caption='Empatica E4 wristband. Source: https://www.empatica.com/assets/images/e4/2/e4_image_divider_pc-lg-xhdpi.jpg',
    width=550)