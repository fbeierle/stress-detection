import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.model_selection import train_test_split

def create_train_test(df, nsplits, subject_column, label_column):
    '''
    Creates a train, test split. Each subject is in one of the sets with all his/her data.
    Takes a df, number of splits, names of the subject and label column.
    Returns 2 dataframes with train and test set.
    '''
    X = df.drop(columns=[subject_column, label_column])
    y = df[[label_column]]
    groups = df[subject_column]
    
    gkf = GroupKFold(n_splits=nsplits)
    train_idx, test_idx = next(gkf.split(X, y, groups))

    X_train = X.iloc[train_idx.tolist(), :]
    y_train = y.iloc[train_idx.tolist(), :]
    groups_train = groups.iloc[train_idx.tolist()]
    
    X_test = X.iloc[test_idx.tolist(), :]
    y_test = y.iloc[test_idx.tolist(), :]
    groups_test = groups.iloc[test_idx.tolist()]
    
    res_train = pd.concat([X_train, groups_train, y_train], axis=1)
    res_test = pd.concat([X_test, groups_test, y_test], axis=1)
    
    return res_train, res_test


def create_train_val_test(df, nsplits_val, nplsits_test, subject_column, label_column):
    '''
    Creates a train, val, test split. Each subject is in one of the sets with all his/her data.
    Takes a df, number of splits for train/val split, number of splits for train+val/test split,
    names of the subject and label column.
    Returns 3 dataframes with train, val, and test set.
    '''
    # get train_temp and test
    res_train_temp, res_test = create_train_test(df, nplsits_test, subject_column, label_column)
    
    # get train and val from train_temp
    res_train, res_val = create_train_test(res_train_temp, nsplits_val, subject_column, label_column)
    
    return res_train, res_val, res_test


def split_df(df, subject_column, label_column):
    '''
    Takes a df and splits it into three dfs, containing the features, labels, and groups.
    '''
    X = df.drop(columns=['subject', 'label'])
    y = df[['label']]
    groups = df['subject']
    return X, y, groups


def remove_correlated_features(df, correlation):
    '''
    Takes a df and removed the correlated features with a correlation value equal or higher to the given value.
    Returns the resulting df and a list of the retained features.
    '''
    cor = df.corr(numeric_only = True)
    keep_columns = np.full(cor.shape[0], True)
    for i in range(cor.shape[0] - 1):
        for j in range(i + 1, cor.shape[0] - 1):
            if (np.abs(cor.iloc[i, j]) >= 0.8):
                keep_columns[j] = False
    selected_columns = df.columns[keep_columns]
    df_reduced = df[selected_columns]
    
    return df_reduced, selected_columns


# for testing purposes, we also create methods for splitting WITHOUT considering groups
def create_train_test_nogrp(df, nsplits, subject_column, label_column):

    X = df.drop(columns=[subject_column, label_column])
    y = df[[label_column]]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    res_train = pd.concat([X_train, y_train], axis=1)
    res_test = pd.concat([X_test, y_test], axis=1)
    
    return res_train, res_test


def split_df_nogrp(df, subject_column, label_column):
    '''
    Takes a df and splits it into three dfs, containing the features, labels, and groups.
    '''
    X = df.drop(columns=['label'])
    y = df[['label']]
    return X, y

def read_data(windowsize, stepsize):
    '''
    Takes the window size and steps size of the calculates features.
    Returns X_train, y_train, groups_train, X_test, y_test, groups_test.
    Prints out info during creation.
    '''
    
    df = pd.read_parquet('data-input/flirt-wesad-acc-bvp-eda-temp-'+str(windowsize)+'-'+str(stepsize)+'.parquet')
    
    # remove columns (see EDA)
    columns_to_drop = ['eda_EDA_n_sign_changes',
     'temp_TEMP_peaks',
     'acc_y_entropy',
     'acc_l2_n_sign_changes',
     'acc_x_entropy',
     'acc_z_entropy',
     'temp_l2_n_sign_changes',
     'bvp_BVP_entropy',
     'temp_TEMP_n_sign_changes',
     'temp_l2_peaks',
     'eda_l2_n_sign_changes']

    df = df.drop(columns=columns_to_drop)
    
    # split into train and test
    df_train, df_test = create_train_test(df, 5, 'subject', 'label')

    X_train, y_train, groups_train = split_df(df_train, 'subject', 'label')
    X_test, y_test, groups_test = split_df(df_test, 'subject', 'label')

    # remove correlated features from train
    X_train, selected_features = remove_correlated_features(X_train, 0.8)

    # remove the same columns from test
    X_test = X_test[selected_features]
    
    # print info
    print('Window Size: ',windowsize,'  Stepsize: ',stepsize)
    print('train shape: ', X_train.shape)
    print('test shape: ', X_test.shape)
    print('test columns: ',X_train.columns)
    
    # Check train and test set sizes
    print('Percentage train set:', len(y_train)/(len(y_train)+len(y_test)))
    print('Percentage test set:', len(y_test)/(len(y_train)+len(y_test)))

    print('\nClass distribution in train set: \n', y_train['label'].value_counts(normalize=True), '\n')

    print('Class distribution in test set: \n', y_test['label'].value_counts(normalize=True), '\n')
    
    return X_train, y_train, groups_train, X_test, y_test, groups_test