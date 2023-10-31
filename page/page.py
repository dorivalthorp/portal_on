from flask import Blueprint, render_template, redirect


page_bp = Blueprint("page", __name__, template_folder="templates", static_folder='static', static_url_path='/page/static')
