
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "clave-local-solo-para-el-laboratorio"

users = {
    "alice": "alice123",
    "bob": "bob123"
}

orders = {
    101: {"owner": "alice", "product": "Laptop", "total": 3000},
    102: {"owner": "bob", "product": "Phone", "total": 1500}
}


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if username not in users or users[username] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    session.clear()
    session["username"] = username

    return jsonify({"message": "Login successful"})


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    if "username" not in session:
        return jsonify({"error": "Authentication required"}), 401

    order = orders.get(order_id)

    if order is None or order["owner"] != session["username"]:
            return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "order_id": order_id,
        "owner": order["owner"],
        "product": order["product"],
        "total": order["total"]
    })


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
