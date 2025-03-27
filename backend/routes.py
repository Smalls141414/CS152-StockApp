from flask import render_template, request, jsonify, session
from api.retire_calc import calculate
from api.portfolio_value_estimator import estimation

def define_routes(app):
    @app.route("/retire", methods=['GET', 'POST'])
    def retire():
        data = request.get_json()
        print(data)
        retireResponse = calculate( float(data["expend"]), float(data["current_age"]), float(data["retire_age"]))
        return jsonify(retireResponse)

    @app.route("/portfolio", methods=['GET', 'POST'])
    def portfolio():
        data = request.get_json()
        print(data)
        portfolioResponse = estimation(data["ticker"], data["start_date"], data["end_date"], float(data["investment"]), data["frequency"])
        return jsonify(portfolioResponse)