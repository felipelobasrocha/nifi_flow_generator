from flask import Flask, render_template, redirect, url_for, request
from nipyapi import config, canvas, security, nifi
from vvdatalab_nifi_flow_generator import app

@app.route('/')
def index():
    return 'Hello World!'