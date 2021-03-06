from flask import Flask, render_template, request, jsonify,url_for
from db_utils import OperacoesBD
import stripe
import yaml

conf = yaml.load(open('conf/application.yml'))

secret_key = conf['app']['secret_key']
publishable_key = conf['app']['publishable_key']

stripe.api_key = secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = conf['app']['api_secret_key']

connection, cursor = OperacoesBD.conexao_bd_rds(conf)

@app.route('/')
def index():
	return render_template('index.html', key=publishable_key)

@app.route('/charge', methods=['POST'])
def charge():
	amount = request.form['creditos']
	amount = amount.replace(",", "")
	user_id = request.form['id']
	
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

	if user_id != '':
		OperacoesBD.atualiza_saldo(connection,cursor,amount,user_id)

	return render_template('charge.html', amount=amount)

@app.route('/saldo_usuario/<string:id_usuario>', methods=['GET'])
def getSaldoUsuario(id_usuario):
	if id_usuario != None:
		saldo = OperacoesBD.retorna_saldo_usuario_reais(cursor, id_usuario)
		return jsonify(saldo=str(saldo))
	else:
		return 'Id inválido!'

if __name__ == '__main__':
	app.run(threaded=True)