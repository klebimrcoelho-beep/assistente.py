import os
import subprocess
import json
from dotenv import load_dotenv
from openai import OpenAI

# Carrega a chave de segurança do arquivo .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. CRIANDO A MEMÓRIA DO ROBÔ E AJUSTANDO O COMPORTAMENTO
historico = [
    {"role": "system", "content": "Você é um assistente de mesa inteligente e parceiro de projetos. Aja naturalmente, como em uma conversa humana contínua. Você está falando com o Kleberson, mas NÃO repita o nome dele o tempo todo, use apenas de vez em quando se for muito natural. Seja direto, amigável e evite respostas muito longas."}
]

def ouvir():
    print("\n[Ouvindo...] Pode falar!")
    resultado = subprocess.run(["termux-dialog", "speech", "-i", "Fale com o robô..."], capture_output=True, text=True)
    
    try:
        dados = json.loads(resultado.stdout)
        texto = dados.get("text", "")
        print(f"Você disse: {texto}")
        return texto
    except:
        return ""

def pensar(texto_usuario):
    print("[Pensando...]")
    
    # 2. SALVANDO O QUE VOCÊ DISSE NA MEMÓRIA
    historico.append({"role": "user", "content": texto_usuario})
    
    # Limita a memória às últimas 10 interações para não gastar muitos créditos e o robô não ficar lento
    if len(historico) > 11:
        historico.pop(1)

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historico,
        max_tokens=150
    )
    
    texto_resposta = resposta.choices[0].message.content
    print(f"Robô: {texto_resposta}")
    
    # 3. SALVANDO O QUE O ROBÔ RESPONDEU NA MEMÓRIA
    historico.append({"role": "assistant", "content": texto_resposta})
    
    return texto_resposta

def falar(texto):
    subprocess.run(["termux-tts-speak", texto])

def iniciar():
    falar("Memória ativada. Pode falar comigo.")
    
    while True:
        texto_ouvido = ouvir()
        
        # Palavras para desligar o robô
        if texto_ouvido.lower() in ["parar", "desligar", "encerrar", "dormir", "tchau"]:
            falar("Desligando o sistema. Até logo!")
            break
            
        if texto_ouvido:
            resposta = pensar(texto_ouvido)
            falar(resposta)
        else:
            print("Não entendi ou o microfone falhou. Tentando de novo...")

if __name__ == "__main__":
    iniciar()