from flask import Flask, jsonify, request, render_template
import json
import random

app = Flask(__name__)

# Carrega as perguntas
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pergunta", methods=["GET"])
def get_pergunta():
    pergunta = random.choice(questions)
    opcoes = pergunta["opcoes"].copy()
    random.shuffle(opcoes)
    correta_index = opcoes.index(pergunta["opcoes"][pergunta["correta"]])
    pergunta["correta_embaralhada"] = correta_index
    return jsonify({
        "id": pergunta["id"],
        "imagem": pergunta["imagem"],
        "opcoes": opcoes,
        "correta": correta_index,
        "faixa": pergunta.get("faixa", "branca")
    })

@app.route("/responder", methods=["POST"])
def responder():
    data = request.get_json()
    pergunta_id = data.get("pergunta_id")
    resposta = data.get("resposta")
    pergunta = next((q for q in questions if q["id"] == pergunta_id), None)
    if not pergunta:
        return jsonify({"erro": "Pergunta não encontrada"}), 404
    correta = (resposta == pergunta["correta_embaralhada"])
    return jsonify({
        "correta": correta,
        "resposta_correta": pergunta["correta_embaralhada"]
    })

if __name__ == "__main__":
    app.run(debug=True)
