import streamlit as st
import time
from util import salvar_sistema

def modo_staff(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")

    if "staffs_confrontos" not in sistema:
        sistema["staffs_confrontos"] = {}

    confronto_atual = sistema["staffs_confrontos"].get(usuario_logado)

    with st.sidebar:
        st.success(f"Logado como: {usuario_logado} (staff)")
        st.markdown("## \ud83d\udccb Menu do Staff")

        opcoes_staff = {
            "Escolher confronto": lambda: escolher_confronto(sistema, ARQUIVO_JSON, usuario_logado),
            "Ver jogadores dos times": lambda: verificar_times_jogadores(sistema, usuario_logado),
            "Definir sequ\u00eancia (M/F)": lambda: definir_sequencia(sistema, ARQUIVO_JSON, usuario_logado),
            "Registrar ponto": lambda: registrar_ponto(sistema, ARQUIVO_JSON, usuario_logado),
            "Remover ponto": lambda: remover_ponto(sistema, ARQUIVO_JSON, usuario_logado),
            "Iniciar tempo": lambda: iniciar_tempo(sistema, ARQUIVO_JSON, usuario_logado),
            "Finalizar confronto": lambda: finalizar_confronto(sistema, ARQUIVO_JSON, usuario_logado),
        }

        escolha = st.radio("Selecione uma a\u00e7\u00e3o:", list(opcoes_staff.keys()), key=f"staff_menu_{usuario_logado}")

        for _ in range(20):
            st.write("")

        if st.button("\ud83d\udeaa Sair"):
            st.session_state.clear()
            st.rerun()

    st.title("\ud83c\udfae Painel do Staff")
    st.subheader(f"Torneio ativo: {torneio if torneio else 'Nenhum'}")

    if torneio and confronto_atual:
        confronto = sistema["torneio"][torneio]["confrontos"].get(confronto_atual, {})

        time1 = confronto.get("time1", "?")
        time2 = confronto.get("time2", "?")
        horario = confronto.get("horario", "?")
        local = confronto.get("local", "?")

        st.markdown(f"### \ud83d\udfe7 Confronto ativo: **{confronto_atual}**  \u2014  {time1} vs {time2} \u00e0s {horario} no {local}")

        col1, col2 = st.columns(2)

        with col1:
            if "tempo_inicio" in confronto:
                tempo_decorrido = int(time.time() - confronto["tempo_inicio"])
                minutos = tempo_decorrido // 60
                segundos = tempo_decorrido % 60
                st.markdown(f"""
                    <div style='background-color:#fdd835;padding:10px;border-radius:10px;width:fit-content;'>
                    \u23f1\ufe0f <strong>Tempo atual:</strong> {minutos:02d}:{segundos:02d}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color:#fdd835;padding:10px;border-radius:10px;width:fit-content;'>
                    \u23f1\ufe0f <strong>Tempo:</strong> N\u00e3o iniciado
                    </div>
                """, unsafe_allow_html=True)

        with col2:
            seq = confronto.get("sequencia")
            idx = confronto.get("indice_sequencia", 0)
            letra_atual = seq[idx] if seq and idx < len(seq) else "Fim" if seq else "?"

            st.markdown(f"""
                <div style='background-color:#3f51b5;color:white;padding:10px;border-radius:10px;width:fit-content;'>
                \ud83d\udd01 <strong>Sequ\u00eancia atual:</strong> {letra_atual}
                </div>
            """, unsafe_allow_html=True)

    else:
        st.subheader("Confronto ativo: Nenhum")

    st.divider()
    if escolha:
        opcoes_staff[escolha]()

def escolher_confronto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")
    if not torneio:
        st.warning("Nenhum torneio ativo.")
        return

    confrontos = sistema["torneio"][torneio].get("confrontos", {})
    if not confrontos:
        st.info("Nenhum confronto cadastrado.")
        return

    opcoes = {
        num: f"{num}: {dados['time1']} vs {dados['time2']} \u00e0s {dados['horario']} no {dados['local']}"
        for num, dados in confrontos.items()
    }
    escolha = st.selectbox("Escolha o confronto:", list(opcoes.keys()), format_func=lambda x: opcoes[x])

    if st.button("\u2705 Confirmar confronto"):
        sistema["staffs_confrontos"][usuario_logado] = escolha
        salvar_sistema(sistema, ARQUIVO_JSON)
        st.success(f"Confronto {escolha} ativo para {usuario_logado}!")



def escolher_confronto(sistema, usuario_logado, ARQUIVO_JSON):
    torneio_atual = sistema.get("torneio_ativo")

    if not torneio_atual or torneio_atual not in sistema["torneio"]:
        st.warning("⚠️ Nenhum torneio ativo selecionado.")
        return

    confrontos = sistema["torneio"][torneio_atual].get("confrontos", {})

    if not confrontos:
        st.info("⚠️ Nenhum confronto cadastrado ainda.")
        return

    opcoes = {
        numero: f"{numero}: {dados['time1']} vs {dados['time2']} às {dados['horario']} no {dados['local']}"
        for numero, dados in confrontos.items()
    }

    jogo_marcar = st.selectbox("📋 Escolha o confronto:", options=list(opcoes.keys()), format_func=lambda x: opcoes[x])

    if st.button("✅ Marcar confronto como ativo"):
        if "staffs_confrontos" not in sistema:
            sistema["staffs_confrontos"] = {}
        sistema["staffs_confrontos"][usuario_logado] = jogo_marcar
        salvar_sistema(sistema, ARQUIVO_JSON)

        dados = confrontos[jogo_marcar]
        st.success(f"{jogo_marcar} marcado com sucesso!")
        st.markdown(f"**Confronto ativo:** {dados['time1']} 🆚 {dados['time2']} às {dados['horario']} no {dados['local']}")

def verificar_times_jogadores(sistema, usuario_logado):
    torneio_atual = sistema.get("torneio_ativo")
    confronto_id = sistema.get("staffs_confrontos", {}).get(usuario_logado)

    if not torneio_atual or not confronto_id:
        st.warning("⚠️ Torneio ou confronto não foi selecionado.")
        return

    confronto = sistema["torneio"][torneio_atual]["confrontos"]
    if confronto_id not in confronto:
        st.error("❌ Confronto não encontrado.")
        return

    time1 = confronto[confronto_id]["time1"]
    time2 = confronto[confronto_id]["time2"]
    times = sistema["torneio"][torneio_atual]["times"]

    col1, col2 = st.columns(2)
    for i, nome_time in enumerate((time1, time2)):
        if nome_time not in times:
            st.error(f"❌ Time '{nome_time}' não encontrado.")
            continue

        dados = times[nome_time]
        jogadores = dados.get("jogadores", {})

        with (col1 if i == 0 else col2):
            st.markdown(f"### 🔷 Time: {nome_time} – Pontos: {dados['pontos']}")
            if jogadores:
                for nome_jogador, estatisticas in jogadores.items():
                    st.markdown(
                        f"- **{nome_jogador}** | Gols: {estatisticas['gols']} | Assistências: {estatisticas['assistencias']}"
                    )
            else:
                st.warning("⚠️ Nenhum jogador cadastrado nesse time ainda.")

def definir_sequencia(sistema, ARQUIVO_JSON, usuario_logado):
    from util import salvar_sistema

    torneio_atual = sistema.get("torneio_ativo")
    confronto_ativo_staff = sistema.get("staffs_confrontos", {}).get(usuario_logado)

    if not torneio_atual or not confronto_ativo_staff:
        st.warning("⚠️ Torneio ou confronto não foi selecionado.")
        return

    confronto = sistema["torneio"][torneio_atual]["confrontos"].get(confronto_ativo_staff)
    if not confronto:
        st.error("❌ Confronto não encontrado.")
        return

    if confronto.get("finalizado"):
        st.error("🚫 Esse confronto já foi finalizado. Não é possível definir sequência.")
        return

    escolha = st.radio("Escolha a sequência:", ["M", "F"], key="radio_sequencia")

    if st.button("✅ Confirmar sequência"):
        if escolha == "M":
            sequencia = ["M", "F", "F", "M", "M", "F", "F", "M", "M", "F", "F", "M", "M", "F", "F", "M", "M", "F"]
        else:
            sequencia = ["F", "M", "M", "F", "F", "M", "M", "F", "F", "M", "M", "F", "F", "M", "M", "F", "F", "M"]

        confronto["sequencia"] = sequencia
        confronto["tipo_sequencia"] = escolha
        confronto["indice_sequencia"] = 0

        salvar_sistema(sistema, ARQUIVO_JSON)

        st.success(f"✅ Sequência {escolha} definida com sucesso.")
        st.markdown("🔁 Sequência:")
        st.markdown(" → ".join(sequencia))

def registrar_ponto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio_atual = sistema.get("torneio_ativo")
    jogo_atual = sistema["staffs"][usuario_logado].get("confronto_ativo")

    if not torneio_atual or not jogo_atual:
        st.warning("⚠️ Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio_atual]["confrontos"][jogo_atual]
    if confronto.get("finalizado"):
        st.error("🚫 Esse confronto já foi finalizado.")
        return

    if "sequencia" not in confronto or "indice_sequencia" not in confronto:
        st.warning("⚠️ Sequência não definida para esse confronto.")
        return

    if confronto["indice_sequencia"] >= len(confronto["sequencia"]):
        st.error("🚨 A sequência já foi totalmente utilizada.")
        return

    times = sistema["torneio"][torneio_atual]["times"]
    time1 = confronto["time1"]
    time2 = confronto["time2"]

    time_nome = st.selectbox("🏷️ Time que fez o gol:", [time1, time2])
    jogadores = list(times[time_nome]["jogadores"].keys())

    if not jogadores:
        st.warning("⚠️ Nenhum jogador cadastrado nesse time.")
        return

    jogador_gol = st.selectbox("⚽ Jogador que marcou o gol:", jogadores)
    jogador_assis = st.selectbox("🎯 Jogador que deu a assistência:", jogadores)

    if st.button("✅ Registrar ponto"):
        times[time_nome]["pontos"] += 1
        times[time_nome]["jogadores"][jogador_gol]["gols"] += 1
        times[time_nome]["jogadores"][jogador_assis]["assistencias"] += 1
        confronto["indice_sequencia"] += 1

        salvar_sistema(sistema, ARQUIVO_JSON)

        st.success(f"🎉 Gol do {time_nome}! {jogador_gol} marcou com assistência de {jogador_assis}.")
        st.rerun()

def remover_ponto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio_atual = sistema.get("torneio_ativo")
    jogo_atual = sistema["staffs"][usuario_logado].get("confronto_ativo")

    if not torneio_atual or not jogo_atual:
        st.warning("⚠️ Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio_atual]["confrontos"][jogo_atual]

    if confronto.get("finalizado"):
        st.error("🚫 Esse confronto já foi finalizado.")
        return

    if "sequencia" not in confronto or "indice_sequencia" not in confronto:
        st.warning("⚠️ Sequência não definida.")
        return

    if confronto["indice_sequencia"] == 0:
        st.info("⚠️ Nenhum ponto registrado ainda.")
        return

    idx = confronto["indice_sequencia"] - 1
    letra = confronto["sequencia"][idx]

    st.markdown(f"""
        <div style='background-color:#ff9800;color:white;padding:10px;border-radius:10px;width:fit-content;'>
        🛑 <strong>Removendo ponto da jogada #{idx + 1}</strong> (letra: {letra})
        </div>
    """, unsafe_allow_html=True)

    times = sistema["torneio"][torneio_atual]["times"]
    time1 = confronto["time1"]
    time2 = confronto["time2"]

    time_nome = st.selectbox("🏷️ Time que perdeu o ponto:", [time1, time2])

    jogadores_com_estatisticas = [
        nome for nome, estat in times[time_nome]["jogadores"].items()
        if estat["gols"] > 0 or estat["assistencias"] > 0
    ]

    if not jogadores_com_estatisticas:
        st.warning("⚠️ Nenhum jogador com estatísticas disponíveis nesse time.")
        return

    jogador_gol = st.selectbox("⚽ Jogador que teve o gol removido:", jogadores_com_estatisticas)
    jogador_assis = st.selectbox("🎯 Jogador que teve a assistência removida:", jogadores_com_estatisticas)

    if st.button("🗑️ Confirmar remoção do ponto"):
        if times[time_nome]["jogadores"][jogador_gol]["gols"] > 0:
            times[time_nome]["jogadores"][jogador_gol]["gols"] -= 1
        if times[time_nome]["jogadores"][jogador_assis]["assistencias"] > 0:
            times[time_nome]["jogadores"][jogador_assis]["assistencias"] -= 1
        if times[time_nome]["pontos"] > 0:
            times[time_nome]["pontos"] -= 1

        confronto["indice_sequencia"] -= 1
        salvar_sistema(sistema, ARQUIVO_JSON)

        st.success(f"✅ Ponto removido com sucesso. Jogada #{idx + 1} anulada.")

        if confronto["indice_sequencia"] > 0:
            nova_letra = confronto["sequencia"][confronto["indice_sequencia"] - 1]
            st.info(f"🔁 Nova letra ativa: **{nova_letra}**")
        else:
            st.info("ℹ️ Nenhuma jogada restante no histórico.")

def iniciar_tempo(sistema, ARQUIVO_JSON, usuario_logado):
    torneio_atual = sistema.get("torneio_ativo")
    chave_staff = f"confronto_ativo_{usuario_logado}"
    jogo_atual = sistema.get(chave_staff)

    if not torneio_atual or not jogo_atual:
        st.warning("⚠️ Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio_atual]["confrontos"][jogo_atual]

    # ✅ Confronto finalizado: não mostra nada
    if confronto.get("finalizado"):
        st.markdown("### ✅ Confronto finalizado.")
        return

    st.markdown("## 🕒 Controle de tempo")

    if "tempo_inicio" not in confronto:
        if st.button("▶️ Iniciar tempo"):
            tempo_atual = time.time()
            confronto["tempo_inicio"] = tempo_atual
            salvar_sistema(sistema, ARQUIVO_JSON)
            st.success("🕒 Tempo iniciado com sucesso!")
            st.rerun()
    else:
        tempo_inicio = confronto["tempo_inicio"]
        tempo_decorrido = int(time.time() - tempo_inicio)
        minutos = tempo_decorrido // 60
        segundos = tempo_decorrido % 60

        st.markdown(f"""
            <div style='background-color:#fdd835;padding:10px;border-radius:10px;width:fit-content;'>
            ⏱️ <strong>Tempo atual:</strong> {minutos:02d}:{segundos:02d}
            </div>
        """, unsafe_allow_html=True)

        time.sleep(1)
        st.rerun()

def finalizar_confronto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")
    chave_staff = f"confronto_ativo_{usuario_logado}"
    confronto_id = sistema.get(chave_staff)

    if not torneio or not confronto_id:
        st.warning("⚠️ Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio]["confrontos"][confronto_id]

    if confronto.get("finalizado"):
        st.info("🚫 Esse confronto já foi finalizado.")
        return

    time1 = confronto["time1"]
    time2 = confronto["time2"]
    times = sistema["torneio"][torneio]["times"]

    vencedor = calcular_vencedor_por_gols(sistema, confronto)

    placar1 = confronto.get("placar1", 0)
    placar2 = confronto.get("placar2", 0)

    st.markdown(f"## 🏁 Finalizar confronto: {time1} vs {time2}")
    st.markdown(f"**Placar final:** `{time1}` {placar1} 🆚 {placar2} `{time2}`")

    if vencedor:
        st.success(f"🏆 Time vencedor: **{vencedor}**")
    else:
        st.info("🤝 O jogo terminou empatado.")

    if st.button("✅ Confirmar e finalizar confronto"):
        confronto["finalizado"] = True
        confronto["vencedor"] = vencedor

        if "tempo_inicio" in confronto:
            del confronto["tempo_inicio"]

        salvar_sistema(sistema, ARQUIVO_JSON)
        st.success("🎉 Confronto finalizado com sucesso!")
        st.info("❌ Este confronto agora está bloqueado para novas alterações.")

def calcular_vencedor_por_gols(sistema, confronto):
    torneio = sistema["torneio_ativo"]
    time1 = confronto["time1"]
    time2 = confronto["time2"]
    times = sistema["torneio"][torneio]["times"]

    gols_time1 = sum(j["gols"] for j in times[time1]["jogadores"].values())
    gols_time2 = sum(j["gols"] for j in times[time2]["jogadores"].values())

    confronto["placar1"] = gols_time1
    confronto["placar2"] = gols_time2

    if gols_time1 > gols_time2:
        return time1
    elif gols_time2 > gols_time1:
        return time2
    return None

