import streamlit as st

def modo_jogador(sistema):
    st.title("🎮 Modo Jogador")

    if not sistema["torneio"]:
        st.warning("⚠️ Nenhum torneio foi criado ainda.")
        return

    torneios_disponiveis = list(sistema["torneio"].keys())
    torneio_escolhido = st.selectbox("🎯 Selecione o torneio que deseja visualizar:", torneios_disponiveis)

    confrontos = sistema["torneio"][torneio_escolhido]["confrontos"]
    times = sistema["torneio"][torneio_escolhido]["times"]

    if not confrontos:
        st.info("⚠️ Nenhum confronto cadastrado para esse torneio.")
        return

    st.markdown(f"### 📅 Confrontos do torneio **{torneio_escolhido}**")

    for numero_jogo, dados in confrontos.items():
        time1 = dados["time1"]
        time2 = dados["time2"]
        placar1 = times[time1]["pontos"] if time1 in times else 0
        placar2 = times[time2]["pontos"] if time2 in times else 0

        st.markdown(f"**{numero_jogo}** — {time1} {placar1} 🆚 {placar2} {time2}")

    st.info("🔁 Atualize a página para ver os placares mais recentes.")
