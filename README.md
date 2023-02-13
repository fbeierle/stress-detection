# Stress Detection

This project predicts stress from sensor data from Empatica E4 wrist bands. The project is build on public datasets. This is the capstone project of Felix Beierle in FourthBrain MLE cohort #10. For more details, check out the deployed web-app or the slides (links below).

### ML Pipeline Infrastructure

<img src="web-app/images/stress-detection-infrastructure.png" alt="mle-stack" width="700"/>

### Open TODOs

Finish deployment and demonstrator.


### Limitations

* TODO: In this demo, we are currently querying the model with the preprocessed data. I will update the demo to query the API with the unprocessed data. Then, the backend will process the data and query the model. This is much closer to a real production deployment.
* There are only 15 participants in the WESAD dataset. We should collect more data to get more robust results. Conducting a lab session for doing this will probably quite cost some time and money.
* The study was conducted with the Empatica E4. I am not sure to what extent the results are applicable to other wristbands like the Apple Watch. We should collect data from such wristbands and try to replicate the results.
* If an employer wants to deploy such a model, privacy regulations have to be checked. An alternative would be to deploy a stress detection model as part of an app that a user can choose to install on his/her smartphone.


### Project Pitch Slides

You can find the slides here: https://docs.google.com/presentation/d/1jYoSlDwUnzAsbdbXSUTaDwHXt9nIfGFa


### Deployment

```
git checkout https://github.com/fbeierle/stress-recognition.git
cd stress-recognition
docker compose up --build
```
Then you can enter the web-app on port 8003. The model is being served at port 8002.


### Deployed Web-App

You can reach the deployed web-app here: http://5.189.182.28:8003/

### Query model

You can query the model with an array of values which are features of the Empatica E4 sensor data.
The server is started with
```
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8001
```


Example query:

```
curl -X 'POST' \
  'http://5.189.182.28:8001/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "valuelist": [0.741469, 81.123199, 1423.620000, 0.827793, 3.074085, 74.000000, 903.000000, 1017.000000, 95.000000, 0.999362, 0.663957, 0.060000, 591.000000, 1329.000000, 0.000000, 0.999731, 57.839583, 5.496902, 3240608.000000, 1.657405, 49.744364, 184.000000, 1790.000000, 766.000000, 0.000000, 1.000000, -19.392708, 4.587454, 381237.000000, 2.871800, 13.705477, 85.000000, 218.000000, 7.000000, 1.000000, 0.375299, -13.297917, 6.551781, -49.000000, 17.000000, 210970.000000, -1.985956, 5.751943, 137.000000, 757.000000, 6.000000, 0.580367, 2.997015, 61.204122, 477.000000, 483.000000, 2.310270, 0.052094, 0.492741, -1.176258, 0.000000, 48.000000, 72.000000, 0.971942, 0.022808, 34.083833, 0.015448, -0.167461, 0.222969, 0.380000, 77.000000, 43.000000, 0.020000, 0.834135, 0.002882, 0.002882]
}'
```
