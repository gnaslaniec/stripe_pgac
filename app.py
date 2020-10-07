from flask import Flask, render_template, request
import stripe
import yaml

conf = yaml.load(open('conf/application.yml'))

secret_key = conf['app']['secret_key']
publishable_key = conf['app']['publishable_key']

stripe.api_key = secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = conf['app']['api_secret_key']

@app.route('/')
def index():
	return render_template('index.html', key=publishable_key)

@app.route('/charge', methods=['POST'])
def charge():
	amount = request.form['creditos']
	amount = amount.replace(",", "")
	
	customer = stripe.Customer.create(
		email=request.form['stripeEmail'],
		card=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
		customer=customer.id,
		amount=int(amount),
		currency='brl',
		description='Recarga de créditos PGAC'
	)

	return render_template('charge.html', amount=amount)

if __name__ == '__main__':
	app.run(threaded=True)