from flask import render_template

def define_routes(app):
    @app.route("/test", methods=['GET', 'POST'])
    def test():
	    return "Heelo, World!"
