import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Stress Detection - Dr. Felix Beierle",
    page_icon="👋",
    #layout='wide'
)

st.title('Explore Data')

st.write('This page lets you explore the raw input (test) data of the sensors in the Empatica E4.')

st.write('`subject` refers to the subject of the study')
st.write('`label` indicates stress (1) or no stress (0)')
st.write('`session` refers to session of the recording, i.e., consecutive rows contain consecutive recordings of the experiment.')


st.write('#### ACC - accelerometer - 32 Hz')
st.write('`x`, `y`, and `z` are the sensor data readings from the accelerometer data sensor.')
df = pd.read_parquet('test-data/acc.parquet', engine='pyarrow')
st.dataframe(df)

st.write('#### BVP - blood volume pulse - 64 Hz')
st.write('`bvp` indicates the value from the BVP sensor.')
df = pd.read_parquet('test-data/bvp.parquet', engine='pyarrow')
st.dataframe(df)

st.write('#### EDA - electrodermal activity - 4 Hz')
st.write('`eda` indicates the value from the EDA sensor.')
df = pd.read_parquet('test-data/eda.parquet', engine='pyarrow')
st.dataframe(df)

st.write('#### TEMP - temperature - 4 Hz')
st.write('`temp` indicates the temperatur in Celsius recorded with the Empatica E4 wristband.')
df = pd.read_parquet('test-data/temp.parquet', engine='pyarrow')
st.dataframe(df)
