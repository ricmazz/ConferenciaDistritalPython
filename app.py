from flask import Flask
from waitress import serve
from routes import registrar_rotas

app = Flask(__name__)
registrar_rotas(app)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)