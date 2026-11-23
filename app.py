# ============================================================
<<<<<<< HEAD
#  app.py — Site completo com IA gratuita
#  Backend: Flask + Groq (padrão) / Gemini (alternativa)
#  Fluxo: navegador -> POST /api/chat -> Python -> IA gratuita -> JSON -> tela
=======
#  app.py — Servidor Flask + IA GRATUITA (Groq como padrão)
#  Provedores (sem cartão de crédito):
#    ⚡ Groq (Llama)  -> chave em https://console.groq.com/keys  (PADRÃO, mais estável)
#    🔷 Gemini        -> chave em https://aistudio.google.com/apikey (alternativa)
#  O código detecta automaticamente qual chave foi configurada.
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
# ============================================================
import os
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

<<<<<<< HEAD
# Carrega o .env de forma robusta (procura na pasta atual e acima)
=======
# Carrega o .env de forma robusta (procura no diretório atual e acima)
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
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
<<<<<<< HEAD
    if len(valor) >= 2 and (
        (valor.startswith('"') and valor.endswith('"')) or
        (valor.startswith("'") and valor.endswith("'"))
    ):
=======
    if (valor.startswith('"') and valor.endswith('"')) or \
       (valor.startswith("'") and valor.endswith("'")):
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
        valor = valor[1:-1].strip()
    return valor


app = Flask(__name__)
CORS(app)

SISTEMA = (
<<<<<<< HEAD
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

=======
    "Você é um assistente virtual amigável e prestativo. "
    "Responda sempre em português do Brasil, de forma clara e simples."
)

>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
CHAVE_GROQ = limpar_chave(os.getenv("GROQ_API_KEY"))
CHAVE_GEMINI = limpar_chave(os.getenv("GEMINI_API_KEY"))
MODEL_IA = os.getenv("MODEL_IA", "").strip()

cliente_groq = None
cliente_gemini = None
provedor_ativo = None

<<<<<<< HEAD
# 1º: Groq (rápido e estável)
=======
# 1º tenta o Groq (rápido e estável — não sobrecarrega)
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
if CHAVE_GROQ:
    try:
        from openai import OpenAI
        cliente_groq = OpenAI(api_key=CHAVE_GROQ, base_url="https://api.groq.com/openai/v1")
<<<<<<< HEAD
        provedor_ativo = "Groq"
    except Exception as e:
        print(f"[AVISO] Groq não iniciou: {e}")

# 2º: Gemini, se não houver Groq
=======
        provedor_ativo = "Groq (Llama)"
    except Exception as e:
        print(f"[AVISO] Não foi possível iniciar o Groq: {e}")

# 2º tenta o Gemini (alternativa) se não houver Groq
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
if cliente_groq is None and CHAVE_GEMINI:
    try:
        from google import genai
        cliente_gemini = genai.Client(api_key=CHAVE_GEMINI)
<<<<<<< HEAD
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
=======
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
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
        )}), 401
    if "429" in msg or "ResourceExhausted" in msg or "quota" in msg.lower() or "rate limit" in msg.lower():
        return jsonify({"erro": "Limite gratuito atingido. Aguarde cerca de 1 minuto e tente novamente."}), 429
    if "503" in msg or "UNAVAILABLE" in msg or "disconnected" in msg.lower() or "timeout" in msg.lower():
<<<<<<< HEAD
        return jsonify({"erro": "A IA está instável neste momento. Aguarde alguns segundos e tente novamente."}), 503
    if "404" in msg or "not found" in msg.lower() or "no longer available" in msg:
        return jsonify({"erro": (
            "Modelo não disponível. Modelos gratuitos do Groq: "
            "openai/gpt-oss-20b, openai/gpt-oss-120b, qwen/qwen3.8-27b. "
            "Defina MODEL_IA no .env (ex: MODEL_IA=openai/gpt-oss-20b) e reinicie."
=======
        return jsonify({"erro": "Servidor da IA instável neste momento. Aguarde um momento e tente novamente."}), 503
    if "404" in msg or "not found" in msg.lower() or "no longer available" in msg or "model" in msg.lower() and "not" in msg.lower():
        return jsonify({"erro": (
            "Modelo de IA não disponível. Defina MODEL_IA no .env com um modelo atual "
            "(ex: MODEL_IA=llama-3.3-70b-versatile) e reinicie o servidor."
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
        )}), 500
    return jsonify({"erro": f"Falha na IA ({provedor_ativo}): {msg}"}), 500


def chamar_groq(mensagem):
<<<<<<< HEAD
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
=======
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
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
    from google.genai import types
    candidatos = [MODEL_IA] if MODEL_IA else []
    candidatos += [m for m in MODELOS_GEMINI if m not in candidatos]
    ultimo_erro = None

<<<<<<< HEAD
    for modelo in candidatos:
        for tentativa in range(3):
            try:
                resp = cliente_gemini.models.generate_content(
                    model=modelo,
                    contents=mensagem,
                    config=types.GenerateContentConfig(
                        system_instruction=SISTEMA, temperature=0.7, max_output_tokens=1200
=======
    for nome_modelo in candidatos:
        for tentativa in range(3):
            try:
                resp = cliente_gemini.models.generate_content(
                    model=nome_modelo,
                    contents=mensagem,
                    config=types.GenerateContentConfig(
                        system_instruction=SISTEMA, temperature=0.7, max_output_tokens=800
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
                    ),
                )
                return jsonify({
                    "resposta": (resp.text or "").strip(),
<<<<<<< HEAD
                    "provedor": "Gemini",
                    "modelo": modelo,
=======
                    "provedor": f"Google Gemini ({nome_modelo})",
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
                })
            except Exception as e:
                msg = str(e)
                ultimo_erro = e
<<<<<<< HEAD
                if "404" in msg or "not found" in msg.lower() or "no longer available" in msg:
=======
                if "no longer available" in msg or "404" in msg or "not found" in msg.lower():
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
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
<<<<<<< HEAD
    """Diagnóstico: mostra qual provedor e chave foram lidos."""
    return jsonify({
        "ia_ativa": provedor_ativo is not None,
        "provedor": provedor_ativo,
        "modelo": MODEL_IA or (MODELOS_GROQ[0] if cliente_groq else (MODELOS_GEMINI[0] if cliente_gemini else None)),
        "groq_chave_lida": bool(CHAVE_GROQ),
        "gemini_chave_lida": bool(CHAVE_GEMINI),
        "env_encontrado": bool(_caminho_env),
=======
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
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        dados = request.get_json(silent=True) or {}
        mensagem = (dados.get("mensagem") or "").strip()

        if not mensagem:
<<<<<<< HEAD
            return jsonify({"erro": "Digite uma mensagem antes de enviar."}), 400

        if cliente_groq is None and cliente_gemini is None:
            return jsonify({"resposta": (
                "Ainda não configurei a chave da IA! É grátis e sem cartão: "
                "pegue em console.groq.com/keys, cole no .env como "
                "GROQ_API_KEY=sua_chave (sem aspas), reinicie o servidor e eu respondo."
=======
            return jsonify({"erro": "A mensagem está vazia."}), 400

        if cliente_groq is None and cliente_gemini is None:
            return jsonify({"resposta": (
                "Ainda não configurei a chave da IA! É de graça e não precisa de cartão. "
                "Recomendado: vá em console.groq.com/keys, crie sua chave, cole no .env "
                "em GROQ_API_KEY=sua_chave (sem aspas), reinicie o servidor e eu respondo!"
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
            )})

        if cliente_groq is not None:
            return chamar_groq(mensagem)
        return chamar_gemini(mensagem)

    except Exception as e:
        return classificar_erro(e)


if __name__ == "__main__":
    debug = os.getenv("DEBUG", "False").lower() == "true"
<<<<<<< HEAD
    print(f"[INFO] Provedor ativo: {provedor_ativo or 'NENHUM (sem chave)'}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=debug)
=======
    print(f"[INFO] Provedor de IA ativo: {provedor_ativo or 'NENHUM (sem chave)'}")
    print(f"[INFO] .env carregado de: {_caminho_env or 'não encontrado'}")
    app.run(host="0.0.0.0", port=5000, debug=debug)
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
