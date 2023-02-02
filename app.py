import flask
from flask import render_template, request
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib


model = joblib.load('model/model_bike.sav')

app = flask.Flask(__name__, template_folder='templates')

# Create histogramme graphique space
df = pd.read_csv('data/bike_data.csv')


@app.route('/bike_page')
def bike_page():
    return flask.render_template('bike_page.html')


@app.route('/table_data')
def table_data():
    data = pd.read_csv('data/bike_data.csv')
    data.to_csv('sample_data.csv', index=None)
    data_view = data[['date', 'temperature', 'humidity', 'windspeed', 'count']].head(n=40)
    return flask.render_template('table_data.html', tables=[data_view.to_html(classes='data_bike')], titles=[''])


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        windspeed = request.form['windspeed']
        input_variables = pd.DataFrame([[temperature, humidity, windspeed]],
                                       columns=['temperature', 'humidity', 'windspeed'],
                                       dtype=float)
        result = model.predict(input_variables)[0]
        input_view = input_variables.reset_index()
        return flask.render_template('main.html', original_input=input_view, result=round(result, 0))


if __name__ == '__main__':
    app.run()
