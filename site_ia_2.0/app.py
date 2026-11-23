# ============================================================
#  app.py — Site completo com IA gratuita
#  Backend: Flask + Groq (padrão) / Gemini (alternativa)
#  Fluxo: navegador -> POST /api/chat -> Python -> IA gratuita -> JSON -> tela
# ============================================================
import os
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

# Carrega o .env de forma robusta (procura na pasta atual e acima)
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
    if len(valor) >= 2 and (
        (valor.startswith('"') and valor.endswith('"')) or
        (valor.startswith("'") and valor.endswith("'"))
    ):
        valor = valor[1:-1].strip()
    return valor


app = Flask(__name__)
CORS(app)

SISTEMA = (
    "Você é um assistente virtual amigável, claro e prestativo. "
    "Responda sempre em português do Brasil, de forma objetiva e natural. "
    "Use parágrafos curtos e, quando fizer sentido, liste itens com marcadores."
)

# Modelos gratuitos do Groq (2026). Llama 3.x viraram Enterprise/pagos.
# Tenta o mais rápido primeiro; em 404 parte para o próximo.
MODELOS_GROQ = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
]

# Modelos do Gemini (fallback opcional)
MODELOS_GEMINI = ["gemini-3.8-flash", "gemini-2.5-flash"]

CHAVE_GROQ = limpar_chave(os.getenv("GROQ_API_KEY"))
CHAVE_GEMINI = limpar_chave(os.getenv("GEMINI_API_KEY"))
MODEL_IA = os.getenv("MODEL_IA", "").strip()

cliente_groq = None
cliente_gemini = None
provedor_ativo = None

# 1º: Groq (rápido e estável)
if CHAVE_GROQ:
    try:
        from openai import OpenAI
        cliente_groq = OpenAI(api_key=CHAVE_GROQ, base_url="https://api.groq.com/openai/v1")
        provedor_ativo = "Groq"
    except Exception as e:
        print(f"[AVISO] Groq não iniciou: {e}")

# 2º: Gemini, se não houver Groq
if cliente_groq is None and CHAVE_GEMINI:
    try:
        from google import genai
        cliente_gemini = genai.Client(api_key=CHAVE_GEMINI)
        provedor_ativo = "Gemini"
    except Exception as e:
        print(f"[AVISO] Gemini não iniciou: {e}")


def classificar_erro(erro):
    """Converte erros técnicos em mensagens claras em português."""
    msg = str(erro)
    if "401" in msg or "Unauthenticated" in msg or "invalid_api_key" in msg.lower() or "api key" in msg.lower():
        return jsonify({"erro": (
            "Chave da IA inválida (erro 401). Corrija assim: "
            "1) crie uma chave grátis em console.groq.com/keys; "
            "2) cole no .env como GROQ_API_KEY=sua_chave (sem aspas nem espaços); "
            "3) pare o servidor com Ctrl+C e rode python app.py de novo."
        )}), 401
    if "429" in msg or "ResourceExhausted" in msg or "quota" in msg.lower() or "rate limit" in msg.lower():
        return jsonify({"erro": "Limite gratuito atingido. Aguarde cerca de 1 minuto e tente novamente."}), 429
    if "503" in msg or "UNAVAILABLE" in msg or "disconnected" in msg.lower() or "timeout" in msg.lower():
        return jsonify({"erro": "A IA está instável neste momento. Aguarde alguns segundos e tente novamente."}), 503
    if "404" in msg or "not found" in msg.lower() or "no longer available" in msg:
        return jsonify({"erro": (
            "Modelo não disponível. Modelos gratuitos do Groq: "
            "openai/gpt-oss-20b, openai/gpt-oss-120b, qwen/qwen3.8-27b. "
            "Defina MODEL_IA no .env (ex: MODEL_IA=openai/gpt-oss-20b) e reinicie."
        )}), 500
    return jsonify({"erro": f"Falha na IA ({provedor_ativo}): {msg}"}), 500


def chamar_groq(mensagem):
    """Groq com fallback entre modelos e retry em falhas transitórias."""
    candidatos = [MODEL_IA] if MODEL_IA else []
    candidatos += [m for m in MODELOS_GROQ if m not in candidatos]
    ultimo_erro = None

    for modelo in candidatos:
        for tentativa in range(3):
            try:
                resp = cliente_groq.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": SISTEMA},
                        {"role": "user", "content": mensagem},
                    ],
                    temperature=0.7,
                    max_tokens=1200,
                )
                return jsonify({
                    "resposta": resp.choices[0].message.content.strip(),
                    "provedor": "Groq",
                    "modelo": modelo,
                })
            except Exception as e:
                msg = str(e)
                ultimo_erro = e
                if "404" in msg or "not found" in msg.lower():
                    break  # modelo indisponível: tenta o próximo
                if "503" in msg or "disconnected" in msg.lower() or "timeout" in msg.lower():
                    time.sleep(2 * (tentativa + 1))
                    continue
                raise
    raise ultimo_erro


def chamar_gemini(mensagem):
    """Gemini como alternativa, também com fallback e retry."""
    from google.genai import types
    candidatos = [MODEL_IA] if MODEL_IA else []
    candidatos += [m for m in MODELOS_GEMINI if m not in candidatos]
    ultimo_erro = None

    for modelo in candidatos:
        for tentativa in range(3):
            try:
                resp = cliente_gemini.models.generate_content(
                    model=modelo,
                    contents=mensagem,
                    config=types.GenerateContentConfig(
                        system_instruction=SISTEMA, temperature=0.7, max_output_tokens=1200
                    ),
                )
                return jsonify({
                    "resposta": (resp.text or "").strip(),
                    "provedor": "Gemini",
                    "modelo": modelo,
                })
            except Exception as e:
                msg = str(e)
                ultimo_erro = e
                if "404" in msg or "not found" in msg.lower() or "no longer available" in msg:
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
    """Diagnóstico: mostra qual provedor e chave foram lidos."""
    return jsonify({
        "ia_ativa": provedor_ativo is not None,
        "provedor": provedor_ativo,
        "modelo": MODEL_IA or (MODELOS_GROQ[0] if cliente_groq else (MODELOS_GEMINI[0] if cliente_gemini else None)),
        "groq_chave_lida": bool(CHAVE_GROQ),
        "gemini_chave_lida": bool(CHAVE_GEMINI),
        "env_encontrado": bool(_caminho_env),
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        dados = request.get_json(silent=True) or {}
        mensagem = (dados.get("mensagem") or "").strip()

        if not mensagem:
            return jsonify({"erro": "Digite uma mensagem antes de enviar."}), 400

        if cliente_groq is None and cliente_gemini is None:
            return jsonify({"resposta": (
                "Ainda não configurei a chave da IA! É grátis e sem cartão: "
                "pegue em console.groq.com/keys, cole no .env como "
                "GROQ_API_KEY=sua_chave (sem aspas), reinicie o servidor e eu respondo."
            )})

        if cliente_groq is not None:
            return chamar_groq(mensagem)
        return chamar_gemini(mensagem)

    except Exception as e:
        return classificar_erro(e)


if __name__ == "__main__":
    debug = os.getenv("DEBUG", "False").lower() == "true"
    print(f"[INFO] Provedor ativo: {provedor_ativo or 'NENHUM (sem chave)'}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=debug)
