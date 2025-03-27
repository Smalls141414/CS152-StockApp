from flask import render_template, request, jsonify, session

def define_routes(app):
    @app.route("/retire", methods=['GET', 'POST'])
    def retire():
        data = request.get_json()
        print(data)
        testResponse = {'retire_amt': 5000, 'retire_years': 5, 'inflate_rate': 12, 'time_period': 5, 'retire_amt_raw': 5000}
        return jsonify(testResponse)

    @app.route("/portfolio", methods=['GET', 'POST'])
    def portfolio():
        data = request.get_json()
        print(data)
        testResponse = {'ticker': 'GOOGL', 'avg_price': 12, 'end_price': 13, 'abs_return': 14, 'amount_inv': 15, 'profit': 16, 'value': 17, 'stocks': 18, 'today_value': 19, 'final_profit': 20, 'final_return': 21, 'ann_return': 22}
        return jsonify(testResponse)