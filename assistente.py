import os
import subprocess
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. Carrega a chave de segurança do arquivo .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ouvir():
    print("\n[Ouvindo...] Pode falar!")
    # Abre o microfone nativo do Android
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
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente de mesa inteligente e parceiro de projetos. Responda de forma direta, amigável e conversacional ao Kleberson. Seja breve."},
            {"role": "user", "content": texto_usuario}
        ],
        max_tokens=150
    )
    texto_resposta = resposta.choices[0].message.content
    print(f"Robô: {texto_resposta}")
    return texto_resposta

def falar(texto):
    subprocess.run(["termux-tts-speak", texto])

def iniciar():
    falar("Sistema iniciado com sucesso. Olá Kleberson, estou pronto para trabalhar.")
    
    while True:
        texto_ouvido = ouvir()
        
        # Se você falar uma dessas palavras, o programa encerra
        if texto_ouvido.lower() in ["parar", "desligar", "encerrar", "dormir"]:
            falar("Desligando o sistema. Até logo!")
            break
            
        if texto_ouvido:
            resposta = pensar(texto_ouvido)
            falar(resposta)
        else:
            print("Não entendi ou o microfone falhou. Tentando de novo...")

if __name__ == "__main__":
    iniciar()