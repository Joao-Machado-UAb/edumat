from flask import Flask, jsonify, request, send_from_directory
from typing import Dict, List, Optional
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
# Simulação de um banco de dados de analytics
analytics_db: Dict[str, List[Dict]] = {
    "activity123": [
        {
            "inveniraStdID": 1001,
            "quantAnalytics": [
                {"name": "Acedeu à atividade", "value": True},
                {"name": "Download documento 1", "value": True},
                {"name": "Evolução pela atividade (%)", "value": "33.3"},
            ],
            "qualAnalytics": [
                {
                    "Student activity profile": "https://ActivityProvider/?APAnID=11111111"
                },
                {"Actitivy Heat Map": "https://ActivityProvider/?APAnID=21111111"},
            ],
        },
        {
            "inveniraStdID": 1002,
            "quantAnalytics": [
                {"name": "Acedeu à atividade", "value": True},
                {"name": "Download documento 1", "value": False},
                {"name": "Evolução pela atividade (%)", "value": "10.0"},
            ],
            "qualAnalytics": [
                {
                    "Student activity profile": "https://ActivityProvider/?APAnID=11111112"
                },
                {"Actitivy Heat Map": "https://ActivityProvider/?APAnID=21111112"},
            ],
        },
    ]
}


def get_activity_analytics(activity_id: str) -> Optional[List[Dict]]:
    """
    Recupera os dados analíticos de uma atividade específica.
    """
    return analytics_db.get(activity_id)


@app.route("/", methods=["POST"])  # Mudamos a rota para a raiz '/'
def handle_analytics_request():
    """
    Endpoint para processar pedidos de analytics de atividades.
    Espera receber um JSON com o formato: {"activityID": "string"}
    """
    try:
        request_data = request.get_json()

        if not request_data or "activityID" not in request_data:
            return (
                jsonify(
                    {"error": "Pedido inválido. É necessário fornecer um activityID."}
                ),
                400,
            )

        activity_id = request_data["activityID"]
        analytics_data = get_activity_analytics(activity_id)

        if analytics_data is None:
            return (
                jsonify(
                    {
                        "error": f"Não foram encontrados dados para a atividade {activity_id}"
                    }
                ),
                404,
            )

        return jsonify(analytics_data)

    except Exception as e:
        return jsonify({"error": f"Erro ao processar o pedido: {str(e)}"}), 500


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
