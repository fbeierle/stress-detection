import pandas as pd
import numpy as np
from sklearn.preprocessing import MaxAbsScaler
from sklearn.ensemble import ExtraTreesClassifier
import joblib
import utils


def train():
    '''
    Trains the ExtraTreesClassifier model with the training data.
    Dumps the model to /model/model.joblib
    Stores the test data in /test-data/ as paraquet files, one for stress, one for no stress.
    '''

    # read data
    windowsize = 30
    stepsize = 1
    X_train, y_train, groups_train, X_test, y_test, groups_test = utils.read_data(windowsize, stepsize)

    # store test data
    df_test = X_test
    # df_test['subject'] = groups_test
    df_test['label'] = y_test

    if not os.path.isdir('test-data'):
        os.makedirs('test-data')

    df_test_stress = df_test[df_test['label'] == 1]
    df_test_nostress = df_test[df_test['label'] == 0]

    df_test_stress = df_test_stress.drop(columns={'label'})
    df_test_nostress = df_test_nostress.drop(columns={'label'})

    df_test_stress.to_parquet('test-data/test-data-stress.parquet', compression='ZSTD')
    df_test_nostress.to_parquet('test-data/test-data-nostress.parquet', compression='ZSTD')


    # get train data as numpy arrays
    X_train = X_train.to_numpy()

    # train model
    model = ExtraTreesClassifier(bootstrap=True,
                             criterion="log_loss",
                             max_features=0.6,
                             min_samples_leaf=5,
                             min_samples_split=14,
                             n_estimators=50,
                             random_state=0)
    
    model.fit(X_train, y_train.values.ravel())

    # store model
    if not os.path.isdir('model'):
        os.makedirs('model')
    
    joblib.dump(model, 'model/model.joblib')


def predict(data):
    '''
    Classifies the given (preprocessed) data into stress/no stress.
    Expects an array.
    Returns 0 or 1.
    '''

    model = joblib.load('model/model.joblib')
    data = [data]
    pred = model.predict(data)
    pred = pred[0]
    return pred