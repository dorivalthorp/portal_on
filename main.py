from login.login import login_bp
from homepage.homepage import homepage_bp
from a5digital.a5digital import a5digital_bp
from administracao.administracao import administracao_bp
from gcamp.gcamp import gcamp_bp
from page.page import page_bp
from navbar.navbar import navbar_bp
from smartoperation.smartoperation import smartoperation_bp
from smartagent.smartagent import smartagent_bp
from smartview.smartview import smartview_bp
from televendas.televendas import televendas_bp
from cadastro.cadastro import cadastro_bp
from flask import Flask

app = Flask(__name__)
app.register_blueprint(page_bp)
app.register_blueprint(navbar_bp)
app.register_blueprint(login_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(a5digital_bp)
app.register_blueprint(administracao_bp)
app.register_blueprint(gcamp_bp)
app.register_blueprint(smartoperation_bp)
app.register_blueprint(smartagent_bp)
app.register_blueprint(smartview_bp)
app.register_blueprint(televendas_bp)
app.register_blueprint(cadastro_bp)


if __name__ == '__main__':
    app.run(debug=True)