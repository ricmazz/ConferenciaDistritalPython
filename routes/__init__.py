from .home import home_bp
from .registrar import registrar_bp
from .lista import lista_bp
from .gerar_qrcode import qrcode_bp

def registrar_rotas(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(registrar_bp)
    app.register_blueprint(lista_bp)
    app.register_blueprint(qrcode_bp)