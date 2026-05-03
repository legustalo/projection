# Essa linha do flask faz com que ele crie rotas, receba dados, responda em JSON e envia arquivos numa aplicação web
from flask import Flask, request, jsonify, send_from_directory

# A biblioteca "re" serve para buscar, extrair, validar e manipular padrões específicos de um texto (str)
import re

# Cria o servidor e informa ao flask o arquivo principal
servidor = Flask(__name__)


# Função para calcular média com o parâmetro "notas_str"
def calcular_media(notas_str):
    # Transforma todos os valores numéricos no parâmetro "notas_str" em "float"
    notas = list(map(float, re.findall(r"\d+(?:\.\d+)?", notas_str)))

    # verifica a lista vazia antes de validar os valores
    if not notas:
        return "Nenhuma nota encontrada."

    # Verifica se existe alguma nota (any) maior que 10 ou menor que 0
    elif any(n > 10 or n < 0 for n in notas):
        return "Sua nota não pode ser maior que 10 ou menor que 0."

    # Soma todas as notas da lista "notas" e depois divide pela quantidade de notas na lista "notas"
    media = sum(notas) / len(notas)
    resultado = f"Média: {media:.2f}\n"

    # Verifica se a média é somente maior que 6, pois já está sendo verificado se as notas são maior que 0 ou menor que 10
    if media >= 6.0:
        resultado += "Situação: Aprovado(a)"
    else:
        resultado += "Situação: Reprovado(a)"

    return resultado


def calcular_faltas(faltas_str, total_str):
    # O try está verificando se os valores de "faltas_str" e de "total_str" podem ser convertidos em "int"
    try:
        faltas = int(faltas_str)
        total_aulas = int(total_str)

        # Verifica se o total de aulas é maior que 0, pois não existe divisão com 0
        if total_aulas <= 0:
            return "Total de aulas inválido."

        # Fórmula para adquirir a porcentagem de faltas e multiplicá-las por 100 para obter o valor real em porcentagem
        percentual = (faltas / total_aulas) * 100

        # O limite é o total de aulas multiplicado por 25 por cento
        limite = total_aulas * 0.25

        # Mostra ao usuário o cálculo para chegar no resultado do percentual e o limite permitido
        resultado  = f"Faltas: {faltas}/{total_aulas} ({percentual:.1f}%)\n"
        resultado += f"Limite permitido: {limite:.0f} faltas (25%)\n"

        # Verifica se as faltas estão dentro ou fora do limite
        if faltas <= limite:
            resultado += "Situação: Frequência OK"
        else:
            resultado += "Situação: Reprovado(a) por falta"

        return resultado

    # Exceção se o valor não puder ser convertido em "int"
    except ValueError:
        return "Por favor, insira valores numéricos válidos."


# Toda essa função verifica se as palavras-chave estão na variável "pergunta" a partir do parâmetro "perguntas"
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
@servidor.route("/")
def index():
    # Serve o arquivo HTML principal
    return send_from_directory(".", "index.html")


# Define o endpoint "/perguntar", que aceita requisições do tipo POST
@servidor.route("/perguntar", methods=["POST"])
def perguntar():
    """
    Recebe: { "pergunta": "qual minha média?" }
    Retorna: { "tipo": "resposta" | "pedir_notas" | "pedir_faltas", "texto": "..." }
    """
    dados = request.get_json()
    pergunta = dados.get("pergunta", "")
    return jsonify(condicionais(pergunta))


# Endpoint que recebe os dados em texto e chama a função "calcular_media"
@servidor.route("/calcular_media", methods=["POST"])
def rota_media():
    """
    Recebe: { "notas": "7 8 9.5" }
    Retorna: { "texto": "Média: 8.17\nSituação: Aprovado(a)" }
    """
    dados = request.get_json()
    notas = dados.get("notas", "")
    return jsonify({"texto": calcular_media(notas)})


# Faz a mesma coisa com as faltas
@servidor.route("/calcular_faltas", methods=["POST"])
def rota_faltas():
    """
    Recebe: { "faltas": "5", "total": "40" }
    Retorna: { "texto": "Faltas: 5/40 ..." }
    """
    dados  = request.get_json()
    faltas = dados.get("faltas", "")
    total  = dados.get("total", "")
    return jsonify({"texto": calcular_faltas(faltas, total)})


# Verifica se o código está sendo executado diretamente e executa o servidor em modo debug
if __name__ == "__main__":
    servidor.run(debug=True)
