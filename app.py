from flask import Flask, jsonify, request, send_from_directory

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
@app.route('/provide_analytics', methods=['POST'])
def provide_analytics():
    if request.is_json:
        data = request.get_json()
        activity_id = data.get('activityID')
        # Aqui você pode buscar os dados analíticos da atividade
        return jsonify([
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
        ])
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415
        
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
