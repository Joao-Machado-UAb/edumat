# app.py

from flask import Flask, jsonify, request, render_template
from activity_facade import ActivityFacade

app = Flask(__name__)
activity_facade = ActivityFacade()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_activity", methods=["POST"])
def create_activity():
    activity_id = request.json.get('activity_id')
    result = activity_facade.create_activity(activity_id)
    return jsonify(result), 201

@app.route("/update_activity", methods=["PUT"])
def update_activity():
    data = request.json
    result = activity_facade.update_activity(
        data.get('activity_id'), 
        data.get('resumo'), 
        data.get('instrucoes')
    )
    return jsonify(result), 200

@app.route("/analytics", methods=["GET"])
def get_analytics():
    activity_id = request.args.get('activity_id')
    analytics = activity_facade.get_activity_analytics(activity_id)
    return render_template("analytics.html", analytics_data=analytics)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
