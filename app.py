from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    try:
        a = float(data.get("input1"))
        b = float(data.get("input2"))
    except (TypeError, ValueError):
        return jsonify({"error": "input1 and input2 must be numeric"}), 400

    op = data.get("operator")
    if op not in {"+", "-", "*", "/"}:
        return jsonify({"error": "Invalid operator"}), 400

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    else:
        if b == 0:
            return jsonify({"error": "Division by zero"}), 400
        result = a / b

    return jsonify({"result": result}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
