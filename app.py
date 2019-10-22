from flask import Flask, render_template, redirect, url_for, request
from nipyapi import config, canvas, security, nifi

import sys

import re
import json
import nipyapi

app = Flask(__name__)

@app.route('/')
def test():
    return sys.path