from flask import Flask, render_template, redirect, url_for, request
from nipyapi import config, canvas, security, nifi
from vvdatalab_nifi_flow_generator import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        error = None
        if request.method == 'POST':
            if security.service_login('nifi',request.form['username'],request.form['password'],True) == False:
                error = 'Invalid Credentials. Please try again.'
            else:
                return redirect(url_for('home'))
    except:
        error = 'Invalid Credentials. Please try again.'
    
    return render_template('login.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', error='error')    