from ollama import chat
from tools import listar_times

MAX_PASSOS = 3

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "listar_times",
            "description": "Lista os times monitorados pela empresa.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

mensagens = [
    {
        "role": "user",
        "content": "Quais são os times monitorados pela empresa?"
    }
]

for passo in range(MAX_PASSOS):

    print(f"\n--- PASSO {passo + 1} ---")

    resposta = chat(
        model="qwen3:4b",
        messages=mensagens,
        tools=TOOLS
    )

    mensagens.append(resposta.message)

    # Se o modelo não pediu nenhuma ferramenta,
    # significa que chegou à resposta final.
    if not resposta.message.tool_calls:
        print("Resposta final:")
        print(resposta.message.content)
        break

    # Executa as ferramentas solicitadas pelo modelo
    for chamada in resposta.message.tool_calls:

        nome = chamada.function.name
        argumentos = chamada.function.arguments

        print(f"Ferramenta escolhida: {nome}")
        print(f"Argumentos: {argumentos}")

        if nome == "listar_times":
            resultado = listar_times()

            print(f"Resultado da ferramenta: {resultado}")

            mensagens.append(
                {
                    "role": "tool",
                    "content": str(resultado)
                }
            )