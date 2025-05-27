from flask import Flask, jsonify, render_template, request
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

#==============================================

@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

#==============================================



@app.route('/clima')
def homepage():
    return render_template('pagclima.html')

@app.route('/estados', methods=['GET'])
def lista_estado():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    resposta = requests.get(url)
    result = resposta.json()
    
    estados = sorted([estado['sigla'] for estado in result])
    
    return jsonify(estados)
        
@app.route('/cidades/<estado>', methods=['GET'])
def lista_cidades(estado):
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado}/municipios'
    resposta = requests.get(url)
    result = resposta.json()

    cidades = [cidade['nome'] for cidade in result]
    
    return jsonify(cidades)

@app.route('/clima/<estado>/<cidade>', methods=['GET'])
def consulta_clima(estado, cidade):
    url = f'https://api.weatherapi.com/v1/current.json?key=c4380707dde242f4b78202712252204&q={cidade}&lang=pt'
    
    resposta = requests.get(url)
    result = resposta.json()

    temperatura = result.get('current', {}).get('temp_c', 'Dados indisponíveis')
    umidade = result.get('current', {}).get('humidity', 'Dados indisponíveis')
    condicao = result.get('current', {}).get('condition', {}).get('text', 'Dados indisponíveis')
    visibilidade = result.get('current', {}).get('vis_km', 'Dados indisponíveis')
    pressao = result.get('current', {}).get('pressure_mb', 'Dados indisponíveis')
    

    return jsonify({
        'temperatura': temperatura,
        'umidade': umidade,
        'condicao': condicao,
        'visibilidade': visibilidade,
        'pressao': pressao
    })

#=======================================================

@app.route('/cep', methods = ['GET', 'POST'])
def buscarcep():
    if request.method == 'POST':
        cep = request.form.get('cep')
        url = f'https://viacep.com.br/ws/{cep}/json/'
        resposta = requests.get(url)
        if resposta.status_code != 200:
            return render_template('pagcep.html', erro = 'Erro ao consultar CEP.')
        
        result = resposta.json()
        
        if result.get('erro'):
            return render_template('pagcep.html', erro = 'CEP não encontrado')
        

        return render_template('pagcep.html',
            logradouro = result['logradouro'],
            bairro = result['bairro'],
            localidade = result['localidade'],
            estado = result['estado'],
            uf = result['uf'],
            regiao = result['regiao'],
            ddd = result['ddd']
        )

    elif request.method == 'GET':
        return render_template('pagcep.html')


if __name__ == '__main__':
    app.run(debug=True)

