from flask import Flask, jsonify, request, send_from_directory

from flask_cors import CORS  # Para permitir requisições cross-origin

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Página de configuração da atividade e parâmetros respetivos
@app.route('/config', methods=['GET'])
def config():
    return '''
    <form>
        <label for="activity_name">Nome da Atividade:</label><br>
        <input type="text" id="activity_name" name="activity_name"><br>
        <label for="question">Questão:</label><br>
        <input type="text" id="question" name="question"><br>
        <input type="submit" value="Submit">
    </form>
    '''

@app.route('/json_params', methods=['GET'])
def json_params():
    return jsonify([
        {"name": "Equações do 1.º Grau a uma incógnita", "type": "text/plain"},
        {"name": "Questão sobre equações do 1.º Grau a uma incógnita", "type": "text/plain"}
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

# Deploy da atividade
@app.route('/user_url', methods=['GET'])
def user_url():
    activity_id = request.args.get('activityID')
    return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}"})

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json()
    activity_id = data.get('activityID')
    student_id = data.get('Inven!RAstdID')
    json_params = data.get('json_params')
    # Aqui você pode armazenar os dados necessários para a atividade
    return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}&student_id={student_id}"})

# Analytics de atividade
from flask import Flask, jsonify, request

app = Flask(__name__)

# Adiciona CORS usando decorator do Flask
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/provide_analytics', methods=['POST'])
def provide_analytics():
    try:
        # Verifica se os dados são JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        
        # Verifica se activityID está presente
        activity_id = data.get('activityID')
        if not activity_id:
            return jsonify({"error": "activityID is required"}), 400

        # Seus dados analíticos
        analytics_data = [
            {
                "inveniraStdID": 1001,
                "qualAnalytics": [
                    {"name": "Acesso à atividade", "value": True},
                    {"name": "Download de recursos", "value": True},
                    {"name": "Upload de documentos", "value": True},
                    {"name": "Relatório das respostas concretamente dadas", "value": "Suficiente"}
                ],
                "quantAnalytics": [
                    {"name": "Número de acessos", "value": 50},
                    {"name": "Download de recursos", "value": 12},
                    {"name": "Progresso na atividade (%)", "value": 10.0}
                ],
            },
            {
                "inveniraStdID": 1002,
                "qualAnalytics": [
                    {"name": "Acesso à atividade", "value": True},
                    {"name": "Download de recursos", "value": True},
                    {"name": "Upload de documentos", "value": True},
                    {"name": "Relatório das respostas concretamente dadas", "value": "Suficiente"}
                ],
                "quantAnalytics": [
                    {"name": "Número de acessos", "value": 60},
                    {"name": "Download de recursos", "value": 16},
                    {"name": "Progresso na atividade (%)", "value": 40.0}
                ],
            }
        ]

        return jsonify(analytics_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota de teste
@app.route('/', methods=['GET'])
def test():
    return jsonify({"message": "Server is running!"})
        
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
