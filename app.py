from flask import Flask, jsonify, request

app = Flask(__name__)

# Demo data only. A real application would use a database and authenticated sessions.
INVOICES = {
    1001: {"owner": "alice", "amount": 50.00},
    1002: {"owner": "bob", "amount": 75.00},
}

DISCOUNTS = {
    "WELCOME10": {"percent": 10, "used": False},
}


@app.get("/invoices/<int:invoice_id>")
def get_invoice(invoice_id: int):
    username = request.headers.get("X-User")

    if not username:
        return jsonify(error="Authentication required"), 401

    invoice = INVOICES.get(invoice_id)
    if invoice is None:
        return jsonify(error="Invoice not found"), 404

    if invoice["owner"] != username:
        return jsonify(error="Forbidden"), 403



    return jsonify(invoice_id=invoice_id, amount=invoice["amount"])


@app.post("/discounts/<code>/apply")
def apply_discount(code: str):
    discount = DISCOUNTS.get(code)

    if discount is None:
        return jsonify(error="Unknown discount"), 404

    if discount["used"]:
        return jsonify(error="Discount already used"), 409

    discount["used"] = True
    return jsonify(percent=discount["percent"], applied=True)


if __name__ == "__main__":
    app.run(debug=False)