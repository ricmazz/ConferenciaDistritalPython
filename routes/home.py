from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return render_template("index.html")


# Nova rota para fornecer dados para o gráfico de inscritos vs presentes
@home_bp.route("/dados-grafico")
def dados_grafico():
    from flask import request
    from services.spreedsheet import carregar_dados_planilha

    lista_inscritos = carregar_dados_planilha("ListaInscritos")
    lista_presenca = carregar_dados_planilha("ListaPresenca")

    total_presentes = len(lista_presenca)
    total_inscritos = len(lista_inscritos) - total_presentes

    return {
        "ausentes": total_inscritos,
        "presentes": total_presentes
    }