# ============================================================
#  app.py — Servidor Flask + IA GRATUITA (Groq como padrão)
#  Provedores (sem cartão de crédito):
#    ⚡ Groq (Llama)  -> chave em https://console.groq.com/keys  (PADRÃO, mais estável)
#    🔷 Gemini        -> chave em https://aistudio.google.com/apikey (alternativa)
#  O código detecta automaticamente qual chave foi configurada.
# ============================================================
import os
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

# Carrega o .env de forma robusta (procura no diretório atual e acima)
_caminho_env = find_dotenv(usecwd=True)
if _caminho_env:
    load_dotenv(_caminho_env, override=True)
else:
    load_dotenv(override=True)


def limpar_chave(valor):
    """Remove espaços e aspas acidentais que causam erro 401."""
    if not valor:
        return ""
    valor = valor.strip()
    if (valor.startswith('"') and valor.endswith('"')) or \
       (valor.startswith("'") and valor.endswith("'")):
        valor = valor[1:-1].strip()
    return valor


app = Flask(__name__)
CORS(app)

SISTEMA = (
    "Você é um assistente virtual amigável e prestativo. "
    "Responda sempre em português do Brasil, de forma clara e simples."
)

CHAVE_GROQ = limpar_chave(os.getenv("GROQ_API_KEY"))
CHAVE_GEMINI = limpar_chave(os.getenv("GEMINI_API_KEY"))
MODEL_IA = os.getenv("MODEL_IA", "").strip()

cliente_groq = None
cliente_gemini = None
provedor_ativo = None

# 1º tenta o Groq (rápido e estável — não sobrecarrega)
if CHAVE_GROQ:
    try:
        from openai import OpenAI
        cliente_groq = OpenAI(api_key=CHAVE_GROQ, base_url="https://api.groq.com/openai/v1")
        provedor_ativo = "Groq (Llama)"
    except Exception as e:
        print(f"[AVISO] Não foi possível iniciar o Groq: {e}")

# 2º tenta o Gemini (alternativa) se não houver Groq
if cliente_groq is None and CHAVE_GEMINI:
    try:
        from google import genai
        cliente_gemini = genai.Client(api_key=CHAVE_GEMINI)
        provedor_ativo = "Google Gemini"
    except Exception as e:
        print(f"[AVISO] Não foi possível iniciar o Gemini: {e}")


def classificar_erro(erro):
    """Transforma erros técnicos em mensagens que o usuário entende."""
    msg = str(erro)
    if "401" in msg or "Unauthenticated" in msg or "API key" in msg or "invalid_api_key" in msg:
        return jsonify({"erro": (
            "Chave da IA inválida (erro 401). Faça assim: "
            "1) Pegue uma chave nova em console.groq.com/keys (recomendado) ou aistudio.google.com/apikey; "
            "2) Cole no .env: GROQ_API_KEY=sua_chave (sem aspas, sem espaços); "
            "3) Pare o servidor (Ctrl+C) e rode python app.py de novo."
        )}), 401
    if "429" in msg or "ResourceExhausted" in msg or "quota" in msg.lower() or "rate limit" in msg.lower():
        return jsonify({"erro": "Limite gratuito atingido. Aguarde cerca de 1 minuto e tente novamente."}), 429
    if "503" in msg or "UNAVAILABLE" in msg or "disconnected" in msg.lower() or "timeout" in msg.lower():
        return jsonify({"erro": "Servidor da IA instável neste momento. Aguarde um momento e tente novamente."}), 503
    if "404" in msg or "not found" in msg.lower() or "no longer available" in msg or "model" in msg.lower() and "not" in msg.lower():
        return jsonify({"erro": (
            "Modelo de IA não disponível. Defina MODEL_IA no .env com um modelo atual "
            "(ex: MODEL_IA=llama-3.3-70b-versatile) e reinicie o servidor."
        )}), 500
    return jsonify({"erro": f"Falha na IA ({provedor_ativo}): {msg}"}), 500


def chamar_groq(mensagem):
    """Chama o Groq com retry automático em falhas transitórias."""
    modelo = MODEL_IA or "llama-3.3-70b-versatile"
    ultimo_erro = None
    for tentativa in range(3):
        try:
            resp = cliente_groq.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": SISTEMA},
                    {"role": "user", "content": mensagem},
                ],
                temperature=0.7,
                max_tokens=800,
            )
            return jsonify({
                "resposta": resp.choices[0].message.content.strip(),
                "provedor": f"Groq ({modelo})",
            })
        except Exception as e:
            msg = str(e)
            ultimo_erro = e
            if "404" in msg or "not found" in msg.lower():
                break  # modelo errado: para e trata no classificar_erro
            if "503" in msg or "disconnected" in msg.lower() or "timeout" in msg.lower():
                time.sleep(2 * (tentativa + 1))
                continue
            raise
    raise ultimo_erro


MODELOS_GEMINI = ["gemini-3.8-flash", "gemini-2.5-flash"]


def chamar_gemini(mensagem):
    """Chama o Gemini (fallback) com retry e vários modelos."""
    from google.genai import types
    candidatos = [MODEL_IA] if MODEL_IA else []
    candidatos += [m for m in MODELOS_GEMINI if m not in candidatos]
    ultimo_erro = None

    for nome_modelo in candidatos:
        for tentativa in range(3):
            try:
                resp = cliente_gemini.models.generate_content(
                    model=nome_modelo,
                    contents=mensagem,
                    config=types.GenerateContentConfig(
                        system_instruction=SISTEMA, temperature=0.7, max_output_tokens=800
                    ),
                )
                return jsonify({
                    "resposta": (resp.text or "").strip(),
                    "provedor": f"Google Gemini ({nome_modelo})",
                })
            except Exception as e:
                msg = str(e)
                ultimo_erro = e
                if "no longer available" in msg or "404" in msg or "not found" in msg.lower():
                    break
                if "503" in msg or "UNAVAILABLE" in msg or "disconnected" in msg.lower() or "timeout" in msg.lower():
                    time.sleep(2 * (tentativa + 1))
                    continue
                raise
    raise ultimo_erro


@app.route("/")
def pagina_inicial():
    return render_template("index.html")


@app.route("/api/status")
def status():
    """Diagnóstico rápido — mostra se cada chave foi lida corretamente."""
    return jsonify({
        "ia_ativa": provedor_ativo is not None,
        "provedor": provedor_ativo,
        "env_encontrado": _caminho_env or "não encontrado",
        "groq_chave_lida": bool(CHAVE_GROQ),
        "groq_inicio_chave": (CHAVE_GROQ[:6] + "...") if CHAVE_GROQ else None,
        "groq_tamanho": len(CHAVE_GROQ) if CHAVE_GROQ else 0,
        "gemini_chave_lida": bool(CHAVE_GEMINI),
        "gemini_inicio_chave": (CHAVE_GEMINI[:6] + "...") if CHAVE_GEMINI else None,
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        dados = request.get_json(silent=True) or {}
        mensagem = (dados.get("mensagem") or "").strip()

        if not mensagem:
            return jsonify({"erro": "A mensagem está vazia."}), 400

        if cliente_groq is None and cliente_gemini is None:
            return jsonify({"resposta": (
                "Ainda não configurei a chave da IA! É de graça e não precisa de cartão. "
                "Recomendado: vá em console.groq.com/keys, crie sua chave, cole no .env "
                "em GROQ_API_KEY=sua_chave (sem aspas), reinicie o servidor e eu respondo!"
            )})

        if cliente_groq is not None:
            return chamar_groq(mensagem)
        return chamar_gemini(mensagem)

    except Exception as e:
        return classificar_erro(e)


if __name__ == "__main__":
    debug = os.getenv("DEBUG", "False").lower() == "true"
    print(f"[INFO] Provedor de IA ativo: {provedor_ativo or 'NENHUM (sem chave)'}")
    print(f"[INFO] .env carregado de: {_caminho_env or 'não encontrado'}")
    app.run(host="0.0.0.0", port=5000, debug=debug)
