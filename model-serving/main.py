from fastapi import FastAPI, Query, HTTPException, Response
import uvicorn
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

class Values(BaseModel):
    valuelist: list = []

# load model
model = joblib.load('model/model.joblib')

@app.post("/predict/", response_model=int, status_code=200)
async def get_prediction(values: Values) -> int:
    '''
    Gets prediction from the predict method in model.
    '''

    #print(values)
    #print(values.valuelist)

    reshaped = np.array(values.valuelist).reshape(1,-1)

    prediction_results_arr = model.predict(reshaped)
    prediction_results = prediction_results_arr[0]

    return Response(content=str(prediction_results), media_type="application/json")
