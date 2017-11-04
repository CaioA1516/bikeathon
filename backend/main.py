#!flask/bin/python
from flask import Flask
from flask import abort
from flask import request
from user import User
from flask_sqlalchemy import SQLAlchemy
import stripe
import json
import ssl

from db_manager import db
from db_manager import app

#Get speed and distance reading
@app.route('/sensor', methods=['POST'])
def postBikeData():
	jsonDict = request.get_json()
	print jsonDict
	#Throw error if data not included
	if not jsonDict or not 'speed' in jsonDict or not 'distance' in jsonDict or not 'bikeid' in jsonDict:
		abort(400)

	print "SPEED", jsonDict['speed'], "DISTANCE", jsonDict['distance'], "BIKE_ID", jsonDict['bikeid']
	return 'ok', 200

#Return index.html
@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

#Charge user
@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)


#Set up Stripe
def setupStripe():
	# Set your secret key: remember to change this to your live secret key in production
	# See your keys here: https://dashboard.stripe.com/account/apikeys
	config = open("config.json").read()
	configDict = json.loads(config)
	stripe.api_key = configDict['stripe_api_key']

	# Token is created using Checkout or Elements!
	# Get the payment token ID submitted by the form:
	stripe.Charge.retrieve(
	  "ch_1BKZ5Q2eZvKYlo2CrmTJgJBF",
	  api_key="sk_test_BQokikJOvBiI2HlWgH4olfQ2"
	)
	
if __name__ == '__main__':
    app.run(debug=True)