
import streamlit as st
import hashlib
import os
import json
from util import salvar_sistema, carregar_sistema
from admin import modo_administrador
from staff import modo_staff
from jogador import modo_jogador
from espirito import modo_capitao

ARQUIVO_JSON = "sistema_salvo.json"

# ===== Funções auxiliares =====
def gerar_md5(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def obter_credenciais():
    lista_de_usuarios = []
    if not os.path.exists("credenciais.txt"):
        return lista_de_usuarios

    with open("credenciais.txt", "r") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(":")
            if partes[0] == "staff" and len(partes) == 4:
                tipo, login, senha, torneio = partes
                lista_de_usuarios.append({"tipo": tipo, "login": login, "senha": senha, "torneio": torneio})
            elif partes[0] == "admin" and len(partes) == 3:
                tipo, login, senha = partes
                lista_de_usuarios.append({"tipo": tipo, "login": login, "senha": senha})
            elif partes[0] == "jogador" and len(partes) == 3:
                tipo, login, senha = partes
                lista_de_usuarios.append({"tipo": tipo, "login": login, "senha": senha})
            elif partes[0] == "capitão" and len(partes) == 4:
                tipo, login, senha, torneio = partes
                lista_de_usuarios.append({"tipo": tipo, "login": login, "senha": senha, "torneio": torneio})
    return lista_de_usuarios

# ===== Streamlit config =====
st.set_page_config(page_title="Sistema de Torneio", layout="wide")
sistema = carregar_sistema(ARQUIVO_JSON)

if "usuario_logado" in st.session_state:
    usuario = st.session_state["usuario_logado"]
    tipo = usuario["tipo"]
    login = usuario["login"]


    if tipo == "admin":
        modo_administrador(sistema, ARQUIVO_JSON, login)
    elif tipo == "staff":
        sistema["torneio_ativo"] = usuario["torneio"]
        modo_staff(sistema, ARQUIVO_JSON, login)
    elif tipo == "jogador":
        modo_jogador(sistema)
    elif tipo == "capitão":
        sistema["torneio_ativo"] = usuario["torneio"]
        modo_capitao(sistema, ARQUIVO_JSON, login)

    salvar_sistema(sistema, ARQUIVO_JSON)

else:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.title("🎮 Acesso")
        opcao = st.radio("Escolha uma opção:", ["Login", "Registrar", "Sair"])

    with col2:
        if opcao == "Login":
            st.header("🔐 Login")
            login = st.text_input("Login")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                usuarios = obter_credenciais()
                senha_md5 = gerar_md5(senha)
                for usuario in usuarios:
                    if usuario["login"] == login and usuario["senha"] == senha_md5:
                        st.session_state["usuario_logado"] = usuario
                        st.rerun()
                st.error("Login ou senha incorretos.")

        elif opcao == "Registrar":
            st.header("📝 Registrar novo jogador")
            novo_login = st.text_input("Novo login")
            nova_senha = st.text_input("Nova senha", type="password")
            if st.button("Registrar"):
                usuarios = obter_credenciais()
                if any(user["login"] == novo_login for user in usuarios):
                    st.error("Login já existe. Escolha outro.")
                else:
                    senha_md5 = gerar_md5(nova_senha)
                    with open("credenciais.txt", "a") as f:
                        f.write(f"jogador:{novo_login}:{senha_md5}\n")
                    st.success("Jogador registrado com sucesso!")

        elif opcao == "Sair":
            st.info("Saindo do sistema... Feche a aba se desejar encerrar.")
