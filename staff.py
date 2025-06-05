import streamlit as st
import time
from util import salvar_todos

def modo_staff(sistema, ARQUIVO_JSON, usuario_logado):
    if "staffs_confrontos" not in sistema:
        sistema["staffs_confrontos"] = {}

    torneio = sistema.get("torneio_ativo")
    confronto_id = sistema["staffs_confrontos"].get(usuario_logado)
    confronto = sistema["torneio"][torneio]["confrontos"].get(confronto_id) if confronto_id and torneio else None

    st.title("🎮 Painel do Staff")

    # TOPO COM INFORMAÇÕES
    col1, col2, col3 = st.columns([0.4, 0.3, 0.3])
    
    with col1:
        st.markdown(f"""
            <div style='background-color:#1976d2;padding:10px;border-radius:10px;text-align:center;color:white;font-weight:bold;'>
                🏆 Torneio ativo:<br>{torneio if torneio else "Nenhum"}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        if confronto:
            tempo_inicio = confronto.get("tempo_inicio")
            if tempo_inicio:
                tempo_decorrido = int(time.time() - tempo_inicio)
                minutos = tempo_decorrido // 60
                segundos = tempo_decorrido % 60
                tempo_str = f"{minutos:02d}:{segundos:02d}"
            else:
                tempo_str = "Não iniciado"

            st.markdown(f"""
                <div style='background-color:#4caf50;padding:10px;border-radius:10px;text-align:center;color:white;font-weight:bold;'>
                    ⏱️ Tempo:<br>{tempo_str}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background-color:#4caf50;padding:10px;border-radius:10px;text-align:center;color:white;font-weight:bold;'>
                    ⏱️ Tempo:<br> -
                </div>
            """, unsafe_allow_html=True)

    with col3:
        if confronto:
            seq = confronto.get("sequencia")
            idx = confronto.get("indice_sequencia", 0)
            letra = seq[idx] if seq and idx < len(seq) else "Fim"
            st.markdown(f"""
                <div style='background-color:#3f51b5;padding:10px;border-radius:10px;text-align:center;color:white;font-weight:bold;'>
                    🔁 Sequência atual:<br>{letra}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background-color:#3f51b5;padding:10px;border-radius:10px;text-align:center;color:white;font-weight:bold;'>
                    🔁 Sequência atual:<br> -
                </div>
            """, unsafe_allow_html=True)

    # CONFRONTO DETALHADO
    if confronto:
        time1 = confronto.get("time1", "?")
        time2 = confronto.get("time2", "?")
        horario = confronto.get("horario", "?")
        local = confronto.get("local", "?")
        st.markdown(f"### 📍 Confronto: **{confronto_id} — {time1} vs {time2} às {horario} no {local}**")
    else:
        st.markdown("### 📍 Confronto: Nenhum selecionado.")

    # MENU LATERAL
    with st.sidebar:
        st.success(f"Logado como: {usuario_logado} (staff)")
        st.markdown("## Menu do Staff")

        opcoes_staff = {
            "Escolher confronto": lambda: escolher_confronto(sistema, ARQUIVO_JSON, usuario_logado),
            "Ver jogadores dos times": lambda: verificar_times_jogadores(sistema, usuario_logado),
            "Definir sequência (M/F)": lambda: definir_sequencia(sistema, ARQUIVO_JSON, usuario_logado),
            "Registrar ponto": lambda: registrar_ponto(sistema, ARQUIVO_JSON, usuario_logado),
            "Remover ponto": lambda: remover_ponto(sistema, ARQUIVO_JSON, usuario_logado),
            "Iniciar tempo": lambda: iniciar_tempo(sistema, ARQUIVO_JSON, usuario_logado),
            "Finalizar confronto": lambda: finalizar_confronto(sistema, ARQUIVO_JSON, usuario_logado),
        }

        escolha = st.radio("Selecione uma ação:", list(opcoes_staff.keys()), key=f"staff_menu_{usuario_logado}")

        for _ in range(15):
            st.write("")

        if st.button("🚪 Sair"):
            st.session_state.clear()
            st.rerun()

    st.divider()
    if escolha:
        opcoes_staff[escolha]()





def escolher_confronto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")

    if not torneio:
        st.warning("⚠️ Nenhum torneio ativo.")
        return

    confrontos = sistema["torneio"][torneio].get("confrontos", {})

    if not confrontos:
        st.info("⚠️ Nenhum confronto cadastrado.")
        return

    opcoes = {
        num: f"{num}: {dados['time1']} vs {dados['time2']} às {dados['horario']} no {dados['local']}"
        for num, dados in confrontos.items()
    }

    confronto_escolhido = st.selectbox(
        "📋 Escolha o confronto:",
        options=list(opcoes.keys()),
        format_func=lambda x: opcoes[x],
        key=f"selectbox_confronto_{usuario_logado}"
    )

    if st.button("✅ Confirmar confronto", key=f"botao_confirmar_{usuario_logado}"):
        sistema.setdefault("staffs_confrontos", {})[usuario_logado] = confronto_escolhido
        salvar_todos(sistema, ARQUIVO_JSON)
        st.success(f"Confronto **{confronto_escolhido}** marcado como ativo para {usuario_logado} ✅")
        st.rerun()

def verificar_times_jogadores(sistema, usuario_logado):
    torneio_atual = sistema.get("torneio_ativo")
    confronto_id = sistema["staffs_confrontos"].get(usuario_logado)

    if not torneio_atual or not confronto_id:
        st.warning("⚠️ Torneio ou confronto não foi selecionado.")
        return

    confronto = sistema["torneio"][torneio_atual]["confrontos"].get(confronto_id)
    if not confronto:
        st.warning("❌ Confronto não encontrado.")
        return

    time1, time2 = confronto["time1"], confronto["time2"]
    times = sistema["torneio"][torneio_atual]["times"]
    stats = confronto.setdefault("gols", {})  # ← usa apenas os dados salvos neste confronto

    col1, col2 = st.columns(2)

    for col, nome_time in zip((col1, col2), (time1, time2)):
        with col:
            jogadores = times[nome_time]["jogadores"]
            gols_time = sum(stats.get(nome, {}).get("gols", 0) for nome in jogadores)

            st.markdown(f"### 🔷 {nome_time}")
            st.markdown(f"**Total de Gols no Confronto: {gols_time}**")

            if jogadores:
                for nome, _ in jogadores.items():
                    g = stats.get(nome, {}).get("gols", 0)
                    a = stats.get(nome, {}).get("assistencias", 0)
                    st.write(f"👤 {nome} — ⚽ Gols: {g} | 🎯 Assistências: {a}")
            else:
                st.write("⚠️ Nenhum jogador cadastrado.")

def definir_sequencia(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")
    confronto_id = sistema.get("staffs_confrontos", {}).get(usuario_logado)

    if not torneio or not confronto_id:
        st.warning("⚠️ Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio]["confrontos"][confronto_id]

    if confronto.get("finalizado"):
        st.error("🚫 Esse confronto já foi finalizado. Não é possível definir sequência.")
        return

    st.markdown("### 🔁 Defina a sequência de pontuação (M ou F)")
    escolha = st.radio("Escolha a sequência:", ["M", "F"], horizontal=True)

    col1, col2 = st.columns([0.5, 0.5])
    
    with col1:
        if st.button("✅ Confirmar sequência"):
            if escolha == "M":
                sequencia = ["M", "F", "F", "M", "M", "F", "F", "M", "M", "F", "F", "M", "M",
                             "F", "F", "M", "M", "F"]
            else:
                sequencia = ["F", "M", "M", "F", "F", "M", "M", "F", "F", "M", "M", "F", "F",
                             "M", "M", "F", "F", "M"]

            confronto["sequencia"] = sequencia
            confronto["tipo_sequencia"] = escolha
            confronto["indice_sequencia"] = 0

            salvar_todos(sistema, ARQUIVO_JSON)
            st.success(f"✅ Sequência {escolha} definida com sucesso!")
            st.rerun()

    with col2:
        if st.button("🔄 Resetar sequência"):
            confronto.pop("sequencia", None)
            confronto.pop("tipo_sequencia", None)
            confronto.pop("indice_sequencia", None)
            salvar_todos(sistema, ARQUIVO_JSON)
            st.warning("🔁 Sequência resetada com sucesso!")
            st.rerun()

def iniciar_tempo(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")
    confronto_id = sistema["staffs_confrontos"].get(usuario_logado)

    if not torneio or not confronto_id:
        st.warning("⚠️ Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio]["confrontos"][confronto_id]

    if confronto.get("finalizado"):
        st.info("🚫 Confronto finalizado. Tempo encerrado.")
        return

    st.markdown("### ⏱️ Controle de Tempo")

    if "tempo_inicio" not in confronto:
        if st.button("▶️ Iniciar tempo"):
            confronto["tempo_inicio"] = time.time()
            confronto["tempo_pausado"] = False
            salvar_todos(sistema, ARQUIVO_JSON)
            st.rerun()

    elif confronto.get("tempo_pausado"):
        if st.button("🔁 Retomar tempo"):
            pausa = confronto.get("tempo_pausa")
            if pausa:
                tempo_antes = pausa - confronto["tempo_inicio"]
                confronto["tempo_inicio"] = time.time() - tempo_antes
            confronto["tempo_pausado"] = False
            salvar_todos(sistema, ARQUIVO_JSON)
            st.rerun()
    else:
        tempo_inicio = confronto["tempo_inicio"]
        tempo_decorrido = int(time.time() - tempo_inicio)
        minutos = tempo_decorrido // 60
        segundos = tempo_decorrido % 60

        st.markdown(f"""
            <div style='background-color:#4caf50;padding:10px;border-radius:10px;width:fit-content;color:white;font-size:18px'>
            🟢 Tempo atual: {minutos:02d}:{segundos:02d}
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏸️ Pausar tempo"):
                confronto["tempo_pausado"] = True
                confronto["tempo_pausa"] = time.time()
                salvar_todos(sistema, ARQUIVO_JSON)
                st.rerun()

        with col2:
            if st.button("🔄 Reiniciar tempo"):
                del confronto["tempo_inicio"]
                confronto.pop("tempo_pausa", None)
                confronto.pop("tempo_pausado", None)
                salvar_todos(sistema, ARQUIVO_JSON)
                st.rerun()

    time.sleep(1)
    st.rerun()

def registrar_ponto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio_atual = sistema.get("torneio_ativo")
    confronto_id = sistema["staffs_confrontos"].get(usuario_logado)

    if not torneio_atual or not confronto_id:
        st.warning("⚠️ Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio_atual]["confrontos"][confronto_id]
    if confronto.get("finalizado"):
        st.error("🚫 Confronto já finalizado.")
        return

    if "sequencia" not in confronto or "indice_sequencia" not in confronto:
        st.warning("⚠️ Sequência não definida.")
        return

    if confronto["indice_sequencia"] >= len(confronto["sequencia"]):
        st.error("🚨 Sequência finalizada.")
        return

    time1 = confronto["time1"]
    time2 = confronto["time2"]
    times_disponiveis = [time1, time2]

    nome_time = st.selectbox("🏷️ Selecione o time que fez o gol:", options=times_disponiveis)

    jogadores = list(sistema["torneio"][torneio_atual]["times"][nome_time]["jogadores"].keys())
    if not jogadores:
        st.warning("⚠️ Nenhum jogador cadastrado nesse time.")
        return

    nome_gol = st.selectbox("⚽ Jogador que fez o gol:", options=jogadores)
    nome_assis = st.selectbox("🎯 Jogador que deu assistência:", options=jogadores)

    if st.button("✅ Confirmar ponto"):
        # Garante estrutura de gols por confronto
        if "gols" not in confronto:
            confronto["gols"] = {}

        for jogador in [nome_gol, nome_assis]:
            if jogador not in confronto["gols"]:
                confronto["gols"][jogador] = {"gols": 0, "assistencias": 0}

        confronto["gols"][nome_gol]["gols"] += 1
        confronto["gols"][nome_assis]["assistencias"] += 1
        confronto["indice_sequencia"] += 1

        salvar_todos(sistema, ARQUIVO_JSON)

        st.success(f"✅ Gol registrado com sucesso! {nome_gol} fez o gol com assistência de {nome_assis}.")
        st.rerun()

def remover_ponto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")
    confronto_id = sistema["staffs_confrontos"].get(usuario_logado)

    if not torneio or not confronto_id:
        st.warning("Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio]["confrontos"][confronto_id]

    if confronto.get("finalizado") or confronto.get("indice_sequencia", 0) == 0:
        st.error("Não há pontos para remover.")
        return

    st.subheader("🛑 Remover Ponto")

    times_validos = []
    for t in [confronto["time1"], confronto["time2"]]:
        if sistema["torneio"][torneio]["times"][t]["pontos"] > 0:
            times_validos.append(t)

    if not times_validos:
        st.warning("Nenhum time tem pontos registrados.")
        return

    time_selecionado = st.selectbox("Time que teve o ponto removido", times_validos)
    jogadores = sistema["torneio"][torneio]["times"][time_selecionado]["jogadores"]

    jogadores_gol = [j for j, est in jogadores.items() if est["gols"] > 0]
    jogadores_assis = [j for j, est in jogadores.items() if est["assistencias"] > 0]

    if not jogadores_gol or not jogadores_assis:
        st.warning("Nenhum jogador elegível para remoção.")
        return

    jogador_gol = st.selectbox("Jogador do gol a ser removido", jogadores_gol)
    jogador_assis = st.selectbox("Jogador da assistência a ser removida", jogadores_assis)

    if st.button("Remover ponto"):
        jogadores[jogador_gol]["gols"] -= 1
        jogadores[jogador_assis]["assistencias"] -= 1
        sistema["torneio"][torneio]["times"][time_selecionado]["pontos"] -= 1
        confronto["indice_sequencia"] -= 1
        salvar_todos(sistema, ARQUIVO_JSON)
        st.success("Ponto removido com sucesso.")

def finalizar_confronto(sistema, ARQUIVO_JSON, usuario_logado):
    torneio = sistema.get("torneio_ativo")
    confronto_id = sistema["staffs_confrontos"].get(usuario_logado)

    if not torneio or not confronto_id:
        st.warning("Torneio ou confronto não selecionado.")
        return

    confronto = sistema["torneio"][torneio]["confrontos"].get(confronto_id)
    if not confronto:
        st.error("Confronto não encontrado.")
        return

    if confronto.get("finalizado"):
        st.info("🚫 Esse confronto já está finalizado.")
        return

    time1 = confronto["time1"]
    time2 = confronto["time2"]
    stats = confronto.get("gols", {})

    times = sistema["torneio"][torneio]["times"]

    gols_time1 = sum(v["gols"] for j, v in stats.items() if j in times[time1]["jogadores"])
    gols_time2 = sum(v["gols"] for j, v in stats.items() if j in times[time2]["jogadores"])

    st.markdown("## ⚠️ Deseja finalizar o confronto?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {time1}")
        st.write(f"Total de gols: {gols_time1}")

    with col2:
        st.markdown(f"### {time2}")
        st.write(f"Total de gols: {gols_time2}")

    # Mostrar tempo final
    if "tempo_inicio" in confronto:
        if confronto.get("tempo_pausado"):
            tempo_final = confronto["tempo_pausa"] - confronto["tempo_inicio"]
        else:
            tempo_final = time.time() - confronto["tempo_inicio"]
        minutos = int(tempo_final) // 60
        segundos = int(tempo_final) % 60
        st.write(f"⏱️ Tempo total: {minutos:02d}:{segundos:02d}")
    else:
        st.write("⏱️ Tempo: Não iniciado.")

    if st.button("✅ Confirmar finalização"):
        # Salvar placares no confronto
        confronto["placar1"] = gols_time1
        confronto["placar2"] = gols_time2

        # Adiciona os pontos dos gols aos totais gerais
        times[time1]["pontos"] += gols_time1
        times[time2]["pontos"] += gols_time2

        # Verifica vencedor
        if gols_time1 > gols_time2:
            confronto["vencedor"] = time1
        elif gols_time2 > gols_time1:
            confronto["vencedor"] = time2
        else:
            confronto["vencedor"] = "Empate"

        # Marca como finalizado e trava o tempo
        confronto["finalizado"] = True
        if "tempo_inicio" in confronto and not confronto.get("tempo_pausado"):
            confronto["tempo_pausa"] = time.time()
            confronto["tempo_pausado"] = True

        salvar_todos(sistema, ARQUIVO_JSON)
        st.success(f"✅ Confronto finalizado! Resultado: **{gols_time1} x {gols_time2}** — Vencedor: **{confronto['vencedor']}**")

