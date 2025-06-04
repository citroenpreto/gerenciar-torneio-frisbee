import streamlit as st

def modo_jogador(sistema):
    st.title("🎮 Modo Jogador")

    # === SIDEBAR COM BOTÃO DE SAIR ===
    with st.sidebar:
        st.markdown("## 👤 Modo Jogador")

        for _ in range(20):
            st.write("")

        if st.button("🚪 Sair"):
            st.session_state.clear()
            st.rerun()

    if not sistema["torneio"]:
        st.warning("⚠️ Nenhum torneio foi criado ainda.")
        return

    torneios_disponiveis = list(sistema["torneio"].keys())
    torneio_escolhido = st.selectbox("🎯 Selecione o torneio que deseja visualizar:", torneios_disponiveis)

    confrontos = sistema["torneio"][torneio_escolhido]["confrontos"]

    if not confrontos:
        st.info("⚠️ Nenhum confronto cadastrado para esse torneio.")
        return

    st.markdown(f"### 📅 Confrontos do torneio **{torneio_escolhido}**")

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

        st.markdown(f"**{numero_jogo}** — {resultado} ⏰ {horario} 📍 {local}")

    st.info("🔁 Atualize a página para ver os placares mais recentes.")
