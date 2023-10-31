from flask import Blueprint, render_template, redirect


smartagent_bp = Blueprint("smartagent", __name__, template_folder="templates", static_folder='static', static_url_path='/smartagent/static')
@smartagent_bp.route('/smartagent/home')
def a5digitalHome():
    return render_template("homepage.html")