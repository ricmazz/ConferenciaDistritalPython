from flask import Blueprint, render_template, request, redirect, url_for
import base64
from services.spreedsheet import carregar_dados_planilha, registrar_presenca, Inscrito

registrar_bp = Blueprint("registrar", __name__)

@registrar_bp.route("/registrar")
def registrar():
    lista_inscritos = carregar_dados_planilha("ListaInscritos")
    lista_presenca = carregar_dados_planilha("ListaPresenca")
    codigos_presentes = {p.numero for p in lista_presenca}

    for inscrito in lista_inscritos:
        inscrito.presente = inscrito.numero in codigos_presentes

    return render_template("registrar.html", inscritos=lista_inscritos)


# Novo endpoint para confirmação de presença manual
@registrar_bp.route("/confirmar-presenca", methods=["POST"])
def confirmar_presenca():
    numero = request.form.get("numero")

    if not numero:
        return render_template("erro.html", mensagem="Número de inscrição não informado.")

    lista_inscritos = carregar_dados_planilha("ListaInscritos")

    inscrito = next((i for i in lista_inscritos if str(i.numero) == str(numero)), None)

    if not inscrito:
        return render_template("erro.html", mensagem="Inscrição não encontrada.")

    lista_presenca = carregar_dados_planilha("ListaPresenca")
    if any(str(i.numero) == str(numero) for i in lista_presenca):
        return render_template("erro.html", mensagem="Esta inscrição já foi confirmada anteriormente.")

    registrar_presenca(inscrito)

    return render_template("inscricaoconfirmada.html", inscrito={
        "numero": inscrito.numero,
        "nome": inscrito.nome,
        "cargo": inscrito.cargo,
        "clube": inscrito.clube
    })

@registrar_bp.route("/confirmar")
def confirmar_inscricao():
    numero = request.args.get("p")

    if not numero:
        return render_template("erro.html", mensagem="O link de confirmação está incorreto ou incompleto.")

    lista_inscritos = carregar_dados_planilha("ListaInscritos")

    inscrito = next((i for i in lista_inscritos if str(i.numero) == str(numero)), None)
    if not inscrito:
        return render_template("erro.html", mensagem="Esta inscrição não foi encontrada.")

    lista_presenca = carregar_dados_planilha("ListaPresenca")
    if any(str(i.numero) == str(numero) for i in lista_presenca):
        return render_template("erro.html", mensagem="Esta inscrição já foi confirmada anteriormente.")

    registrar_presenca(inscrito)

    return render_template("inscricaoconfirmada.html", inscrito={
        "numero": inscrito.numero,
        "nome": inscrito.nome,
        "cargo": inscrito.cargo,
        "clube": inscrito.clube
    })