from flask import Blueprint, render_template, redirect


smartview_bp = Blueprint("smartview", __name__, template_folder="templates", static_folder='static', static_url_path='/smartview/static')
@smartview_bp.route('/smartview/home')
def smartviewHome():
    return render_template("homepage.html")