from fastapi import FastAPI, Query, HTTPException, Response
import uvicorn
from pydantic import BaseModel
import numpy as np
import pandas as pd
import flirt

app = FastAPI()

class Values(BaseModel):
    valuelist: list = []

@app.post("/preprocess/", response_model=list, status_code=200)
def preprocess(acc_x: Values, acc_y: Values, acc_z: Values, bvp: Values, eda: Values, temp: Values) -> list:
    '''
    Preprocesses data for querying the model.
    '''

    preprocessing_results = preprocess_internal(acc_x.valuelist, acc_y.valuelist, acc_z.valuelist,
                                        bvp.valuelist, eda.valuelist, temp.valuelist)

    return Response(content=str(preprocessing_results), media_type="application/json")


def preprocess_internal(acc_x, acc_y, acc_z, bvp, eda, temp):

    # create dataframes
    df_acc = pd.DataFrame(list(zip(acc_x, acc_y, acc_z)), columns =['x', 'y', 'z'])
    df_bvp = pd.DataFrame(bvp, columns =['BVP'])
    df_eda = pd.DataFrame(eda, columns =['EDA'])
    df_temp = pd.DataFrame(temp, columns =['TEMP'])

    window_length = 30
    window_step_size = 1

    res = get_features(df_acc, df_bvp, df_eda, df_temp, window_length, window_step_size)

    # columns to keep
    columns_to_keep = ['bvp_BVP_mean', 'bvp_BVP_std', 'bvp_BVP_sum', 'bvp_BVP_skewness',
        'bvp_BVP_kurtosis','bvp_BVP_peaks','bvp_BVP_n_above_mean','bvp_BVP_n_below_mean',
        'bvp_BVP_n_sign_changes','bvp_BVP_perm_entropy','bvp_BVP_svd_entropy','bvp_l2_min',
        'bvp_l2_n_above_mean','bvp_l2_n_below_mean','bvp_l2_n_sign_changes','bvp_l2_perm_entropy',
        'acc_x_mean','acc_x_std','acc_x_energy','acc_x_skewness','acc_x_kurtosis','acc_x_peaks',
        'acc_x_lineintegral','acc_x_n_above_mean','acc_x_n_sign_changes','acc_x_iqr','acc_y_mean',
        'acc_y_std','acc_y_energy','acc_y_skewness','acc_y_kurtosis','acc_y_peaks','acc_y_n_above_mean',
        'acc_y_n_sign_changes','acc_y_iqr','acc_y_svd_entropy','acc_z_mean','acc_z_std','acc_z_min',
        'acc_z_max','acc_z_energy','acc_z_skewness','acc_z_kurtosis','acc_z_peaks','acc_z_n_above_mean',
        'acc_z_n_sign_changes','acc_z_svd_entropy','acc_l2_skewness','acc_l2_kurtosis','acc_l2_n_above_mean',
        'acc_l2_n_below_mean','eda_EDA_mean','eda_EDA_std','eda_EDA_skewness','eda_EDA_kurtosis','eda_EDA_peaks',
        'eda_EDA_n_above_mean','eda_EDA_n_below_mean','eda_EDA_perm_entropy','eda_EDA_svd_entropy',
        'temp_TEMP_mean','temp_TEMP_std','temp_TEMP_skewness','temp_TEMP_kurtosis','temp_TEMP_lineintegral',
        'temp_TEMP_n_above_mean','temp_TEMP_n_below_mean','temp_TEMP_iqr','temp_TEMP_perm_entropy',
        'temp_TEMP_svd_entropy','temp_l2_svd_entropy']
    
    res = res[columns_to_keep]

    return res.iloc[0].to_list()


def get_features(df_acc, df_bvp, df_eda, df_temp, window_length, window_step_size):
    
    # calculate features
    acc_features = get_features_inner(df_acc, ['x', 'y', 'z'], 'acc_', window_length, window_step_size, 32)
    bvp_features = get_features_inner(df_bvp, ['BVP'], 'bvp_', window_length, window_step_size, 64)
    eda_features = get_features_inner(df_eda, ['EDA'], 'eda_', window_length, window_step_size, 4)
    temp_features = get_features_inner(df_temp, ['TEMP'], 'temp_', window_length, window_step_size, 4)

    # merge
    res = pd.concat([bvp_features, acc_features, eda_features, temp_features], axis=1)

    return res


def get_features_inner(df, columns_list, prefix, window_length, window_step_size, frequency):
     
    # we need to set a correct datetime index (nanoseconds calculated from frequency)
    # otherwise Flirt will create a wrong timeindex
    ns = '250000000N'
    if frequency == 64:
        ns = '15625000N'
    elif frequency == 32:
        ns = '31250000N'
    time_index = pd.date_range(start=0, periods=len(df), freq=ns)
    df = df.set_index(time_index)
    
    df = df[columns_list]
    df = df.dropna()

    features = flirt.get_acc_features(df,
                                      window_length=window_length, 
                                      window_step_size=window_step_size,
                                      data_frequency=frequency)
    features = features.add_prefix(prefix)
    return features
