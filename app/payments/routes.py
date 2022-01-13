from flask import Blueprint, jsonify, request
import os
import json
import stripe

payments = Blueprint('payments', __name__, url_prefix='/payments')

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@payments.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        try:
            user = stripe.Customer.retrieve(data[1]['uid'])
        except:
            user = stripe.Customer.create(email=data[1]['email'], name=data[1]['displayName'], id=data[1]['uid'])
        
        intent = stripe.PaymentIntent.create(
            amount=int(data[0]['total']*100), # i'll do this differently -> decide if i want to just use my cart total from the client or if I want to calculate total here
            currency='usd',
            customer=user,
            payment_method_types=['card']
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print(str(e))
        return jsonify(error=str(e)), 403