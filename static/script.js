// ============================================================
//  script.js — Interatividade do chat
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
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensagem: texto }),
        });

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
