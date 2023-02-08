import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Stress Recognition - Dr. Felix Beierle",
    page_icon="👋",
    #layout='wide'
)

st.title('Model Explainability')

st.write('''
* We are using SHAP for model explainability, as it creates intuitive plots about feature importance.
* We have to consider that overall, we have 71 features. The plot below shows the top features, but there are many more, each contributing a small amount for the final explanation.
* The features were calculated with the FLIRT library (https://flirt.readthedocs.io/ and https://doi.org/10.1016/j.cmpb.2021.106461). The paper explains the meaning of the features.
* We observe that the perm_entropy (permutation entropy) of the BVP (blood volume pulse) signal is deemed the feature with the most significant impact on the model output. Permutation entropy is defined as a measure of complexity of timeseries data (http://stubber.math-inf.uni-greifswald.de/pub/full/prep/2001/11.pdf). For lower values for this feature, the model is likelier to predict 1 (stress). Given the data we have, it is very difficult for a layperson of the medical field to interpret results like this. What we could imagine is that if there is a high stress level, the pulse is generally high, driving down the complexity of the BVP value. Similarly, we could guess the interpretation of the other features - a medical expert should be involved for more knowledgeable interpretations of these results.
''')

img_shap = Image.open('images/shap-output.png')
st.image(img_shap,
    width=600)