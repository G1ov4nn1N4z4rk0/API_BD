import json 
#ferramenta que o pynthon disponibiliza
from flask import Flask, Response, request # type: ignore
#conexao com o banco de dados
from flask_sqlalchemy import SQLAlchemy  # type: ignore

#aplicacao do tipo flask
app = Flask('carros')

#havera modificacoes
# por padrao, em aplicacao em producao isso fica FALSE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#configuracao no banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_carro'
#acessando o mysql, minha senha o ip do banco de dados e a tabela
mybd = SQLAlchemy(app)
#configuracao

#estrutura
#definimos a estrutura da tabela tb_carro
class carro(mybd.Model):
    __tablename__ = 'tb_carro'
    id_carro = mybd.Column(mybd.Integer, primary_key = True )
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(10))
#convertemos a tabela em json
    def to_json(self):
        return{"id_carro":self.id_carro, 
            "marca":self.marca,
            "modelo":self.modelo,
            "valor":self.valor,
            "cor":self.cor,
            "numero_vendas":self.numero_vendas,
            "ano":self.ano}


#agora comeca a api pra cima foi ESTRUTURA E CONFIGURACAO
# **************** API *****************
# selecionar tufo (GET)
#GET = VISUALIZAR
@app.route("/carros", methods =["GET"])
def selecionar_carros():

    #EXECUTA UMA CONSULTA NO BANCO DE DADOS PARA OBTER TODOS OS REGISTROS NA TABELA
    #METODO QUERY.ALL() RETORNA UMA LISTA DE OBJETOS 'CARROS'

    carro_objetos = carro.query.all()

    carro_json = [carro.to_json() for carro in carro_objetos]

    return gera_response(200, "carros", carro_json)


#selecionar individual (por id)
@app.route("/carros/<id>", methods=["GET"])
def seleciona_carro_id(id):
    carro_objetos = carro.query.filter_by(id_carro=id).first()
    carro_json = carro_objetos.to_json()

    return gera_response(200, "carros", carro_json)

# cadastrar 
@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()

    try:
        carros = carro(id_carro=body["id_carro"],marca=body["marca"],modelo=body["modelo"],valor=body["valor"], cor=body["cor"], numero_vendas=body["numero_vendas"], ano=body["ano"])
    
        mybd.session.add(carros)
        mybd.session.commit()
        return gera_response(201, "carros", carros.to_json(),"criado com sucesso.")
    except Exception as e:
        print('erro', e)

        return gera_response(400, "carros",{},"erro ao cadastro")
#atualizar

@app.route("/carros/<id>",methods=["PUT"])
def atualizar_carro(id):
   # consultar por id
    carro_objetos = carro.query.filter_by(id_carro=id).first()
  #  corpo da requisicao
    body = request.get_json()

    try:
       if('id_carro'in body):
         carro_objetos.id_carro = body['id_carro']
       if('marca' in body):
         carro_objetos. marca = body['marca']
       if('modelo'in body):
           carro_objetos.modelo = body['modelo']
       if('valor' in body):
           carro_objetos.valor = body['valor']
       if('cor' in body):
           carro_objetos.numero_vendas = body['numero_vendas']
       if('numero_vendas' in body):
           carro_objetos.numero_vendas = body['numero_vendas']
       if('ano' in body):
           carro_objetos.ano = body['ano']

       mybd.session.add(carro_objetos)
       mybd.session.commit()

       return gera_response(200, "carros", carro_objetos.to_json(),"atualizado com sucesso")
       
    except Exception as e:
        print('erro', e)
        return gera_response(400, 'carros',{},'erro ao atualizar')

    #deletar
@app.route("/carros/<id>", methods=["DELETE"])
def deletar_carro(id):
    carro_objetos = carro.query.filter_by(id_carro=id).first()

    try:
        mybd.session.delete(carro_objetos)
        mybd.session.commit()

        return gera_response(200,"carros",carro_objetos.to_json(),"deletado com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "carro",{},"erro")
    
         

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')
    
app.run(port = 5000, host='localhost', debug= True) # debug significa teste


    

##