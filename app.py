# ==========================================================
# ANÁLISE HISTÓRICA DAS SELEÇÕES CAMPEÃS DA COPA DO MUNDO
# Banco de Dados II
# Streamlit
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Análise Histórica das Seleções Campeãs",
    page_icon="🏆",
    layout="wide"
)

# ==========================================================
# CARREGAMENTO DOS DADOS
# ==========================================================

from pathlib import Path

@st.cache_data
def carregar_dados():

    BASE = Path(__file__).parent
    DADOS = BASE / "dados"

    tournaments = pd.read_csv(DADOS / "tournaments.csv")
    matches = pd.read_csv(DADOS / "matches.csv")
    teams = pd.read_csv(DADOS / "teams.csv")
    standings = pd.read_csv(DADOS / "tournament_standings.csv")
    hosts = pd.read_csv(DADOS / "host_countries.csv")

    return tournaments, matches, teams, standings, hosts

tournaments, matches, teams, standings, hosts = carregar_dados()

# ==========================================================
# TÍTULO
# ==========================================================

st.markdown(
    """
    <h1 style='text-align:center; color:#0B3D91;'>
    Análise Histórica das Seleções Campeãs da Copa do Mundo
    </h1>

    <h3 style='text-align:center; color:#555555;'>
    Padrões Históricos para a Copa do Mundo FIFA 2026
    </h3>

    """,
    unsafe_allow_html=True
)

from pathlib import Path

PASTA_IMAGENS = Path(__file__).parent

arquivos = sorted(
    list(PASTA_IMAGENS.glob("*.jpg")) +
    list(PASTA_IMAGENS.glob("*.jpeg")) +
    list(PASTA_IMAGENS.glob("*.png"))
)

st.divider()

st.subheader("📸 Galeria de Jogadores Históricos")

imagem = st.selectbox(
    "Selecione uma imagem",
    arquivos,
    format_func=lambda x: x.stem.replace("_", " ").upper()
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(imagem, width=300)

st.caption(f"Imagem: {imagem.stem.replace('_', ' ').upper()}")

st.markdown(
"""
<div style="text-align:center; font-size:18px;">

Este dashboard apresenta uma análise histórica das seleções campeãs da Copa do Mundo FIFA,
utilizando dados do repositório <b>jfjelstul/worldcup</b>, com o objetivo de identificar padrões
que possam contribuir para análises relacionadas à Copa do Mundo FIFA 2026.

</div>
""",
unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Filtros")

anos = sorted(tournaments["year"].unique())

ano_inicial, ano_final = st.sidebar.select_slider(
    "Período",
    options=anos,
    value=(min(anos), max(anos))
)

campeoes = ["Todas"] + sorted(
    tournaments["winner"].dropna().unique()
)

campeao = st.sidebar.selectbox(
    "Seleção Campeã",
    campeoes
)

dados = tournaments[
    (tournaments["year"] >= ano_inicial) &
    (tournaments["year"] <= ano_final)
]

if campeao != "Todas":
    dados = dados[dados["winner"] == campeao]
    

# ==========================================================
# KPIs
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Copas realizadas",
    len(dados)
)

col2.metric(
    "Seleções Campeãs",
    dados["winner"].nunique()
)

col3.metric(
    "Países-sede",
    dados["host_country"].nunique()
)

media_times = round(dados["count_teams"].mean(),1)

col4.metric(
    "Média de Participantes",
    media_times
)

st.divider()

# ==========================================================
# CAMPEÕES
# ==========================================================

st.header("🏆 Ranking das Seleções Campeãs")

ranking = (
    dados["winner"]
    .value_counts()
    .reset_index()
)

ranking.columns = [
    "Seleção",
    "Títulos"
]

fig = px.bar(
    ranking,
    x="Seleção",
    y="Títulos",
    color="Títulos",
    template="plotly_white",
    text="Títulos"
)

fig.update_layout(
    xaxis_title="Seleção",
    yaxis_title="Quantidade de títulos"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    ranking,
    use_container_width=True
)

st.divider()

st.info(
"""
Observa-se que poucas seleções concentram a maior parte dos títulos da Copa do Mundo,
evidenciando a predominância histórica de países tradicionais como Brasil, Alemanha,
Itália e Argentina.
"""
)

# ==========================================================
# EVOLUÇÃO DOS CAMPEÕES
# ==========================================================

st.header("📈 Evolução Histórica dos Campeões")

linha = dados[
    ["year", "winner"]
].copy()

fig2 = px.scatter(
    linha,
    x="year",
    y="winner",
    color="winner",
    template="plotly_white",
    size=[10]*len(linha)
)

fig2.update_layout(
    xaxis_title="Ano",
    yaxis_title="Seleção Campeã"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# GOLS
# ==========================================================

st.header("⚽ Estatísticas de Gols")

matches["total_goals"] = (
    matches["home_team_score"] +
    matches["away_team_score"]
)

media = round(matches["total_goals"].mean(),2)
maximo = matches["total_goals"].max()
total = matches["total_goals"].sum()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Média por jogo",
    media
)

c2.metric(
    "Maior número de gols",
    maximo
)

c3.metric(
    "Total de gols",
    total
)

st.divider()

st.info(
"""
A média de gols por partida permite avaliar a evolução ofensiva da competição ao
longo das diferentes edições da Copa do Mundo.
"""
)

# ==========================================================
# PAÍSES-SEDE
# ==========================================================

st.header("🌍 Países-Sede das Copas do Mundo")

sedes = (
    dados["host_country"]
    .value_counts()
    .reset_index()
)

sedes.columns = [
    "País",
    "Quantidade"
]

fig3 = px.bar(
    sedes,
    x="País",
    y="Quantidade",
    color="Quantidade",
    template="plotly_white",
    text="Quantidade"
)

fig3.update_layout(
    xaxis_title="País",
    yaxis_title="Número de Copas"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# ==========================================================
# ANFITRIÃO
# ==========================================================

st.header("🏠 Desempenho do País-Sede")

host_perf = (
    hosts["performance"]
    .value_counts()
    .reset_index()
)

host_perf.columns = [
    "Resultado",
    "Quantidade"
]

fig4 = px.pie(
    host_perf,
    names="Resultado",
    values="Quantidade",
    template="plotly_white",
    hole=0.45
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.dataframe(
    host_perf,
    use_container_width=True
)

st.divider()

st.info(
"""
Os dados mostram que alguns países receberam a competição mais de uma vez,
demonstrando sua importância na história da Copa do Mundo.
"""
)

# ==========================================================
# CONTINENTES
# ==========================================================

st.header("🌎 Distribuição das Seleções por Continente")

continentes = (
    teams["region_name"]
    .value_counts()
    .reset_index()
)

continentes.columns = [
    "Continente",
    "Seleções"
]

fig5 = px.bar(
    continentes,
    x="Continente",
    y="Seleções",
    color="Seleções",
    template="plotly_white",
    text="Seleções"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.divider()

# ==========================================================
# PARTICIPAÇÕES
# ==========================================================

st.header("⚽ Seleções com mais Participações")

participacoes = (
    standings.groupby("team_name")
    .size()
    .reset_index(name="Participações")
    .sort_values(
        "Participações",
        ascending=False
    )
)

top10 = participacoes.head(10)

fig6 = px.bar(
    top10,
    x="team_name",
    y="Participações",
    color="Participações",
    template="plotly_white",
    text="Participações"
)

fig6.update_layout(
    xaxis_title="Seleção",
    yaxis_title="Participações"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.dataframe(
    top10,
    use_container_width=True
)

st.divider()

# ==========================================================
# MELHORES CAMPANHAS
# ==========================================================

st.header("🥇 Top 10 Campanhas")

melhores = standings[
    standings["position"] <= 10
].sort_values(
    ["position", "team_name"]
)

st.dataframe(
    melhores,
    use_container_width=True
)

st.divider()

# ==========================================================
# COMPARAÇÃO
# ==========================================================

st.header("📊 Comparação entre Seleções Campeãs")

selecoes = sorted(
    dados["winner"].unique()
)

selecionadas = st.multiselect(
    "Selecione uma ou mais seleções",
    selecoes,
    default=selecoes[:3]
)

comparacao = ranking[
    ranking["Seleção"].isin(selecionadas)
]

fig7 = px.bar(
    comparacao,
    x="Seleção",
    y="Títulos",
    color="Seleção",
    template="plotly_white",
    text="Títulos"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.divider()

# ==========================================================
# EVOLUÇÃO DO NÚMERO DE PARTICIPANTES
# ==========================================================

st.header("👥 Evolução do Número de Seleções Participantes")

participantes = dados[
    ["year", "count_teams"]
].sort_values("year")

fig8 = px.line(
    participantes,
    x="year",
    y="count_teams",
    template="plotly_white",
    markers=True
)

fig8.update_layout(
    xaxis_title="Ano",
    yaxis_title="Número de Seleções"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

st.divider()

# ==========================================================
# CAMPEÃO X PAÍS-SEDE
# ==========================================================

st.header("🏆 Campeão e País-Sede")

campeoes = dados[
    ["year", "host_country", "winner"]
].copy()

campeoes.columns = [
    "Ano",
    "País-Sede",
    "Campeão"
]

st.dataframe(
    campeoes,
    use_container_width=True
)

st.divider()

# ==========================================================
# PREVISÃO PARA 2026
# ==========================================================

st.header("🔮 Análise Histórica para a Copa do Mundo de 2026")

ranking2026 = (
    dados["winner"]
    .value_counts()
    .reset_index()
)

ranking2026.columns = [
    "Seleção",
    "Títulos"
]

ranking2026["Pontuação"] = (
    ranking2026["Títulos"] /
    ranking2026["Títulos"].max()
) * 100

st.info(
"""
A previsão abaixo utiliza apenas o histórico de títulos das seleções.
Não considera elenco atual, ranking FIFA ou desempenho recente.
"""
)

fig9 = px.bar(
    ranking2026.head(10),
    x="Seleção",
    y="Pontuação",
    color="Pontuação",
    template="plotly_white",
    text=ranking2026.head(10)["Pontuação"].round(1)
    
)

fig9.update_layout(
    xaxis_title="Seleção",
    yaxis_title="Índice Histórico"
)

st.plotly_chart(
    fig9,
    use_container_width=True
)

st.dataframe(
    ranking2026,
    use_container_width=True
)

st.divider()

# ==========================================================
# EXPORTAÇÃO
# ==========================================================

st.header("⬇️ Exportar Dados")

csv = ranking2026.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Baixar Ranking em CSV",
    data=csv,
    file_name="ranking_campeoes.csv",
    mime="text/csv"
)

st.divider()

# ==========================================================
# CONCLUSÕES
# ==========================================================

st.header("Conclusões")

maior = ranking2026.iloc[0]["Seleção"]
titulos = ranking2026.iloc[0]["Títulos"]

st.success(f"A seleção com maior número de títulos é {maior}, com {titulos} conquistas.")

st.write(
"""
A análise histórica permite observar padrões importantes
na evolução da Copa do Mundo, como:

- crescimento do número de seleções participantes;
- concentração de títulos em poucas seleções;
- influência dos países-sede;
- desempenho histórico das principais campeãs;
- evolução da competição ao longo das décadas.

Esses dados auxiliam na compreensão do histórico da competição
e podem servir como base para análises e previsões da Copa do
Mundo FIFA de 2026.
"""
)


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")

st.caption("""
Projeto desenvolvido para a disciplina de Banco de Dados II

Tema:
Análise Histórica das Seleções Campeãs da Copa do Mundo:
Padrões para a Copa do Mundo de 2026

Tecnologias utilizadas:

• Python

• Streamlit

• Pandas

• Plotly

Fonte dos dados:

Repositório jfjelstul/worldcup
""")
