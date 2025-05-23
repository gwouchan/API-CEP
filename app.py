from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello, world!'), 200

@app.route('/senai', methods=['GET'])
def senai():
    return jsonify(message='Eai, turma do Senai!!!!'), 200

@app.route('/pesquisacep/<cep>', methods=['GET'])
def pesquisacep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    resposta = requests.get(url)
    return resposta.json()

@app.route('/tempo/<cidade>', methods=['GET'])
def pesquisatemperatura(cidade):
    url = f'https://api.weatherapi.com/v1/current.json?key=c4380707dde242f4b78202712252204&q={cidade}&lang=pt'
    resposta = requests.get(url)
    result = resposta.json()

    cidade = result['location']['name']
    regiao = result['location']['region']
    temperatura = result['current']['temp_c']
    umidade = result['current']['humidity']
    condicao = result['current']['condition']['text']
    visibilidade = result['current']['vis_km']
    pressao = result['current']['pressure_mb']


    

    #return resposta.json()
    return render_template("paginatempo.html", cid = cidade, reg = regiao, temp = temperatura, umid = umidade,
                           cond = condicao, vis = visibilidade, press = pressao)

if __name__ == '__main__':
    app.run(debug=True)

