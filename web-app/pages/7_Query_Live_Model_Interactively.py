import streamlit as st
import pandas as pd
import requests
import json

#import logging
#logging.basicConfig(level=logging.DEBUG)

st.set_page_config(
    page_title="Stress Detection - Dr. Felix Beierle",
    page_icon="👋",
    layout='wide'
)

col1, col2 = st.columns(2)

res = None

with col1:
    st.title('Query Live Model')

    st.write('You can query the model interactively here. Note that the timestamps start at unix time 0 instead of the real time of recording.')

    df_ns = pd.read_parquet('test-data/test-data-nostress.parquet', engine='pyarrow')
    st.write('## Test data - Ground truth: no stress', df_ns)
    selected_indices_ns = st.multiselect('Select rows:', df_ns.index, key='multiselect_nostress')
    selected_rows_ns = df_ns.loc[selected_indices_ns]
    st.write('#### Selected Rows', selected_rows_ns)
    st.write('Only the first row will be send to the model')

    if not selected_rows_ns.empty:
        valuelist = selected_rows_ns.values[0].tolist()
        json_string = '{\"valuelist\": '+str(valuelist)+'}'
        print(json_string)
        payload = json.loads(json_string)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        if st.button('Send Request to model', key='button01'):
            res = requests.post('http://modelserving:8002/predict/', json=payload, headers=headers)

    df_s = pd.read_parquet('test-data/test-data-stress.parquet', engine='pyarrow')
    st.write('## Test data - Ground truth: stress', df_s)
    selected_indices_s = st.multiselect('Select rows:', df_s.index, key='multiselect_stress')
    selected_rows_s = df_s.loc[selected_indices_s]
    st.write('#### Selected Rows', selected_rows_s)
    st.write('Only the first row will be send to the model')

    if not selected_rows_s.empty:
        valuelist = selected_rows_s.values[0].tolist()
        json_string = '{\"valuelist\": '+str(valuelist)+'}'
        payload = json.loads(json_string)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        if st.button('Send Request to model', key='button02'):
            res = requests.post('http://modelserving:8002/predict/', json=payload, headers=headers)

with col2:
    st.title('Model Response')
    st.write('''
            This shows the response of the model: 1 (stress) or 0 (no stress).
            ''')
    st.write('API: http://5.189.182.28:8002/docs#/default/get_prediction_predict__post')

    if res:
        st.write(res)
        st.write(res.headers)
        st.write('## '+res.content.decode())
        