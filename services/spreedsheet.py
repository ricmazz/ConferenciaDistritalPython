import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Inscrito:
    numero: str
    nome: str
    cargo: str
    clube: str
    presente: bool = False

def carregar_dados_planilha(nome_aba):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Controle de Presença").worksheet(nome_aba)
    return [Inscrito(
        numero=linha["Numero"],
        nome=linha["Nome"],
        cargo=linha["Cargo"],
        clube=linha["Clube"]
    ) for linha in sheet.get_all_records()]

def registrar_presenca(inscrito: Inscrito):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Controle de Presença").worksheet("ListaPresenca")
    hora_confirmacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sheet.append_row([inscrito.numero, inscrito.nome, inscrito.cargo, inscrito.clube, hora_confirmacao])