import json 
from flask import Flask, Respose, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask('carros')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/carro'
#acessando o mysql, minha senha o ip do banco de dados e a tabela

mybd = SQLAlchemy(app)
#
class carro(mybd.Model):
    id = mybd.Column(mybd.integer, primary_key = True )
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.string(100))
    numero_vendas = mybd.Column(mybd.float)
    ano = mybd.Column(mybd.String(10))
#convertemos a tabela em json
def to_json(self):
    return{"id":self.id, 
           "marca":self.marca,
           "modelo":self.modelo,
           "valor":self.valor,
           "cor":self.cor,
           "numero_vendas":self.numero_vendas,
           "ano":self.ano}

# **************** API *****************
# selecionar tufo (GET)
@app.route("/carros", methods =["GET"])
def selecionar_carros():

    #EXECUTA UMA CONSULTA NO BANCO DE DADOS PARA OBTER TODOS OS REGISTROS NA TABELA
    #METODO QUERY.ALL() RETORNA UMA LISTA DE OBJETOS 'CARROS'

    carro_objetos = carro.query.all()

    carro_json = [carro.to_json() for carro in carro_objetos]

    return gera_response(200, "carros", carro_json)