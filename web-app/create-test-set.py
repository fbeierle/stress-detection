# this script creates the unprocessed test-set

import pandas as pd
import numpy as np
import os

# load data
df_acc = pd.read_parquet('../model-development/data-input/dataset_wesad_wrist_acc.parquet')
df_bvp = pd.read_parquet('../model-development/data-input/dataset_wesad_wrist_bvp.parquet')
df_eda = pd.read_parquet('../model-development/data-input/dataset_wesad_wrist_eda.parquet')
df_temp = pd.read_parquet('../model-development/data-input/dataset_wesad_wrist_temp.parquet')

# make sure folder exists
if not os.path.isdir('test-data'):
    os.makedirs('test-data')

def get_user_data(userid):
    df_acc_curr = filter_df(df_acc, userid)
    df_bvp_curr = filter_df(df_bvp, userid)
    df_eda_curr = filter_df(df_eda, userid)
    df_temp_curr = filter_df(df_temp, userid)
    return df_acc_curr, df_bvp_curr, df_eda_curr, df_temp_curr

def filter_df(df, userid):
    df_curr = df[df['subject'] == userid]
    return df_curr

# get data for test users 3, 6, 10
# reduce data by only using the first 25 rows each
df_acc_test = pd.concat([get_user_data(3)[0].head(25), get_user_data(6)[0].head(25), get_user_data(10)[0].head(25)])
df_bvp_test = pd.concat([get_user_data(3)[1].head(25), get_user_data(6)[1].head(25), get_user_data(10)[1].head(25)])
df_eda_test = pd.concat([get_user_data(3)[2].head(25), get_user_data(6)[2].head(25), get_user_data(10)[2].head(25)])
df_temp_test = pd.concat([get_user_data(3)[3].head(25), get_user_data(6)[3].head(25), get_user_data(10)[3].head(25)])

# parquet each type of data to ../test-data/[acc,bvp,eda,temp].parquet
df_acc_test.to_parquet('test-data/acc.parquet', compression='ZSTD')
df_bvp_test.to_parquet('test-data/bvp.parquet', compression='ZSTD')
df_eda_test.to_parquet('test-data/eda.parquet', compression='ZSTD')
df_temp_test.to_parquet('test-data/temp.parquet', compression='ZSTD')
