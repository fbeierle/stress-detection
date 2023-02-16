import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(
    page_title="Stress Detection - Dr. Felix Beierle",
    page_icon="👋",
    layout='wide'
)

col1, col2, col3, col4 = st.columns(4)

res = None
res_predict = None

# load data
df_acc = (pd.read_parquet('test-data/acc.parquet', engine='pyarrow')).head(30*32)[['x', 'y', 'z']].reset_index()
df_bvp = (pd.read_parquet('test-data/bvp.parquet', engine='pyarrow')).head(30*64)[['BVP']].reset_index()
df_eda = (pd.read_parquet('test-data/eda.parquet', engine='pyarrow')).head(30*4)[['EDA']].reset_index()
df_temp = (pd.read_parquet('test-data/temp.parquet', engine='pyarrow')).head(30*4)[['TEMP']].reset_index()

# prepare data for sending for preprocessing
acc_x = df_acc['x'].tolist()
acc_y = df_acc['y'].tolist()
acc_z = df_acc['z'].tolist()
bvp = df_bvp['BVP'].tolist()
eda = df_eda['EDA'].tolist()
temp = df_temp['TEMP'].tolist()
json_string = '{'+'\"acc_x\":{\"valuelist\": '+str(acc_x)+'},'
json_string += '\"acc_y\":{\"valuelist\": '+str(acc_y)+'},'
json_string += '\"acc_z\":{\"valuelist\": '+str(acc_z)+'},'
json_string += '\"bvp\":{\"valuelist\": '+str(bvp)+'},'
json_string += '\"eda\":{\"valuelist\": '+str(eda)+'},'
json_string += '\"temp\":{\"valuelist\": '+str(temp)+'}'
json_string += '}'
payload = json.loads(json_string)
payload_pp = ''


with col1:
    st.title('Raw Sensor Data')

    st.write('Below you can explore raw 30 seconds of sensor data needed for one prediction (user 3, label 1 (stress)).')

    st.write('#### ACC - accelerometer - 32 Hz')
    st.write('`x`, `y`, and `z` are the sensor data readings from the accelerometer data sensor.')
    st.dataframe(df_acc)

    st.write('#### BVP - blood volume pulse - 64 Hz')
    st.write('`bvp` indicates the value from the BVP sensor.')
    st.dataframe(df_bvp)

    st.write('#### EDA - electrodermal activity - 4 Hz')
    st.write('`eda` indicates the value from the EDA sensor.')
    st.dataframe(df_eda)

    st.write('#### TEMP - temperature - 4 Hz')
    st.write('`temp` indicates the temperature in Celsius recorded with the Empatica E4 wristband.')
    st.dataframe(df_temp)

with col2:
    st.title('Send data')

    st.write('''
            When you press the button, the data will be sent to the preprocessing module
            for preprocessing and then to the model for prediction.
            The output will be displayed on the right.
            ''')
    
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    if st.button('Send data', key='buttonpp01'):
        res = requests.post('http://preprocessing:8004/preprocess/', json=payload, headers=headers)
        valuelist_pp = res.content.decode()
        json_string_pp = '{\"valuelist\": '+str(valuelist_pp)+'}'
        #print(json_string_pp)
        payload_pp = json.loads(json_string_pp)
        res_predict = requests.post('http://modelserving:8002/predict/', json=payload_pp, headers=headers)

    st.write(payload)

with col3:
    st.title('Preprocessing Response')
    st.write('''
            This shows the response of the proprocessing module: the features needed as input for inference.
            ''')
    st.write('API: http://5.189.182.28:8004/docs#/default/preprocess_preprocess__post')

    if res:
        st.write(res)
        st.write(res.headers)
        st.write(valuelist_pp)

with col4:
    st.title('Model Response')
    st.write('''
            This shows the response of the model: 1 (stress) or 0 (no stress).
            ''')
    st.write('API: http://5.189.182.28:8002/docs#/default/get_prediction_predict__post')
    
    if res_predict:
        st.write(res_predict)
        st.write(res_predict.headers)
        st.write('## '+res_predict.content.decode())
