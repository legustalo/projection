from flask import Flask, request, jsonify, send_from_directory
import re

app = Flask(__name__)



def calcular_media(notas_str):
    notas = list(map(float, re.findall(r"\d+(?:\.\d+)?", notas_str)))

    if not notas:
        return "Nenhuma nota encontrada."

    media = sum(notas) / len(notas)
    resultado = f"Média: {media:.2f}\n"

    if 6.0 <= media <= 10:
        resultado += "Situação: Aprovado(a) ✓"
    elif 0 <= media < 6.0:
        resultado += "Situação: Reprovado(a) ✗"

    return resultado


def calcular_faltas(faltas_str, total_str):
    try:
        faltas = int(faltas_str)
        total_aulas = int(total_str)

        if total_aulas <= 0:
            return "Total de aulas inválido."

        percentual = (faltas / total_aulas) * 100
        limite     = total_aulas * 0.25

        resultado  = f"Faltas: {faltas}/{total_aulas} ({percentual:.1f}%)\n"
        resultado += f"Limite permitido: {limite:.0f} faltas (25%)\n"

        if faltas <= limite:
            resultado += "Situação: Frequência OK"
        else:
            resultado += "Situação: Reprovado(a) por falta"

        return resultado

    except ValueError:
        return "Por favor, insira valores numéricos válidos."


def condicionais(perguntas):
    pergunta = perguntas.lower()

    if 'horário' in pergunta or 'horario' in pergunta:
        return {"tipo": "resposta", "texto": "O horário da aula é das 19h às 22h."}

    elif 'nota' in pergunta or 'média' in pergunta or 'media' in pergunta:
        return {"tipo": "pedir_notas"}

    elif 'falta' in pergunta or 'faltei' in pergunta or 'frequência' in pergunta or 'frequencia' in pergunta:
        return {"tipo": "pedir_faltas"}

    else:
        return {"tipo": "resposta", "texto": "Não entendi sua pergunta. Tente perguntar sobre horário, notas ou faltas."}


# Rotas Flask
@app.route("/")
def index():
    # Serve o arquivo HTML principal
    return send_from_directory(".", "index.html")


@app.route("/perguntar", methods=["POST"])
def perguntar():
    """
    Recebe: { "pergunta": "qual minha média?" }
    Retorna: { "tipo": "resposta" | "pedir_notas" | "pedir_faltas", "texto": "..." }
    """
    dados    = request.get_json()
    pergunta = dados.get("pergunta", "")
    return jsonify(condicionais(pergunta))


@app.route("/calcular_media", methods=["POST"])
def rota_media():
    """
    Recebe: { "notas": "7 8 9.5" }
    Retorna: { "texto": "Média: 8.17\nSituação: Aprovado ✓" }
    """
    dados = request.get_json()
    notas = dados.get("notas", "")
    return jsonify({"texto": calcular_media(notas)})


@app.route("/calcular_faltas", methods=["POST"])
def rota_faltas():
    """
    Recebe: { "faltas": "5", "total": "40" }
    Retorna: { "texto": "Faltas: 5/40 ..." }
    """
    dados  = request.get_json()
    faltas = dados.get("faltas", "")
    total  = dados.get("total", "")
    return jsonify({"texto": calcular_faltas(faltas, total)})


if __name__ == "__main__":
    app.run(debug=True)