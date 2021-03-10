from flask import Flask, render_template, request, jsonify, redirect, url_for, abort, send_file
import requests
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

app = Flask(__name__)

# dataset load
df = pd.read_csv('bank-full.csv',';')
df.drop(columns='day month poutcome y'.split(), inplace=True)

# model load
model = joblib.load('logreg_model_final')

# sql database connection initiation
sqldb = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password = 'Briansql290196'
)

c = sqldb.cursor(buffered=True)
query = 'USE bank_final_project'
c.execute(query)

# home route
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# predict route
@app.route('/predict', methods=['GET','POST'])
def predict():
    return render_template('predict.html')

# last 10 inputed data route
@app.route('/last10data', methods=['GET', 'POST'])
def last10data():
    query = '''SELECT * FROM (SELECT * FROM customers ORDER BY time_inserted DESC LIMIT 10) AS T ORDER BY time_inserted DESC LIMIT 10;'''
    
    c.execute(query)
    sql_res = c.fetchall()
    return render_template('last10data.html', data=sql_res)

# predicted route
@app.route('/predicted', methods=['GET','POST'])
def predicted():
    bank = request.form

    age = int(bank['age'])
    job = bank['job']
    marital = bank['marital']
    education = bank['education']
    default = bank['default']
    balance = float(bank['balance'])
    housing = bank['housing']
    loan = bank['loan']
    contact = bank['contact']
    duration = int(bank['duration'])
    campaign = int(bank['campaign'])
    pdays = int(bank['pdays'])
    previous = int(bank['previous'])

    data_input=[[age, job, marital, education, default, balance, housing, loan, contact, duration, campaign, pdays, previous]]

    # create input dataframe and get the prediction probability 
    df_test = pd.DataFrame(data_input, columns = df.columns, index=[0])
    pred = model.predict_proba(df_test)[:,1]

    # if else statement for prediction value that will be inserted into database
    if pred <= 0.5:
        y_pred = 0
    else:
        y_pred = 1

    # inserting all the information from the form, current datetime, and prediction result into database
    query= f'''INSERT INTO `customers` VALUES ({age}, '{job}','{marital}','{education}','{default}','{balance}', '{housing}', '{loan}', '{contact}', {duration}, {campaign}, {pdays}, {previous}, (SELECT NOW()), {y_pred});'''
    c.execute(query)
    sqldb.commit()

    return render_template('predicted.html', data=pred)

@app.route('/predicted_yes', methods=['GET', 'POST'])
def pred_yes():

    query = f'''SELECT * FROM customers WHERE predicted = 1 ORDER BY time_inserted DESC'''
    c.execute(query)
    sql_res = c.fetchall()

    return render_template('predicted_yes.html', data=sql_res)


if __name__ == "__main__":
    app.run(debug=True)