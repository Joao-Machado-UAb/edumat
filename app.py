from flask import Flask, jsonify, request, send_from_directory, render_template_string
from ActivityProvider import ActivityProvider

app = Flask(__name__)
activity_provider = ActivityProvider()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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
    return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}&student_id={student_id}"})

@app.route('/analytics', methods=['POST'])
def analytics():
    data = request.get_json()
    activity_id = data.get('activityID')

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

@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    data = request.get_json()
    exercise = data.get('exercise')
    activity_provider.add_exercise(exercise)
    return jsonify({"message": "Exercise added successfully"})

@app.route('/get_exercises', methods=['GET'])
def get_exercises():
    exercises = activity_provider.get_exercises()
    return jsonify(exercises)

@app.route('/add_exercise_form', methods=['GET'])
def add_exercise_form():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adicionar Exercício</title>
    </head>
    <body>
        <h1>Adicionar Exercício de Equação</h1>
        <form id="exerciseForm">
            <label for="exercise">Exercício:</label><br>
            <textarea id="exercise" name="exercise" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Adicionar Exercício">
        </form>
        <script>
            document.querySelector('#exerciseForm').addEventListener('submit', function(event) {
                event.preventDefault();
                const exercise = document.getElementById('exercise').value;
                fetch('/add_exercise', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ exercise: exercise })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                });
            });
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

