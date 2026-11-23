<<<<<<< HEAD
# ✦ Assistente IA — Site Completo e Responsivo

Site completo com **HTML + CSS + JavaScript + Python (Flask) + IA gratuita (Groq/Gemini)**,
interface polida, chat em tempo real e pronto para deploy no Render.

## ✨ Funcionalidades

- 🤖 **IA gratuita** — Groq (`openai/gpt-oss-20b`, mais rápido) como padrão; Gemini como alternativa
- 💬 **Chat em tempo real** — envio sem recarregar a página, indicador "digitando…"
- 🎨 **Interface premium** — hierarquia visual clara, espaçamento consistente, contraste legível, microinterações
- 📱 **100% responsivo** — adapta a celular, tablet e desktop
- 🏷️ **Chips de sugestão** — respostas rápidas com um clique
- 🩺 **Diagnóstico em `/api/status`** — mostra qual provedor/modelo está ativo
- 🛡️ **Erros tratados em português** — 401 (chave), 404 (modelo), 429 (limite), 503 (instável)
- 🔄 **Auto-fallback** — tenta vários modelos gratuitos automaticamente em caso de 404
- 🔒 **Chaves protegidas** — `.gitignore` evita enviar o `.env` ao GitHub

## 📁 Estrutura

```
site_ia_completo/
├── app.py               ← Backend Flask + IA (Groq padrão, Gemini alternativa)
├── requirements.txt     ← Pacotes instalados automaticamente
├── render.yaml          ← Deploy automático no Render
├── .env.example         ← Modelo de configuração (renomeie para .env)
├── .gitignore           ← Protege a chave secreta
├── static/
│   ├── estilos.css      ← Design responsivo premium
│   └── script.js        ← Chat, status, chips e indicador de digitação
└── templates/
    └── index.html       ← Estrutura da interface
```

## ⚙️ Como funciona (fluxo)

```
Usuário digita no chat
      ↓
JavaScript envia POST /api/chat
      ↓
Python (Flask) consulta a IA gratuita (Groq ou Gemini)
      ↓
Resposta volta em JSON e é exibida na tela (sem reload)
```

## 🧪 Rodar localmente

1. Instale o Python 3.10+
2. Renomeie `.env.example` para `.env`
3. Pegue uma chave grátis (sem cartão):
   - **Groq (recomendado):** https://console.groq.com/keys → *Create API Key*
   - **Gemini (alternativa):** https://aistudio.google.com/apikey
4. Cole no `.env`:
   ```env
   GROQ_API_KEY=gsk_sua_chave_aqui
   DEBUG=True
   ```
5. No terminal, dentro da pasta:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
6. Abra **http://localhost:5000** ✅
7. Diagnóstico: **http://localhost:5000/api/status** → deve mostrar `"ia_ativa": true`

> Sem chave o site abre normalmente; o chat explica como conseguir uma gratuita.

## 🐙 Enviar para o GitHub

```bash
git init
git add .
git commit -m "Site com IA completo"
git branch -M main
git remote add origin https://github.com/Raziekel/Site-com-ia.git
git push -u origin main
```

> Confira com `git status` que o `.env` **não** aparece na lista (o `.gitignore` cuida disso).

## 🚀 Deploy no Render (gratuíto)

1. Acesse https://render.com → **New → Web Service**
2. Conecte o repositório `Raziekel/Site-com-ia`
3. O `render.yaml` já sugere os comandos:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Em **Environment Variables**, adicione:
   - `GROQ_API_KEY` = sua chave
5. **Create Web Service** → em 2–5 minutos o site estará no ar 🎉

## 🐞 Troubleshooting rápido

| Mensagem no chat | Causa | Solução |
|---|---|---|
| Chave inválida (401) | Chave errada, com aspas/espaços, ou revogada | Crie nova em console.groq.com/keys; cole sem aspas |
| Modelo não disponível (404) | Modelo antigo descontinuado | O código tenta outros modelos; ou defina `MODEL_IA=openai/gpt-oss-20b` |
| Limite atingido (429) | Cota diária/minuta gratuita | Aguarde ~1 minuto e tente de novo |
| Instável (503) | Provedor sobrecarregado no momento | Tente novamente em instantes (há retry automático) |
| IA offline | `.env` não carregado | Confira que o arquivo se chama exatamente `.env`, na pasta do `app.py` |

## 🧩 Modelos gratuitos do Groq (2026)

- `openai/gpt-oss-20b` — mais rápido (padrão)
- `openai/gpt-oss-120b` — mais capaz
- `qwen/qwen3.8-27b` — alternativa

> Os modelos Llama 3.x migraram para o plano Enterprise/pago; por isso o pacote usa GPT-OSS e Qwen.
=======
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
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
