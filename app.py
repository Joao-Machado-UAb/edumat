
from flask import Flask, jsonify, request

app = Flask(__name__)

# Dados de exemplo para os pedidos da Inven!RA
data = {
    "name": "Exercícios de equações do 1.º grau a uma incógnita",
    "config_url": "https://edumat7.onrender.com/configuracao-atividade.html",
    "json_params_url": "https://edumat7.onrender.com/json-params-atividade",
    "user_url": "https://edumat7.onrender.com/deploy-atividade",
    "analytics_url": "https://edumat7.onrender.com/analytics-atividade",
    "analytics_list_url": "https://edumat7.onrender.com/lista-analytics-atividade"
}

@app.route("/")
def home():
    return "AP - EDUM@T7"
    
@app.route('/configuracao-atividade', methods=['GET'])
def get_config_url():
    return jsonify({"config_url": data["config_url"]})

@app.route('/json-params-atividade', methods=['POST'])
def get_json_params_url():
    params = [
        {"name": "Equações do 1.º Grau a uma incógnita", "type": "text/plain"},
        {"name": "Questão sobre equações do 1.º Grau a uma incógnita", "type": "text/plain"}
    ]
    return jsonify(params)

@app.route('/deploy-atividade', methods=['POST'])
def get_user_url():
    return jsonify({"user_url": data["user_url"]})

@app.route('/analytics-atividade', methods=['GET'])
def get_analytics_url():
    return jsonify({"analytics_url": data["analytics_url"]})

@app.route('/lista-analytics-atividade', methods=['GET'])
def get_analytics_list_url():
    analytics = {
        "qualAnalytics": [
            {"name": "Acesso à atividade", "type": "boolean"},
            {"name": "Download de recursos", "type": "boolean"},
            {"name": "Upload de documentos", "type": "boolean"},
            {"name": "Relatório das respostas concretamente dadas", "type": "text/plain"}
        ],
        "quantAnalytics": [
            {"name": "Número de acessos", "type": "integer"},
            {"name": "Download de recursos", "type": "integer"},
            {"name": "Progresso na atividade (%)", "type": "integer"}
        ]
    }
    return jsonify(analytics)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)


