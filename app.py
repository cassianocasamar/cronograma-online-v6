
from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "API do Cronograma - Online e Funcionando!"

@app.route("/gerar", methods=["GET"])
def gerar_cronograma():
    try:
        subprocess.run(["python", "gerar_cronograma.py"], check=True)
        return jsonify({"status": "ok", "mensagem": "Cronograma gerado com sucesso!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
