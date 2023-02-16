import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Stress Detection - Dr. Felix Beierle",
    page_icon="👋",
    #layout='wide'
)

st.title('Limitations')

st.write('''
* There are only 15 participants in the WESAD dataset. We should collect more data to get more robust results. Conducting a lab session for doing this will probably quite cost some time and money.
* The study was conducted with the Empatica E4. I am not sure to what extent the results are applicable to other wristbands like the Apple Watch. We should collect data from such wristbands and try to replicate the results.
* If an employer wants to deploy such a model, privacy regulations have to be checked. An alternative would be to deploy a stress detection model as part of an app that a user can choose to install on his/her smartphone.
* When collecting more data, we could collect data with labels indicating a level of stress instead of binary stress/no stress values. Then we could predict a stress level instead of a binary label.
''')

#  - The delay of preprocessing is likely larger than that of querying the model / inference.