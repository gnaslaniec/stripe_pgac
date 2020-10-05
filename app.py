from flask import Flask, render_template, request
import stripe

secret_key = 'sk_test_51HS281D3aUJGj8sriZtRGrsSNFtEm2J2ZULrUTROYPyjrDI45JSIJgb5U3cOAD6U4RCvEwL23RzOWqnSzSSl0dvg00DHuncnZq'
publishable_key = 'pk_test_51HS281D3aUJGj8srNPXC2f4qOYyTUIEewqenGhZQ7xIJfOCK9o9MIqI9rEnO58Sm0yTBIR9RKbzSy9o9B1Q3cdKU00n5uHJD9T'

stripe.api_key = secret_key

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', key=publishable_key)

@app.route('/charge', methods=['POST'])
def charge():
	amount = request.form['creditos']

	customer = stripe.Customer.create(
		email=request.form['stripeEmail'],
		card=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
		customer=customer.id,
		amount=amount,
		currency='brl',
		description='Recarga PGAC'
	)

	return render_template('charge.html', amount=amount)

if __name__ == '__main__':
	app.run(debug=True)