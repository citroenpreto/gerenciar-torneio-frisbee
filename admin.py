import streamlit as st
from util import salvar_sistema
import os
import hashlib

def gerar_md5(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def modo_administrador(sistema, ARQUIVO_JSON, usuario_logado):
    menu_admin = [
        "Criar torneio", "Remover torneio", "Acessar torneio",
        "Criar time", "Modificar time", "Adicionar jogador", "Remover jogador",
        "Ver informações dos times", "Registrar pontuação do jogo", "Remover ponto do jogo",
        "Ver estatísticas do jogo", "Definir confrontos", "Alterar confronto",
        "Remover confronto", "Mostrar confrontos", "Registrar novo staff",
        "Remover staff", "Estatísticas do torneio", "Registrar novo capitão",
        "Remover capitão"
    ]

    # === SIDEBAR ===
    with st.sidebar:
        st.success(f"Logado como: {usuario_logado} (admin)")
        escolha = st.radio("📋 Menu do Administrador", menu_admin, key="menu_admin")

        # espaço para empurrar o botão pra baixo
        for _ in range(20):
            st.write("")

        if st.button("Sair", key="botao_sair_admin"):
            st.session_state.pop("usuario_logado")
            st.rerun()

    # === ÁREA CENTRAL ===
    col_esq, col_dir = st.columns([4, 1])  # direita menor, ideal pra info leve

    with col_esq:
        st.title("👤 Painel do Administrador")
        st.write(f"Bem-vindo, {usuario_logado}!")

    with col_dir:
        torneio_ativo_atual = sistema.get("torneio_ativo")
        if torneio_ativo_atual:
            st.info(f"🏆 Torneio ativo:\n\n**{torneio_ativo_atual}**")
        else:
            st.warning("⚠️ Nenhum torneio ativo")

    # === FUNÇÕES ===
    if escolha == "Criar torneio":
        nome = st.text_input("📛 Nome do novo torneio").upper()
        if st.button("Criar torneio", key="criar_torneio"):
            if nome in sistema["torneio"]:
                st.warning("Esse torneio já existe.")
            else:
                sistema["torneio"][nome] = {"times": {}, "confrontos": {}}
                salvar_sistema(sistema, ARQUIVO_JSON)
                st.success(f"Torneio '{nome}' criado com sucesso!")

    elif escolha == "Remover torneio":
        torneios = list(sistema["torneio"].keys())
        if not torneios:
            st.warning("Nenhum torneio cadastrado.")
        else:
            torneio_remover = st.selectbox("Selecione o torneio a remover", torneios)
            if st.button("Remover torneio", key="remover_torneio"):
                del sistema["torneio"][torneio_remover]
                salvar_sistema(sistema, ARQUIVO_JSON)
                st.success(f"Torneio '{torneio_remover}' removido com sucesso!")

    elif escolha == "Acessar torneio":
    
        torneio_ativo(sistema)
        salvar_sistema(sistema, ARQUIVO_JSON)

    elif escolha == "Criar time":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo selecionado.")
        else:
            nome_time = st.text_input("🏷️ Nome do novo time").upper()
            if st.button("Criar time"):
                if nome_time in sistema["torneio"][torneio_atual]["times"]:
                    st.warning("⚠️ Esse time já existe.")
                else:
                    sistema["torneio"][torneio_atual]["times"][nome_time] = {
                        "pontos": 0,
                        "jogadores": {}
                    }
                    salvar_sistema(sistema, ARQUIVO_JSON)
                    st.success(f"✅ Time '{nome_time}' criado com sucesso!")

    elif escolha == "Modificar time":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo selecionado.")
        else:
            times = list(sistema["torneio"][torneio_atual]["times"].keys())
            if not times:
                st.info("Nenhum time cadastrado.")
            else:
                time_escolhido = st.selectbox("Selecione um time:", times)
                acao = st.radio("O que deseja fazer?", ["Renomear", "Deletar"])
                if acao == "Renomear":
                    novo_nome = st.text_input("Novo nome do time").upper()
                    if st.button("Renomear time"):
                        if novo_nome in times:
                            st.warning("Esse nome já existe.")
                        else:
                            sistema["torneio"][torneio_atual]["times"][novo_nome] = sistema["torneio"][torneio_atual]["times"].pop(time_escolhido)
                            salvar_sistema(sistema, ARQUIVO_JSON)
                            st.success(f"✅ Time '{time_escolhido}' renomeado para '{novo_nome}'.")
                else:
                    if st.button("Deletar time"):
                        del sistema["torneio"][torneio_atual]["times"][time_escolhido]
                        salvar_sistema(sistema, ARQUIVO_JSON)
                        st.success(f"🗑️ Time '{time_escolhido}' deletado com sucesso.")

    elif escolha == "Adicionar jogador":
            torneio_atual = sistema.get("torneio_ativo")
            if not torneio_atual:
                st.warning("⚠️ Nenhum torneio ativo selecionado.")
            else:
                times = list(sistema["torneio"][torneio_atual]["times"].keys())
                if not times:
                    st.info("Nenhum time cadastrado.")
                else:
                    time_escolhido = st.selectbox("Selecione o time:", times)
                    nome_jogador = st.text_input("Nome do jogador").upper()
                    if st.button("Adicionar jogador"):
                        sistema["torneio"][torneio_atual]["times"][time_escolhido]["jogadores"][nome_jogador] = {"gols": 0, "assistencias": 0}
                        salvar_sistema(sistema, ARQUIVO_JSON)
                        st.success(f"✅ Jogador '{nome_jogador}' adicionado ao time '{time_escolhido}'.")           

    elif escolha == "Remover jogador":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo selecionado.")
        else:
            times = list(sistema["torneio"][torneio_atual]["times"].keys())
            if not times:
                st.info("Nenhum time cadastrado.")
            else:
                time_escolhido = st.selectbox("Selecione o time:", times)
                jogadores = list(sistema["torneio"][torneio_atual]["times"][time_escolhido]["jogadores"].keys())
                if not jogadores:
                    st.info("Nenhum jogador cadastrado nesse time.")
                else:
                    jogador_escolhido = st.selectbox("Selecione o jogador:", jogadores)
                    if st.button("Remover jogador"):
                        del sistema["torneio"][torneio_atual]["times"][time_escolhido]["jogadores"][jogador_escolhido]
                        salvar_sistema(sistema, ARQUIVO_JSON)
                        st.success(f"✅ Jogador '{jogador_escolhido}' removido do time '{time_escolhido}'.")

    elif escolha == "Ver informações dos times":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio está ativo.")
        else:
            times = sistema["torneio"][torneio_atual]["times"]
            if not times:
                st.warning("⚠️ Nenhum time foi criado ainda.")
            else:
                st.subheader("📋 Informações dos times")
                colunas = st.columns(3)  # Cria 3 colunas lado a lado
                for i, (nome_time, dados) in enumerate(times.items()):
                    with colunas[i % 3]:
                        st.markdown(f"🏷️ **{nome_time}**")
                        jogadores = dados["jogadores"]
                        if jogadores:
                            for nome in jogadores:
                                st.markdown(
                                    f"<div style='margin-bottom: -8px;'>- {nome}</div>",
                                    unsafe_allow_html=True
                                )
                        else:
                            st.markdown("<i>Sem jogadores</i>", unsafe_allow_html=True)

    elif escolha == "Registrar pontuação do jogo":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo.")
        else:
            times = sistema["torneio"][torneio_atual]["times"]
            time = st.selectbox("🏷️ Time que fez o gol:", list(times.keys()))

            if time:
                jogadores_disponiveis = list(times[time]["jogadores"].keys())
                jogador_gol = st.selectbox("⚽ Jogador que marcou o gol:", jogadores_disponiveis)
                jogador_assist = st.selectbox("🎯 Jogador que fez a assistência:", jogadores_disponiveis)

                if st.button("Registrar ponto"):
                    times[time]["pontos"] += 1
                    times[time]["jogadores"][jogador_gol]["gols"] += 1
                    times[time]["jogadores"][jogador_assist]["assistencias"] += 1
                    salvar_sistema(sistema, ARQUIVO_JSON)
                    st.success(f"Gol do {time}! {jogador_gol} marcou e {jogador_assist} deu a assistência.")

    elif escolha == "Remover ponto do jogo":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo.")
        else:
            times = sistema["torneio"][torneio_atual]["times"]
            time = st.selectbox("🏷️ Time que vai perder o ponto:", list(times.keys()))

            if time:
                jogadores_estat = times[time]["jogadores"]

                jogadores_com_gol = [j for j, stats in jogadores_estat.items() if stats["gols"] > 0]
                jogadores_com_assist = [j for j, stats in jogadores_estat.items() if stats["assistencias"] > 0]

                if not jogadores_com_gol and not jogadores_com_assist:
                    st.warning("⚠️ Nenhum jogador com gols ou assistências para remover.")
                    return

                jogador_gol = st.selectbox("❌ Jogador que vai perder o gol:", jogadores_com_gol) if jogadores_com_gol else None
                jogador_assist = st.selectbox("❌ Jogador que vai perder a assistência:", jogadores_com_assist) if jogadores_com_assist else None

                if st.button("Remover ponto"):
                    if times[time]["pontos"] > 0:
                        times[time]["pontos"] -= 1
                    if jogador_gol and jogadores_estat[jogador_gol]["gols"] > 0:
                        jogadores_estat[jogador_gol]["gols"] -= 1
                    if jogador_assist and jogadores_estat[jogador_assist]["assistencias"] > 0:
                        jogadores_estat[jogador_assist]["assistencias"] -= 1
                    salvar_sistema(sistema, ARQUIVO_JSON)
                    st.success(f"✅ Ponto removido do {time}.")


    elif escolha == "Ver estatísticas do jogo":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio está ativo.")
        else:
            times = sistema["torneio"][torneio_atual]["times"]
            if not times:
                st.warning("⚠️ Nenhum time foi criado.")
            else:
                st.subheader("📊 Informações dos times")

                # Agrupa os times em grupos de 3
                times_lista = list(times.items())
                for i in range(0, len(times_lista), 3):
                    grupo = times_lista[i:i+3]
                    colunas = st.columns(len(grupo))

                    for col, (nome_time, dados) in zip(colunas, grupo):
                        with col:
                            st.markdown(f"### 🏷️ {nome_time}")
                            st.markdown(f"<span style='font-size: 13px;'>Pontos: {dados['pontos']}</span>", unsafe_allow_html=True)

                            for nome_jogador, estat in dados["jogadores"].items():
                                linha = f"""
                                <div style="margin-bottom: 4px;">
                                    <span style='font-weight:bold;'>{nome_jogador}</span>
                                    <span style='font-size:12px;'> – ⚽ {estat['gols']} | 🎯 {estat['assistencias']}</span>
                                </div>
                                """
                                st.markdown(linha, unsafe_allow_html=True)

    elif escolha == "Alterar confronto":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo.")
        else:
            confrontos = sistema["torneio"][torneio_atual]["confrontos"]
            times = sistema["torneio"][torneio_atual]["times"]
            if not confrontos:
                st.warning("⚠️ Nenhum confronto cadastrado.")
            else:
                jogo_sel = st.selectbox("Escolha o confronto para alterar:", list(confrontos.keys()))
                dados = confrontos[jogo_sel]

                novo_time1 = st.text_input("Novo Time 1", value=dados["time1"]).upper()
                novo_time2 = st.text_input("Novo Time 2", value=dados["time2"]).upper()
                novo_horario = st.text_input("Novo horário", value=dados["horario"])
                novo_local = st.text_input("Novo local", value=dados["local"])

                if st.button("Salvar alterações"):
                    if novo_time1 not in times or novo_time2 not in times:
                        st.error("❌ Um dos times não existe.")
                    else:
                        dados["time1"] = novo_time1
                        dados["time2"] = novo_time2
                        dados["horario"] = novo_horario
                        dados["local"] = novo_local
                        salvar_sistema(sistema, ARQUIVO_JSON)
                        st.success(f"✅ Confronto '{jogo_sel}' alterado com sucesso!")

    elif escolha == "Remover confronto":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo.")
        else:
            confrontos = sistema["torneio"][torneio_atual]["confrontos"]
            if not confrontos:
                st.warning("⚠️ Nenhum confronto cadastrado.")
            else:
                jogo_sel = st.selectbox("Escolha o confronto para remover:", list(confrontos.keys()))
                if st.button("Remover confronto"):
                    confronto = confrontos[jogo_sel]
                    time1 = confronto.get("time1")
                    time2 = confronto.get("time2")
                    times = sistema["torneio"][torneio_atual]["times"]

                    # 🧼 Zerar estatísticas dos jogadores e pontos dos times
                    for time_nome in [time1, time2]:
                        if time_nome in times:
                            time = times[time_nome]
                            time["pontos"] = 0
                            for jogador in time["jogadores"].values():
                                jogador["gols"] = 0
                                jogador["assistencias"] = 0

                    # ❌ Remover o confronto
                    del confrontos[jogo_sel]
                    salvar_sistema(sistema, ARQUIVO_JSON)
                    st.success(f"🗑️ Confronto '{jogo_sel}' removido com sucesso, incluindo os dados estatísticos.")

    elif escolha == "Mostrar confrontos":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo.")
        else:
            confrontos = sistema["torneio"][torneio_atual]["confrontos"]
            if not confrontos:
                st.warning("⚠️ Nenhum confronto cadastrado.")
            else:
                st.subheader("📋 Confrontos cadastrados:")
                for numero_jogo, dados in confrontos.items():
                    time1 = dados["time1"]
                    time2 = dados["time2"]
                    horario = dados["horario"]
                    local = dados["local"]

                    if dados.get("finalizado"):
                        placar1 = dados.get("placar1", 0)
                        placar2 = dados.get("placar2", 0)
                        vencedor = dados.get("vencedor")
                        resultado = f"🏁 FINALIZADO — {time1} {placar1} 🆚 {placar2} {time2}"
                        if vencedor:
                            resultado += f" 🏆 Vencedor: **{vencedor}**"
                        else:
                            resultado += " 🤝 Empate"
                    else:
                        resultado = f"{time1} 🆚 {time2}"

                    st.markdown(f"📅 **{numero_jogo}** — {resultado}  ⏰ {horario} 📍 {local}")

    elif escolha == "Registrar novo staff":
        login = st.text_input("Login do staff:")
        senha = st.text_input("Senha do staff:", type="password")

        torneios_disponiveis = list(sistema["torneio"].keys())
        if torneios_disponiveis:
            torneio = st.selectbox("Torneio vinculado:", torneios_disponiveis)
        else:
            st.warning("⚠️ Nenhum torneio cadastrado.")
            torneio = None

        if st.button("Registrar staff") and torneio:
            senha_md5 = gerar_md5(senha)
            with open("credenciais.txt", "a") as arquivo:
                arquivo.write(f"staff:{login}:{senha_md5}:{torneio}\n")
            st.success(f"✅ Staff '{login}' registrado para o torneio '{torneio}'.")

    elif escolha == "Remover staff":
        if not os.path.exists("credenciais.txt"):
            st.warning("⚠️ Arquivo de credenciais não encontrado.")
        else:
            with open("credenciais.txt", "r") as f:
                linhas = f.readlines()
            
            # Filtra apenas os usuários do tipo 'staff'
            logins_staff = [linha.split(":")[1] for linha in linhas if linha.startswith("staff:")]

            if not logins_staff:
                st.info("ℹ️ Nenhum staff cadastrado.")
            else:
                login = st.selectbox("👤 Selecione o staff para remover:", logins_staff)

                if st.button("Remover staff"):
                    novas_linhas = [l for l in linhas if not l.startswith(f"staff:{login}:")]
                    with open("credenciais.txt", "w") as f:
                        f.writelines(novas_linhas)
                    st.success(f"🗑️ Staff '{login}' removido com sucesso.")

    elif escolha == "Registrar novo capitão":
        login = st.text_input("Login do capitão:")
        senha = st.text_input("Senha do capitão:", type="password")

        torneios_disponiveis = list(sistema["torneio"].keys())
        if torneios_disponiveis:
            torneio = st.selectbox("Torneio vinculado:", torneios_disponiveis)
        else:
            st.warning("⚠️ Nenhum torneio cadastrado.")
            torneio = None

        if st.button("Registrar capitão") and torneio:
            senha_md5 = gerar_md5(senha)
            with open("credenciais.txt", "a") as arquivo:
                arquivo.write(f"capitão:{login}:{senha_md5}:{torneio}\n")
            st.success(f"✅ Capitão '{login}' registrado para o torneio '{torneio}'.")

    elif escolha == "Remover capitão":
        if not os.path.exists("credenciais.txt"):
            st.warning("⚠️ Arquivo de credenciais não encontrado.")
        else:
            with open("credenciais.txt", "r") as f:
                linhas = f.readlines()

            logins_capitao = [linha.split(":")[1] for linha in linhas if linha.startswith("capitão:")]

            if not logins_capitao:
                st.info("ℹ️ Nenhum capitão cadastrado.")
            else:
                login = st.selectbox("👤 Selecione o capitão para remover:", logins_capitao)

                if st.button("Remover capitão"):
                    novas_linhas = [l for l in linhas if not l.startswith(f"capitão:{login}:")]
                    with open("credenciais.txt", "w") as f:
                        f.writelines(novas_linhas)
                    st.success(f"🗑️ Capitão '{login}' removido com sucesso.")

    elif escolha == "Definir confrontos":
        torneio_atual = sistema.get("torneio_ativo")
        if not torneio_atual:
            st.warning("⚠️ Nenhum torneio ativo.")
        else:
            times = sistema["torneio"][torneio_atual]["times"]
            confrontos = sistema["torneio"][torneio_atual]["confrontos"]

            st.subheader("📋 Confrontos já cadastrados:")
            if confrontos:
                for numero_jogo, dados in confrontos.items():
                    st.markdown(f"📅 **{numero_jogo}**")
            else:
                st.info("Nenhum confronto cadastrado ainda.")

            numero_jogo = st.text_input("Número do jogo (ex: JOGO 1)").upper()
            if numero_jogo in confrontos:
                st.warning("⚠️ Este jogo já está cadastrado!")
            else:
                time1 = st.selectbox("Selecione o Time 1", list(times.keys()), key="definir_time1")
                time2 = st.selectbox("Selecione o Time 2", list(times.keys()), key="definir_time2")
                horario = st.text_input("⏰ Horário do jogo (ex: 10:00)")
                local = st.text_input("📍 Local do jogo")

                if st.button("Cadastrar confronto"):
                    if time1 == time2:
                        st.warning("❌ Os times devem ser diferentes.")
                    else:
                        confrontos[numero_jogo] = {
                            "time1": time1,
                            "time2": time2,
                            "horario": horario,
                            "local": local
                        }
                        salvar_sistema(sistema, ARQUIVO_JSON)
                        st.success(f"✅ {numero_jogo}: {time1} VS {time2} - {horario} no {local} cadastrado com sucesso!")

def torneio_ativo(sistema):
    st.subheader("🎯 Selecionar Torneio Ativo")

    if not sistema["torneio"]:
        st.warning("⚠️ Nenhum torneio foi criado ainda.")
        return

    opcoes = list(sistema["torneio"].keys())
    torneio_escolhido = st.selectbox("📋 Torneios disponíveis:", opcoes, key="torneio_ativo")

    if st.button("Selecionar torneio", key="selecionar_torneio"):
        sistema["torneio_ativo"] = torneio_escolhido
        st.success(f"✅ Torneio '{torneio_escolhido}' foi selecionado como ativo!")

def criar_time(sistema):
    torneio_atual = sistema.get("torneio_ativo")

    if not torneio_atual:
        st.warning("⚠️ Nenhum torneio está ativo. Acesse um torneio primeiro.")
        return

    nome_time = st.text_input("🏷️ Nome do novo time").upper()

    if st.button("Criar time"):
        if nome_time in sistema["torneio"][torneio_atual]["times"]:
            st.warning("⚠️ Esse time já existe.")
        else:
            sistema["torneio"][torneio_atual]["times"][nome_time] = {
                "pontos": 0,
                "jogadores": {}
            }
            st.success(f"✅ Time ⚽ {nome_time} criado com sucesso!")

def modificar_time(sistema):
    torneio_atual = sistema.get("torneio_ativo")

    if not torneio_atual:
        st.warning("⚠️ Nenhum torneio está ativo.")
        return

    times = list(sistema["torneio"][torneio_atual]["times"].keys())
    if not times:
        st.warning("⚠️ Nenhum time cadastrado.")
        return

    nome_time = st.selectbox("✏️ Selecione o time a ser modificado:", times)
    acao = st.radio("Deseja deletar ou renomear o time?", ["Deletar", "Renomear"])

    if acao == "Deletar":
        if st.button("Deletar time"):
            del sistema["torneio"][torneio_atual]["times"][nome_time]
            st.success(f"🗑️ Time '{nome_time}' deletado com sucesso.")

    elif acao == "Renomear":
        novo_nome = st.text_input("🆕 Novo nome do time:").upper()
        if st.button("Renomear time"):
            if novo_nome in sistema["torneio"][torneio_atual]["times"]:
                st.warning(f"⚠️ O time '{novo_nome}' já existe. Escolha outro nome.")
            else:
                sistema["torneio"][torneio_atual]["times"][novo_nome] = sistema["torneio"][torneio_atual]["times"].pop(nome_time)
                st.success(f"✏️ Time '{nome_time}' renomeado para '{novo_nome}'.")

def adicionar_jogador(sistema):
    torneio_atual = sistema.get("torneio_ativo")

    if not torneio_atual:
        st.warning("⚠️ Nenhum torneio está ativo.")
        return

    times = list(sistema["torneio"][torneio_atual]["times"].keys())
    if not times:
        st.warning("⚠️ Nenhum time cadastrado.")
        return

    nome_time = st.selectbox("🏷️ Escolha o time:", times)
    nome_jogador = st.text_input("👤 Nome do jogador a adicionar:").upper()

    if st.button("Adicionar jogador"):
        sistema["torneio"][torneio_atual]["times"][nome_time]["jogadores"][nome_jogador] = {
            "gols": 0,
            "assistencias": 0
        }
        st.success(f"✅ Jogador '{nome_jogador}' adicionado ao time '{nome_time}'.")

def remover_jogador(sistema):
    torneio_atual = sistema.get("torneio_ativo")

    if not torneio_atual:
        st.warning("⚠️ Nenhum torneio está ativo.")
        return

    times = list(sistema["torneio"][torneio_atual]["times"].keys())
    if not times:
        st.warning("⚠️ Nenhum time cadastrado.")
        return

    nome_time = st.selectbox("🏷️ Escolha o time:", times)
    jogadores = list(sistema["torneio"][torneio_atual]["times"][nome_time]["jogadores"].keys())

    if not jogadores:
        st.warning("⚠️ Nenhum jogador nesse time.")
        return

    nome_jogador = st.selectbox("👤 Escolha o jogador para remover:", jogadores)

    if st.button("Remover jogador"):
        del sistema["torneio"][torneio_atual]["times"][nome_time]["jogadores"][nome_jogador]
        st.success(f"✅ Jogador '{nome_jogador}' removido do time '{nome_time}'.")

def informacoes_times(sistema):
    torneio_atual = sistema.get("torneio_ativo")

    if not torneio_atual:
        st.warning("⚠️ Nenhum torneio está ativo. Acesse um torneio primeiro.")
        return

    times = sistema["torneio"][torneio_atual]["times"]

    if not times:
        st.warning("⚠️ Nenhum time foi criado ainda.")
        return

    st.subheader("📋 Informações dos times")

    nomes_times = list(times.keys())
    num_por_linha = 3  # Você pode ajustar esse número

    for i in range(0, len(nomes_times), num_por_linha):
        cols = st.columns(num_por_linha)
        for idx, nome_time in enumerate(nomes_times[i:i+num_por_linha]):
            with cols[idx]:
                st.markdown(f"#### ⚽ {nome_time}")
                jogadores = times[nome_time]["jogadores"]
                if jogadores:
                    for nome_jogador in jogadores:
                        st.markdown(f"- {nome_jogador}")
                else:
                    st.markdown("*Sem jogadores cadastrados*")

def pontuacao_jogo(sistema):
    torneio_atual = sistema["torneio_ativo"]
    times = sistema["torneio"][torneio_atual]["times"]

    st.subheader("⚽ Registrar Pontuação do Jogo")

    nome_time = st.selectbox("Selecione o time que fez o gol:", list(times.keys()), key="pontuacao_time")

    jogadores = list(times[nome_time]["jogadores"].keys())
    if not jogadores:
        st.warning("⚠️ Nenhum jogador nesse time.")
        return

    gol_jogador = st.selectbox("Quem fez o gol?", jogadores, key="gol_jogador")
    assis_jogador = st.selectbox("Quem fez a assistência?", jogadores, key="assist_jogador")

    if st.button("Registrar Gol", key="registrar_gol"):
        times[nome_time]["pontos"] += 1
        times[nome_time]["jogadores"][gol_jogador]["gols"] += 1
        times[nome_time]["jogadores"][assis_jogador]["assistencias"] += 1
        st.success(f"Gol do {nome_time}! {gol_jogador} marcou e {assis_jogador} deu a assistência.")

def remover_pontos(sistema):
    torneio_atual = sistema["torneio_ativo"]
    times = sistema["torneio"][torneio_atual]["times"]

    st.subheader("🛑 Remover Pontuação")
    nome_time = st.selectbox("Selecione o time:", list(times.keys()), key="remover_time")
    jogadores = list(times[nome_time]["jogadores"].keys())

    if not jogadores:
        st.warning("⚠️ Nenhum jogador nesse time.")
        return

    gol_jogador = st.selectbox("Quem teve o gol removido?", jogadores, key="remover_gol")
    assis_jogador = st.selectbox("Quem teve a assistência removida?", jogadores, key="remover_assist")

    if st.button("Remover Ponto", key="remover_ponto"):
        time_data = times[nome_time]

        if time_data["pontos"] > 0:
            time_data["pontos"] -= 1
        if time_data["jogadores"][gol_jogador]["gols"] > 0:
            time_data["jogadores"][gol_jogador]["gols"] -= 1
        if time_data["jogadores"][assis_jogador]["assistencias"] > 0:
            time_data["jogadores"][assis_jogador]["assistencias"] -= 1

        st.success(f"Ponto removido do {nome_time}. {gol_jogador} perdeu um gol e {assis_jogador} perdeu uma assistência.")

def informacoes_jogo(sistema):
    torneio_atual = sistema.get("torneio_ativo")
    if not torneio_atual:
        st.warning("⚠️ Nenhum torneio está ativo.")
        return

    times = sistema["torneio"][torneio_atual]["times"]
    if not times:
        st.warning("⚠️ Nenhum time foi criado ainda.")
        return

    st.subheader("📊 Estatísticas dos Times")
    colunas = st.columns(3)
    for idx, (nome_time, dados) in enumerate(times.items()):
        with colunas[idx % 3]:
            st.markdown(f"### 🏷️ {nome_time}")
            st.markdown(f"**Pontos:** {dados['pontos']}")
            for nome_jogador, estat in dados["jogadores"].items():
                st.write(f"👤 {nome_jogador}")
                st.write(f"⚽ Gols: {estat['gols']} | 🎯 Assistências: {estat['assistencias']}")
                st.markdown("---")

