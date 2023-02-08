import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Stress Recognition - Dr. Felix Beierle",
    page_icon="👋",
    #layout='wide'
)



st.title('Feature Engineering and Model Building')

#col1, col2 = st.columns(2)

#with col1:

st.write('### Intro')

st.write('''
* There are 15 participants. We want to build a model that works for unseen users. In order to evaluate this, we train the model on a subset of the users and use the data from 3 users only for testing.
* The distribution of the labels is 63% stress, 37% no stress. We will use F1 score as the evaluation metric.
''')

st.write('### Feature Engineering')

st.write('''
* Based on the raw data we saw, we can calculate timeseries features.
  - Features like the sum, mean, ...
* Parameters:
  - Window size
  - Step size
* Smaller window size --> faster prediction
  - Trade-off between F1 score and window-size
''')

img_window = Image.open('images/window-step-size.png')
st.image(img_window,
    width=400)

# timeseries feature calculation with FLIRT


st.write('### Model Building')

st.write('''
* AutoML with TPOT
  - Trying different model
  - trying different window and step sizes
* Results:
  - 30 second window size, 1 second step size
  - ExtraTreesClassifier
* Hyperparameter search with scikit-optimize
  - F1: 0.87, Precision: 0.94, Recall: 0.82
''')

# TPOT for model building, exploring
# scikit-opt for hyperparameter tuning
