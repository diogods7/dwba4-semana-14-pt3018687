import logging
import traceback
from flask import redirect

import flask
from replit import db

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
    return flask.jsonify(error=str(e)), 500

@app.route('/', methods=['GET', 'POST'])
def cadastroContatos():
  try:
    contatos = db.get('contatos', {}); 
    print(contatos);
    if flask.request.method == "POST":      
      contatos[flask.request.form['email']] = {'nome': flask.request.form['nome'], 'telefone': flask.request.form['telefone'],'assunto': flask.request.form['assunto'], 'mensagem': flask.request.form['mensagem'],'re': flask.request.form['re']}
    db['contatos'] = contatos
    return flask.render_template('contatos.html', contatos=contatos)
  except Exception as e:
    logging.exception('failed to database')
    flask.abort(500, description=str(e) + ': ' + traceback.format_exc())

@app.route('/limparBanco', methods=['POST'])
def limparBanco():
  try:
    del db["contatos"];
    return flask.render_template('contatos.html')
  except Exception as e:
    logging.exception(e)
    return flask.render_template('contatos.html')

@app.route('/deletarContato/<email>', methods=['POST'])
def deletarContato(email):
    try:
      contatos = db.get('contatos', {});
      del contatos[email];
      db['contatos'] = contatos;
      return redirect('/');
    except Exception as e:
      logging.exception(e);
      return flask.render_template('contatos.html');
    
app.run('0.0.0.0')