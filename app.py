import flask
import pickle

import pandas as pd
from pandas import MultiIndex, Int16Dtype
from pandas import Index
import xgboost as xgb


# Use pickle to import model
with open(f'model/bike_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')
# Create histogramme graphique space
df = pd.read_csv('data/bike_data.csv')


@app.route('/bike_page')
def bike_page():
    return flask.render_template('bike_page.html')


@app.route('/table_data')
def table_data():
    return flask.render_template('table_data.html')


@app.route('/', methods=['GET', 'POST'])
def main():

    if flask.request.method == 'GET':

        return (flask.render_template('main.html'))
    if flask.request.method == 'POST':
        temperature = flask.request.form['temperature']
        humidity = flask.request.form['humidity']
        windspeed = flask.request.form['windspeed']
        input_variables=pd.DataFrame([[temperature, humidity, windspeed]],
                                     columns=['temperature', 'humidity', 'windspeed'],
                                     dtype=float)
        prediction=model.predict(input_variables)[0]

        return flask.render_template('main.html', original_input={'Temperature': temperature, "Humidity": humidity, 'Windspeed': windspeed},
                                     result=prediction)


if __name__ == '__main__':
    app.run()


