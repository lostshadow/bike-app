import flask
import pickle
from flask import Flask, render_template, request, url_for
import xgboost as xgb
from sklearn.model_selection import train_test_split
import xgboost as xgb

import pandas as pd
import numpy as np


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
    data = pd.read_csv('data/bike_data.csv')
    df.to_csv('sample_data.csv', index=None)
    return flask.render_template('table_data.html', tables=[data.to_html()], titles=[''])


@app.route('/', methods=['GET', 'POST'])
def main():

    if request.method == 'GET':

        return (render_template('main.html'))
    if request.method == 'POST':
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        windspeed = request.form['windspeed']
        input_variables=pd.DataFrame([[temperature, humidity, windspeed]],
                                     columns=['temperature', 'humidity', 'windspeed'],
                                     dtype=float)
        prediction=model.predict(input_variables)[0]

        return flask.render_template('main.html',temperature=temperature, humidity=humidity, windspeed=windspeed,result=prediction)

if __name__ == '__main__':
    app.run()


