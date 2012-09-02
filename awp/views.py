# Main Views file for non-app pages
from flask import *

## Imports
from awp import app

## Start routing
@app.route('/')
def show_homepage():
	messagehome = ''
	return render_template('index.html', messagehome=messagehome)

@app.route('/about')
def show_aboutpage():
	return render_template('about.html')

@app.route('/contact')
def show_contactpage():
	return render_template('contact.html')