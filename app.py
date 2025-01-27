# app.py (refatorização)

from flask import Flask, jsonify, request, render_template
from activity_manager import ActivityManager

app = Flask(__name__)
activity_manager = ActivityManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/config")
def config():
    return render_template("config.html")

@app.route("/json_params")
def json_params():
    return jsonify([
        {"name": "resumo", "type": "text/plain"},
        {"name": "instrucoes", "type": "text/plain"},
    ])

@app.route("/analytics_list")
def analytics_list():
    return jsonify(activity_manager.get_analytics_list())

@app.route("/user_url")
def user_url():
    activity_id = request.args.get("activityID")
    activity_manager.create_activity(activity_id)
    return jsonify({"url": f"https://edumat.onrender.com/atividade?id={activity_id}"})

@app.route("/deploy", methods=["POST"])
def deploy():
    data = request.get_json()
    activity_id = data.get("activityID")
    student_id = data.get("Inven!RAstdID")
    json_params = data.get("json_params", {})
    
    activity_manager.update_activity(
        activity_id,
        resumo=json_params.get("resumo"),
        instrucoes=json_params.get("instrucoes")
    )
    
    return jsonify({
        "url": f"https://edumat.onrender.com/atividade?id={activity_id}&student_id={student_id}"
    })

@app.route("/equacoes")
def equacoes():
    activity_id = request.args.get("activityID")
    student_id = request.args.get("student_id")
    
    activity = activity_manager.get_activity(activity_id, student_id)
    if not activity:
        activity = {
            "resumo": "Resumo de equações de 7º ano: Aqui pode encontrar um resumo das equações de 7º ano.",
            "instrucoes": "https://www.matematica.pt/aulas-exercicios.php?id=190"
        }
    
    return render_template("equacoes.html", resumo=activity["resumo"], 
                         instrucoes=activity["instrucoes"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
