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
    base64_str = request.args.get("p")
    
    if not base64_str:
        return render_template("erro.html", mensagem="O link de confirmação está incorreto ou incompleto.")

    try:
        decoded = base64.b64decode(base64_str).decode("utf-8")
        codigo, nome, cargo, clube = decoded.split(";")
    except Exception:
        return render_template("erro.html", mensagem="Erro ao ler o QrCode, tente confirmar a presença pela lista de inscritos.")

    lista_inscritos = carregar_dados_planilha("ListaInscritos")
    
    if not any(i.numero == int(codigo) for i in lista_inscritos):
        return render_template("erro.html", mensagem="Esta inscrição não foi encontrada.")

    lista_presenca = carregar_dados_planilha("ListaPresenca")
    if any(i.numero == int(codigo) for i in lista_presenca):
        return render_template("erro.html", mensagem="Esta inscrição já foi confirmada anteriormente.")

    novo_inscrito = Inscrito(numero=codigo, nome=nome, cargo=cargo, clube=clube)
    registrar_presenca(novo_inscrito)

    return render_template("inscricaoconfirmada.html", inscrito={
        "numero": codigo,
        "nome": nome,
        "cargo": cargo,
        "clube": clube
    })