from flask import Flask, jsonify, make_response, request

from currency_converter import CurrencyConverter, InvalidCurrencyRateError


app = Flask(__name__)
converter = CurrencyConverter()


@app.route("/convert", methods=["POST"])
def convert_currency():
    try:
        # Unpack data
        data = request.get_json()
        ccy_from = data.get("ccy_from")
        ccy_to = data.get("ccy_to")
        quantity = data.get("quantity")

        if not all([ccy_from, ccy_to, quantity]):
            return make_response(
                jsonify({
                    "status": "error",
                    "message": "Missing required fields. ccy_from, ccy_to and quantity are required."
                }),
                400
            )

        result = converter.convert(ccy_from, ccy_to, quantity)
        return make_response(
            jsonify({
                "status": "success",
                "data": {"quantity": result, "ccy": ccy_to}
            }),
            200
        )

    except InvalidCurrencyRateError as e:
        return make_response(
            jsonify({
                "status": "error",
                "message": e.message
            }),
            400
        )

    except Exception as e:
        return make_response(
            jsonify({
                "status": "error",
                "message": "An unexpected error occured."
            }),
            500
        )


if __name__ == "__main__":
    app.run(debug=True)
