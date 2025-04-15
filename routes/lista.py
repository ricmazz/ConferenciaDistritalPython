from flask import Blueprint, render_template
from services.spreedsheet import carregar_dados_planilha

lista_bp = Blueprint("lista", __name__)

@lista_bp.route("/lista")
def lista():
    inscritos = carregar_dados_planilha("ListaPresenca")
    return render_template("lista.html", inscritos=inscritos)
