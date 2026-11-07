# 🚀 Site com IA GRATUITA — Versão Final (Groq como padrão)

Site completo: **HTML + CSS + JavaScript + Python (Flask) + IA gratuita**.
**Groq (Llama)** é o provedor padrão — rápido, estável e não sobrecarrega. O **Google Gemini** fica como alternativa automática.

## ✅ Provedores gratuitos (sem cartão de crédito)

| Provedor | Onde pegar a chave | Modelo padrão |
|---|---|---|
| ⚡ **Groq** (recomendado) | https://console.groq.com/keys | openai/gpt-oss-20b |
| 🔷 Google Gemini | https://aistudio.google.com/apikey | gemini-3.8-flash |

O código detecta automaticamente qual chave você configurou. Se colocar as duas, usa o Groq.

## 🔑 Passo a passo

1. Pegue uma chave grátis em **console.groq.com/keys** → Create API Key → copie
2. Renomeie `.env.example` → **`.env`** (no Windows: ative "Mostrar extensões de arquivo" para não virar `.env.txt`)
3. Cole no `.env`:
   ```env
   GROQ_API_KEY=sua_chave_aqui
   DEBUG=True
   ```
   ❌ Sem aspas, sem espaços ao redor de `=`, uma linha só.
4. Rode:
   ```powershell
   pip install -r requirements.txt
   python app.py
   ```
5. Acesse **http://localhost:5000** ✅
6. Confirme em **http://localhost:5000/api/status** → `"groq_chave_lida": true`

## 🛡️ Tratamento de erros (em português)

- **401** (chave inválida) → explica passo a passo como criar uma chave nova
- **429** (limite) → pede para aguardar 1 minuto
- **503** (instabilidade) → retry automático (3 tentativas) + mensagem amigável
- **Modelo não encontrado** → sugere definir `MODEL_IA` no `.env`

## 🌐 Deploy no Render

Suba para o GitHub → **render.com → New → Web Service** → adicione `GROQ_API_KEY` nas Environment Variables → Create. Em 2–5 min está no ar! 🎉
