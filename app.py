from flask import Flask, jsonify, request, send_from_directory

from db import init_db, save_calculation, fetch_history

app = Flask(__name__)

# Try to initialize the database, but do not crash the app if Mongo is not
# immediately available. This avoids depending on Flask lifecycle hooks that
# may differ across versions or environments.
try:
    init_db()
except Exception:
    # Initialization will be attempted again on demand (lazy) when saving
    # a calculation or fetching history.
    pass


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
        # support pagination: ?limit=100&skip=0
        limit_raw = request.args.get("limit", "100")
        skip_raw = request.args.get("skip", "0")
        try:
            limit = int(limit_raw)
            skip = int(skip_raw)
        except ValueError:
            return jsonify({"error": "limit and skip must be integers"}), 400

        items = fetch_history(limit=limit, skip=skip)
        return jsonify({"history": items}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch history", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
