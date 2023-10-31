from flask import Blueprint, render_template, redirect


smartoperation_bp = Blueprint("smartoperation", __name__, template_folder="templates", static_folder='static', static_url_path='/smartoperation/static')
@smartoperation_bp.route('/smartoperation/home')
def smartoperation():
    return render_template("homepage.html")