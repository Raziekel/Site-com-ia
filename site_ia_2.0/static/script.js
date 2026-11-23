// ============================================================
//  script.js — Interatividade do chat
//  Status da IA, envio com fetch, indicador de digitação,
//  chips de sugestão, auto-rolagem e estados de carregamento.
// ============================================================

const form = document.getElementById("form-chat");
const input = document.getElementById("entrada-mensagem");
const box = document.getElementById("caixa-mensagens");
const statusTexto = document.getElementById("status-texto");
const pill = document.getElementById("status-pill");
const meta = document.getElementById("chat-meta");
const modelTag = document.getElementById("model-tag");
const btn = document.getElementById("btn-enviar");

// ---------- Status da IA na barra superior ----------
async function atualizarStatus() {
    try {
        const resp = await fetch("/api/status");
        const dados = await resp.json();

        if (dados.ia_ativa) {
            pill.className = "pill pill-online";
            pill.textContent = "IA online";
            meta.textContent = "conectado via " + (dados.provedor || "IA");
            modelTag.textContent = dados.modelo || "modelo gratuito";
        } else {
            pill.className = "pill pill-offline";
            pill.textContent = "IA offline (configure a chave)";
            meta.textContent = "aguardando a chave da IA";
            modelTag.textContent = "sem modelo ativo";
        }
    } catch {
        pill.className = "pill pill-offline";
        pill.textContent = "sem conexão com o servidor";
    }
}

atualizarStatus();

// ---------- Bolhas de mensagem ----------
function criarBolso(tipo, texto, avatarEmoji) {
    const wrap = document.createElement("div");
    wrap.className = "bubble " + tipo;

    const avatar = document.createElement("span");
    avatar.className = "avatar";
    avatar.textContent = avatarEmoji;

    const corpo = document.createElement("div");
    corpo.className = "bubble-body";
    corpo.textContent = texto;

    wrap.appendChild(avatar);
    wrap.appendChild(corpo);
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
}

function mostrarDigitando() {
    const wrap = document.createElement("div");
    wrap.className = "bubble ia";
    wrap.id = "digitando";
    wrap.innerHTML =
        '<span class="avatar">🤖</span>' +
        '<div class="bubble-body typing"><span></span><span></span><span></span></div>';
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
}

function removerDigitando() {
    const el = document.getElementById("digitando");
    if (el) el.remove();
}

// ---------- Envio do formulário ----------
form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const texto = input.value.trim();
    if (!texto) return;

    criarBolso("usuario", texto, "🧑");
    input.value = "";
    input.disabled = true;
    btn.disabled = true;
    statusTexto.textContent = "A IA está pensando…";
    mostrarDigitando();

    try {
        const resp = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensagem: texto }),
        });
        const dados = await resp.json();
        removerDigitando();

        if (dados.erro) {
            criarBolso("erro", dados.erro, "⚠️");
        } else {
            criarBolso("ia", dados.resposta, "🤖");
            if (dados.modelo) modelTag.textContent = dados.modelo;
        }
    } catch (erro) {
        removerDigitando();
        criarBolso("erro", "Não foi possível falar com o servidor: " + erro.message, "⚠️");
    } finally {
        input.disabled = false;
        btn.disabled = false;
        statusTexto.textContent = "";
        input.focus();
    }
});

// ---------- Chips de sugestão ----------
document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
        input.value = chip.dataset.prompt;
        form.requestSubmit();
    });
});
