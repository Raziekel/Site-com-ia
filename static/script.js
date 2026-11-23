// ============================================================
//  script.js — Interatividade do chat
<<<<<<< HEAD
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
=======
//  Como funciona: quando o usuário envia o formulário, o JS
//  manda a mensagem para o backend (POST /api/chat) e mostra
//  a resposta na tela sem recarregar a página.
// ============================================================

const formChat = document.getElementById("form-chat");
const entradaMensagem = document.getElementById("entrada-mensagem");
const caixaMensagens = document.getElementById("caixa-mensagens");
const status = document.getElementById("status");
const botaoEnviar = formChat.querySelector("button");

formChat.addEventListener("submit", async (evento) => {
    evento.preventDefault(); // evita que a página recarregue

    const texto = entradaMensagem.value.trim();
    if (!texto) return;

    // 1) Mostra a mensagem do usuário na tela
    adicionarMensagem(texto, "usuario");
    entradaMensagem.value = "";

    // 2) Bloqueia o envio enquanto espera a resposta
    entradaMensagem.disabled = true;
    botaoEnviar.disabled = true;
    status.textContent = "A IA está pensando...";

    try {
        // 3) Envia para o servidor Python (Flask)
        const resposta = await fetch("/api/chat", {
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensagem: texto }),
        });
<<<<<<< HEAD
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
=======

        const dados = await resposta.json();

        // 4) Mostra a resposta da IA (ou o erro)
        if (dados.erro) {
            adicionarMensagem("Ops! " + dados.erro, "ia");
        } else {
            adicionarMensagem(dados.resposta, "ia");
        }
    } catch (erro) {
        adicionarMensagem("Erro de conexão: " + erro.message, "ia");
    } finally {
        // 5) Libera o envio novamente
        entradaMensagem.disabled = false;
        botaoEnviar.disabled = false;
        status.textContent = "";
        entradaMensagem.focus();
    }
});

// Cria um balão de mensagem e rola a tela para o final
function adicionarMensagem(texto, remetente) {
    const div = document.createElement("div");
    div.className = "mensagem " + remetente;
    div.textContent = texto;
    caixaMensagens.appendChild(div);
    caixaMensagens.scrollTop = caixaMensagens.scrollHeight;
}
>>>>>>> 6dcad058ffd7e4eb44b81e7db6b5098fb84f2aeb
