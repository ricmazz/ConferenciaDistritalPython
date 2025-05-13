@echo off
echo Iniciando servidor Flask com Waitress...
cd /d C:\Projetos\Python\ConferenciaDistritalPython

REM Verifica se o ambiente virtual já existe
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo Ambiente virtual não encontrado. Criando novo ambiente...
    python -m venv venv
)

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Instala as dependências, se ainda não estiverem
pip install -r requirements.txt

REM Roda o servidor
python app.py

pause