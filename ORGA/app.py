from flask import Flask, redirect, request, render_template
from flask_cors import CORS
from analizador import Analizador
import datetime
import json

app = Flask(__name__, template_folder="templates")

CORS(app)

app.config.update(
    TESTING=True,
    SECRET_KEY="192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf",
)


@app.route("/interpretar", methods=["POST"])
def main_page():
    if request.method == "POST":
        a = Analizador(request.get_json()['entrada'].upper())
        print(a.get_dictionary())
        #Analizador.analisis()
        return {"Respuesta": "Enviado con Exito"}


@app.route("/", methods=["GET", "POST"])
def inventory():
    if request.method == "GET":
        return {"Success": "200"}


if __name__ == "__main__":
    app.run(debug=True, port=4000)
    # ui.run()
