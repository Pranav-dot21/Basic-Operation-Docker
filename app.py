from flask import Flask, jsonify, request, send_from_directory

from db import init_db, save_calculation, fetch_history

app = Flask(__name__)


@app.before_first_request
def startup():
    init_db()


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    input1 = data.get("input1")
    input2 = data.get("input2")
    operator = data.get("operator")

    try:
        a = float(input1)
        b = float(input2)
    except (TypeError, ValueError):
        return jsonify({"error": "input1 and input2 must be numeric"}), 400

    if operator not in {"+", "-", "*", "/"}:
        return jsonify({"error": "Invalid operator"}), 400

    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    elif operator == "*":
        result = a * b
    else:
        if b == 0:
            return jsonify({"error": "Division by zero"}), 400
        result = a / b

    save_calculation(a, b, operator, result)
    return jsonify({"result": result}), 200


@app.route("/history", methods=["GET"])
def history():
    try:
        items = fetch_history()
        return jsonify({"history": items}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch history", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
