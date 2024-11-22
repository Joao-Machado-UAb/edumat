
from flask import Flask, jsonify, request

app = Flask(__name__)

# Dados de exemplo para os pedidos da Inven!RA
data = {
    "name": "Exercícios de equações do 1.º grau a uma incógnita",
    "config_url": "http://<domínio>/configuracao-atividade.html",
    "json_params_url": "http://<domínio>/json-params-atividade",
    "user_url": "http://<domínio>/deploy-atividade",
    "analytics_url": "http://<domínio>/analytics-atividade",
    "analytics_list_url": "http://<domínio>/lista-analytics-atividade"
}

@app.route('/configuracao-atividade', methods=['GET'])
def get_config_url():
    return jsonify({"config_url": data["config_url"]})

@app.route('/json-params-atividade', methods=['GET'])
def get_json_params_url():
    return jsonify({"json_params_url": data["json_params_url"]})

@app.route('/deploy-atividade', methods=['GET'])
def get_user_url():
    return jsonify({"user_url": data["user_url"]})

@app.route('/analytics-atividade', methods=['GET'])
def get_analytics_url():
    return jsonify({"analytics_url": data["analytics_url"]})

@app.route('/lista-analytics-atividade', methods=['GET'])
def get_analytics_list_url():
    return jsonify({"analytics_list_url": data["analytics_list_url"]})

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)


