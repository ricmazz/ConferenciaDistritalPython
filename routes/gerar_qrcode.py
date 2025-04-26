from flask import Blueprint, render_template, request, send_file
import base64
import qrcode
from io import BytesIO
import base64 as b64
from services.spreedsheet import carregar_dados_planilha
import zipfile
import io
import qrcode.image.svg

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

@qrcode_bp.route("/baixar-qrcodes", methods=["POST"])
def baixar_qrcodes():
    dados = request.get_json()
    numeros = dados.get("numeros", [])
    host = dados.get("host", "http://localhost:5000")
    inscritos = carregar_dados_planilha("ListaInscritos")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for inscrito in inscritos:
            if str(inscrito.numero) in numeros:
                dados_str = f"{inscrito.numero};{inscrito.nome};{inscrito.cargo};{inscrito.clube}"
                base64_str = base64.b64encode(dados_str.encode('utf-8')).decode('utf-8')
                url = f"{host}/confirmar?p={base64_str}"

                factory = qrcode.image.svg.SvgImage
                qr = qrcode.make(url, image_factory=factory)
                buffer = BytesIO()
                qr.save(buffer)
                buffer.seek(0)
                
                filename = f"{inscrito.numero} - {inscrito.nome}.svg"
                zip_file.writestr(filename, buffer.read())

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name="qrcodes.zip"
    )

def gerar_dados_qr_codes(numeros_inscricoes, host="http://localhost:5000"):
    inscritos = carregar_dados_planilha("ListaInscritos")
    
    lista_com_qr = []

    for inscrito in inscritos:
        if str(inscrito.numero) in numeros_inscricoes:
            dados_str = f"{inscrito.numero};{inscrito.nome};{inscrito.cargo};{inscrito.clube}"
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
