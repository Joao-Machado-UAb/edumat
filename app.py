from flask import Flask, jsonify, request, send_from_directory
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Página de configuração da atividade e parâmetros respetivos
@app.route('/config', methods=['GET'])
def config():
    return '''
    <form>
        <label for="resumo">Resumo da dos Conteúdos de Equações de 7.º ano:</label><br>
        <input type="text" id="resumo" name="resumo"><br>
        <label for="instrucoes">URL para o resumo:</label><br>
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

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Analytics de atividade
@app.route('/provide_analytics', methods=['POST'])
def provide_analytics():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        activity_id = data.get('activityID')
        json_params = data.get('json_params')

        if not activity_id:
            return jsonify({"error": "activityID is required"}), 400

        # Aqui você pode armazenar os dados necessários para a atividade
        logging.info(f"Received analytics request for activityID: {activity_id}")

        return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}"})

    except Exception as e:
        logging.error(f"Error processing analytics request: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
