# app.py
from flask import Flask, jsonify, request, render_template
from facade import ActivityFacade

app = Flask(__name__)
facade = ActivityFacade()


@app.route("/json_params", methods=["GET"])
def json_params():
    return jsonify(facade.get_activity_config(None))


@app.route("/analytics_list", methods=["GET"])
def analytics_list():
    return jsonify(facade.get_analytics_config())


@app.route("/deploy", methods=["POST"])
def deploy():
    data = request.get_json()
    return jsonify(
        facade.deploy_activity(
            data.get("activityID"), data.get("Inven!RAstdID"), data.get("json_params")
        )
    )


@app.route("/analytics", methods=["GET"])
def analytics():
    analytics_data = facade.get_analytics()
    return render_template("analytics.html", analytics_data=analytics_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
