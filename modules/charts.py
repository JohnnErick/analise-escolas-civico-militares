import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLOR_MAP = {
    "Cívico-Militar": "#C0392B",       # Vermelho escuro/Terracota sóbrio
    "Não Cívico-Militar": "#2980B9",   # Azul clássico
}

CHART_THEME = "plotly_white"

def make_boxplot_comparison(df: pd.DataFrame, metric_col: str, title: str, y_label: str):
    df_valid = df.dropna(subset=[metric_col, "TIPO_GESTAO"])
    if df_valid.empty:
        return None
        
    fig = px.box(
        df_valid,
        x="TIPO_GESTAO",
        y=metric_col,
        color="TIPO_GESTAO",
        color_discrete_map=COLOR_MAP,
        points="all",
        hover_data=["NO_ESCOLA", "NO_MUNICIPIO", "REDE", "ETAPA", "ANO"],
        title=title,
        labels={"TIPO_GESTAO": "Tipo de Gestão", metric_col: y_label},
        template=CHART_THEME
    )
    
    # Adicionar marcador de média com diamante
    means = df_valid.groupby("TIPO_GESTAO")[metric_col].mean().reset_index()
    for _, row in means.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["TIPO_GESTAO"]],
            y=[row[metric_col]],
            mode="markers+text",
            marker=dict(symbol="diamond", size=12, color="black"),
            text=[f"Média: {row[metric_col]:.1f}"],
            textposition="top right",
            name=f"Média ({row['TIPO_GESTAO']})",
            showlegend=False
        ))
        
    fig.update_layout(
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_title="",
        yaxis_title=y_label
    )
    return fig

def make_histogram_comparison(df: pd.DataFrame, metric_col: str, title: str, x_label: str):
    df_valid = df.dropna(subset=[metric_col, "TIPO_GESTAO"])
    if df_valid.empty:
        return None
        
    fig = px.histogram(
        df_valid,
        x=metric_col,
        color="TIPO_GESTAO",
        color_discrete_map=COLOR_MAP,
        barmode="overlay",
        marginal="box",
        opacity=0.65,
        title=title,
        labels={"TIPO_GESTAO": "Tipo de Gestão", metric_col: x_label},
        template=CHART_THEME,
        hover_data=["NO_ESCOLA", "NO_MUNICIPIO"]
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_title=x_label,
        yaxis_title="Quantidade de Escolas",
        legend=dict(title="Tipo de Gestão", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_scatter_disciplinas(df: pd.DataFrame, title: str):
    df_valid = df.dropna(subset=["SAEB_PORTUGUES", "SAEB_MATEMATICA", "TIPO_GESTAO"])
    if df_valid.empty:
        return None
        
    fig = px.scatter(
        df_valid,
        x="SAEB_PORTUGUES",
        y="SAEB_MATEMATICA",
        color="TIPO_GESTAO",
        color_discrete_map=COLOR_MAP,
        opacity=0.75,
        size_max=10,
        hover_name="NO_ESCOLA",
        hover_data=["NO_MUNICIPIO", "REDE", "ETAPA", "ANO"],
        title=title,
        labels={
            "SAEB_PORTUGUES": "Proficiência SAEB Língua Portuguesa",
            "SAEB_MATEMATICA": "Proficiência SAEB Matemática",
            "TIPO_GESTAO": "Tipo de Gestão"
        },
        template=CHART_THEME
    )
    
    # Linhas de médias gerais como referência
    media_p = df_valid["SAEB_PORTUGUES"].mean()
    media_m = df_valid["SAEB_MATEMATICA"].mean()
    
    fig.add_vline(x=media_p, line_dash="dash", line_color="gray", annotation_text=f"Média Geral LP: {media_p:.1f}")
    fig.add_hline(y=media_m, line_dash="dash", line_color="gray", annotation_text=f"Média Geral Mat: {media_m:.1f}")
    
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(title="Tipo de Gestão", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_time_series(df: pd.DataFrame, metric_col: str, title: str, y_label: str):
    df_valid = df.dropna(subset=[metric_col, "TIPO_GESTAO", "ANO"])
    if df_valid.empty:
        return None
        
    # Agrupa por Ano e Tipo de Gestão
    resumo = df_valid.groupby(["ANO", "TIPO_GESTAO"]).agg(
        media=(metric_col, "mean"),
        mediana=(metric_col, "median"),
        qtd=(metric_col, "count")
    ).reset_index()
    
    fig = go.Figure()
    
    for tipo in ["Cívico-Militar", "Não Cívico-Militar"]:
        sub = resumo[resumo["TIPO_GESTAO"] == tipo].sort_values("ANO")
        if sub.empty:
            continue
        cor = COLOR_MAP.get(tipo, "#333333")
        fig.add_trace(go.Scatter(
            x=sub["ANO"],
            y=sub["media"],
            mode="lines+markers",
            name=f"{tipo} (Média)",
            line=dict(color=cor, width=3),
            marker=dict(size=8),
            hovertemplate="Ano: %{x}<br>Média: %{y:.2f}<br>Nº escolas: %{customdata}<extra></extra>",
            customdata=sub["qtd"]
        ))
        # Linha pontilhada da mediana
        fig.add_trace(go.Scatter(
            x=sub["ANO"],
            y=sub["mediana"],
            mode="lines",
            name=f"{tipo} (Mediana)",
            line=dict(color=cor, width=1.5, dash="dot"),
            showlegend=True,
            hovertemplate="Ano: %{x}<br>Mediana: %{y:.2f}<extra></extra>"
        ))
        
    fig.update_layout(
        title=title,
        xaxis_title="Ano",
        yaxis_title=y_label,
        template=CHART_THEME,
        xaxis=dict(tickmode="linear", dtick=2),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_city_comparison_bar(df: pd.DataFrame, metric_col: str, title: str, x_label: str, top_n=20):
    # Seleciona municípios que tenham ao menos uma escola cívico-militar para comparabilidade direta
    cm_cities = df[df["TIPO_GESTAO"] == "Cívico-Militar"]["NO_MUNICIPIO"].unique()
    df_cities = df[df["NO_MUNICIPIO"].isin(cm_cities)].dropna(subset=[metric_col, "TIPO_GESTAO"])
    
    if df_cities.empty:
        return None
        
    city_summary = df_cities.groupby(["NO_MUNICIPIO", "TIPO_GESTAO"])[metric_col].agg(["mean", "count"]).reset_index()
    # Pega os municípios com maior número de escolas
    top_cities = df_cities.groupby("NO_MUNICIPIO")["ID_ESCOLA"].nunique().sort_values(ascending=False).head(top_n).index
    city_summary = city_summary[city_summary["NO_MUNICIPIO"].isin(top_cities)]
    
    fig = px.bar(
        city_summary,
        x="mean",
        y="NO_MUNICIPIO",
        color="TIPO_GESTAO",
        barmode="group",
        color_discrete_map=COLOR_MAP,
        orientation="h",
        title=title,
        labels={"NO_MUNICIPIO": "Município", "mean": x_label, "TIPO_GESTAO": "Tipo de Gestão"},
        template=CHART_THEME,
        custom_data=["count"]
    )
    fig.update_traces(
        hovertemplate="Município: %{y}<br>Média: %{x:.2f}<br>Nº escolas: %{customdata[0]}<extra></extra>"
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        yaxis=dict(categoryorder="total ascending"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_ideb_vs_projecao_scatter(df: pd.DataFrame, title: str):
    df_valid = df.dropna(subset=["IDEB_OBSERVADO", "IDEB_PROJECAO", "TIPO_GESTAO"])
    if df_valid.empty:
        return None
        
    df_valid["ATINGIU_META"] = np.where(df_valid["IDEB_OBSERVADO"] >= df_valid["IDEB_PROJECAO"], "Atingiu/Superou", "Abaixo da Meta")
    
    fig = px.scatter(
        df_valid,
        x="IDEB_PROJECAO",
        y="IDEB_OBSERVADO",
        color="TIPO_GESTAO",
        symbol="ATINGIU_META",
        color_discrete_map=COLOR_MAP,
        opacity=0.75,
        hover_name="NO_ESCOLA",
        hover_data=["NO_MUNICIPIO", "ETAPA", "ANO"],
        title=title,
        labels={
            "IDEB_PROJECAO": "Meta do IDEB (Projeção INEP)",
            "IDEB_OBSERVADO": "IDEB Observado",
            "TIPO_GESTAO": "Tipo de Gestão",
            "ATINGIU_META": "Meta do IDEB"
        },
        template=CHART_THEME
    )
    
    # Linha diagonal 1:1
    min_val = min(df_valid["IDEB_PROJECAO"].min(), df_valid["IDEB_OBSERVADO"].min())
    max_val = max(df_valid["IDEB_PROJECAO"].max(), df_valid["IDEB_OBSERVADO"].max())
    fig.add_shape(
        type="line", line=dict(dash="dash", color="gray", width=1.5),
        x0=min_val, y0=min_val, x1=max_val, y1=max_val
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_school_map(df: pd.DataFrame, metric_col: str, metric_label: str, title: str):
    """
    Gera mapa interativo de dispersão geográfica das escolas do Paraná com suporte defensivo ao Plotly 6/7.
    """
    df_valid = df.dropna(subset=["LATITUDE", "LONGITUDE", "TIPO_GESTAO"]).copy()
    if df_valid.empty:
        return None

    hover_dict = {
        "NO_MUNICIPIO": True,
        "TIPO_GESTAO": True,
        "ETAPA": True,
        "LATITUDE": False,
        "LONGITUDE": False
    }
    if metric_col in df_valid.columns:
        hover_dict[metric_col] = ":.2f"

    map_kwargs = dict(
        data_frame=df_valid,
        lat="LATITUDE",
        lon="LONGITUDE",
        color="TIPO_GESTAO",
        color_discrete_map=COLOR_MAP,
        hover_name="NO_ESCOLA",
        hover_data=hover_dict,
        zoom=6.0,
        center={"lat": -24.75, "lon": -51.5},
        title=title,
        opacity=0.8
    )

    if hasattr(px, "scatter_map"):
        fig = px.scatter_map(map_style="carto-positron", **map_kwargs)
    else:
        fig = px.scatter_mapbox(mapbox_style="carto-positron", **map_kwargs)

    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1)
    )
    return fig

