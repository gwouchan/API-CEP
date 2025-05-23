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

@app.route('/')
def home():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)

