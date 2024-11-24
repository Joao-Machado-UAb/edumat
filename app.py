from flask import Flask, jsonify, request, send_from_directory
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Página de configuração da atividade e parâmetros respetivos
@app.route('/config', methods=['GET'])
def config():
    return '''
    <form>
        <label for="resumo">Sumário:</label><br>
        <input type="text" id="resumo" name="resumo"><br>
        <label for="instrucoes">URL:</label><br>
        <input type="text" id="instrucoes" name="instrucoes"><br>
        <input type="hidden" id="hidden_resumo" name="hidden_resumo">
        <input type="hidden" id="hidden_instrucoes" name="hidden_instrucoes">
        <input type="submit" value="Submit">
    </form>
    <script>
        document.querySelector('form').addEventListener('submit', function(event) {
            event.preventDefault();
            document.getElementById('hidden_resumo').value = document.getElementById('resumo').value;
            document.getElementById('hidden_instrucoes').value = document.getElementById('instrucoes').value;
            alert('Configuração salva com sucesso!');
        });
    </script>
    '''

@app.route('/json_params', methods=['GET'])
def json_params():
    return jsonify([
        {"name": "resumo", "type": "text/plain"},
        {"name": "instrucoes", "type": "text/plain"}
    ])

# Lista de analytics da atividade
@app.route('/analytics_list', methods=['GET'])
def analytics_list():
    return jsonify({
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
    })

# Deploy da atividade - Primeira Etapa
@app.route('/user_url', methods=['GET'])
def user_url():
    activity_id = request.args.get('activityID')
    # Aqui você pode armazenar o activity_id e preparar a atividade
    return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}"})

# Deploy da atividade - Segunda Etapa
@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json()
    activity_id = data.get('activityID')
    student_id = data.get('Inven!RAstdID')
    json_params = data.get('json_params')
    # Aqui você pode armazenar os dados necessários para a atividade
    return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}&student_id={student_id}"})


# Analytics de atividade
@app.route("/provide_analytics", methods=["POST"])
def provide_analytics():
    # URL do serviço analytics
    analytics_url = "https://edumat.onrender.com/provide_analytics"

    # Dados a serem enviados no corpo da requisição
    data = {
        "activityID": "Este texto é o identificador da instância da atividade na Inven!RA"
    }

    # Fazer a requisição POST
    response = requests.post(analytics_url, json=data)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Converter a resposta para JSON
        analytics_data = response.json()

        # Exibir a resposta
        print(json.dumps(analytics_data, indent=4))
    else:
        print(f"Falha na requisição: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
