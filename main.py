from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from model import predict

app = FastAPI()

class Values(BaseModel):
    valuelist: list = []

@app.post("/predict/", response_model=int, status_code=200)
def get_prediction(values: Values):
    '''
    Gets prediction from the predict method in model.
    '''

    print(values)
    print(values.valuelist)

    prediction_results = predict(values.valuelist)

    print(prediction_results)

    if not prediction_results:
        raise HTTPException(status_code=400, detail="Model not found.")

    return prediction_results