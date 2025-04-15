from flask import Blueprint, render_template, request
import base64
import qrcode
from io import BytesIO
import base64 as b64
from services.spreedsheet import carregar_dados_planilha

qrcode_bp = Blueprint("qrcode", __name__)

@qrcode_bp.route("/gerar-qrcode")
def gerar_qrcode():
    inscritos = carregar_dados_planilha("ListaInscritos")
    return render_template("gerar-qrcode.html", inscritos=inscritos)

@qrcode_bp.route("/gerar-qrcode", methods=["POST"])
def gerar_qrcode_post():
    dados = request.get_json()
    numeros = dados.get("numeros", [])
    host = dados.get("host", "http://localhost:5000")
    etiquetas = gerar_dados_qr_codes(numeros, host=host)
    return render_template("etiquetas.html", inscritos=etiquetas)

def gerar_dados_qr_codes(numeros_inscricoes, host="http://localhost:5000"):
    inscritos = carregar_dados_planilha("ListaInscritos")
    
    lista_com_qr = []

    for inscrito in inscritos:
        if str(inscrito.numero) in numeros_inscricoes:
            dados_str = f"{inscrito.numero},{inscrito.nome},{inscrito.cargo},{inscrito.clube}"
            base64_str = base64.b64encode(dados_str.encode('utf-8')).decode('utf-8')
            url = f"{host}/confirmar?p={base64_str}"

            qr = qrcode.make(url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            img_b64 = b64.b64encode(buffer.getvalue()).decode('utf-8')

            lista_com_qr.append({
                "numero": inscrito.numero,
                "nome": inscrito.nome,
                "cargo": inscrito.cargo,
                "clube": inscrito.clube,
                "qr_code": img_b64
            })

    return lista_com_qr
