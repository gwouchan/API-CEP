from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)