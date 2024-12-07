# app.py

from flask import Flask, jsonify, request, render_template
from singleton_db import SingletonDB

app = Flask(__name__)

# Instância única do SingletonDB
singleton_db = SingletonDB()

# Página de inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de configuração da atividade e parâmetros respetivos
@app.route('/config', methods=['GET'])
def config():
    return '''
    <form>
        <label for="resumo">Resumo:</label><br>
        <input type="text" id="resumo" name="resumo"><br>
        <label for="instrucoes">URL:</label><br>
        <input type="text" id="instrucoes" name="instrucoes"><br>
        <input type="hidden" id="hidden_resumo" name="hidden_resumo">
        <input type="hidden" id="hidden_instrucoes" name="hidden_instrucoes">
        <input type="submit" value="Submit">
    </form>
    <a href="/">Voltar à Página Inicial</a>
    <script>
        document.querySelector('form').addEventListener('submit', function(event) {
            event.preventDefault();
            document.getElementById('hidden_resumo').value = document.getElementById('resumo').value;
            document.getElementById('hidden_instrucoes').value = document.getElementById('instrucoes').value;
            alert('Configuração salva com sucesso!');
        });
    </script>
    '''

# parametros json
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
    singleton_db.create_instance(activity_id)
    return jsonify({"url": f"https://edumat7.onrender.com/atividade?id={activity_id}"})


# Deploy da atividade - Segunda Etapa
@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json()
    activity_id = data.get('activityID')
    student_id = data.get('Inven!RAstdID')
    json_params = data.get('json_params')
    resumo = json_params.get('resumo', '')
    instrucoes = json_params.get('instrucoes', '')
    singleton_db.execute_operations(activity_id, resumo, instrucoes)
    return jsonify({"url": f"https://edumat7.onrender.com/atividade?id={activity_id}&student_id={student_id}"})

# Analytics de atividade
@app.route('/analytics', methods=['POST'])
def analytics():
    data = request.get_json()
    activity_id = data.get('activityID')
    analytics_data = singleton_db.access_data(activity_id)
    return jsonify(analytics_data)

# atividade equações
@app.route('/equacoes', methods=['GET'])
def equacoes():
    activity_id = request.args.get('activityID')
    data = singleton_db.access_data(activity_id)
    if data:
        resumo = data.get('resumo', '')
        instrucoes = data.get('instrucoes', '')
    else:
        resumo = "Resumo de equações de 7º ano: Aqui você pode encontrar um resumo das equações de 7º ano."
        instrucoes = "https://www.matematica.pt/aulas-exercicios.php?id=190"
    return render_template('equacoes.html', resumo=resumo, instrucoes=instrucoes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
