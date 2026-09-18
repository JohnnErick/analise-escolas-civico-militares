import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLOR_MAP = {
    "Cívico-Militar": "#C0392B",              # Vermelho escuro/Terracota sóbrio
    "Não Cívico-Militar": "#2980B9",          # Azul clássico
    "Rede Estadual Regular": "#16A085",       # Verde-azulado sóbrio
    "Mesmo Município (Não-CM)": "#8E44AD",    # Roxo sóbrio
    "Rede Municipal": "#E67E22",              # Laranja sóbrio
    "Média Estadual": "#7F8C8D"               # Cinza neutro
}

CHART_THEME = "plotly_white"

def make_boxplot_comparison(df: pd.DataFrame, metric_col: str, title: str, y_label: str, group_col: str = "TIPO_GESTAO"):
    if group_col not in df.columns or metric_col not in df.columns:
        return None
    df_valid = df.dropna(subset=[metric_col, group_col])
    if df_valid.empty:
        return None
        
    hover_cols = [c for c in ["NO_ESCOLA", "NO_MUNICIPIO", "REDE", "ETAPA", "ANO"] if c in df_valid.columns]
    fig = px.box(
        df_valid,
        x=group_col,
        y=metric_col,
        color=group_col,
        color_discrete_map=COLOR_MAP,
        points="all",
        hover_data=hover_cols,
        title=title,
        labels={group_col: "Grupo", metric_col: y_label},
        template=CHART_THEME
    )
    
    # Adicionar marcador de média com diamante
    means = df_valid.groupby(group_col)[metric_col].mean().reset_index()
    for _, row in means.iterrows():
        fig.add_trace(go.Scatter(
            x=[row[group_col]],
            y=[row[metric_col]],
            mode="markers+text",
            marker=dict(symbol="diamond", size=12, color="black"),
            text=[f"Média: {row[metric_col]:.2f}"],
            textposition="top right",
            name=f"Média ({row[group_col]})",
            showlegend=False
        ))
        
    fig.update_layout(
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_title="",
        yaxis_title=y_label
    )
    return fig

def make_histogram_comparison(df: pd.DataFrame, metric_col: str, title: str, x_label: str, group_col: str = "TIPO_GESTAO"):
    if group_col not in df.columns or metric_col not in df.columns:
        return None
    df_valid = df.dropna(subset=[metric_col, group_col])
    if df_valid.empty:
        return None
        
    hover_cols = [c for c in ["NO_ESCOLA", "NO_MUNICIPIO"] if c in df_valid.columns]
    fig = px.histogram(
        df_valid,
        x=metric_col,
        color=group_col,
        color_discrete_map=COLOR_MAP,
        barmode="overlay",
        marginal="box",
        opacity=0.65,
        title=title,
        labels={group_col: "Grupo", metric_col: x_label},
        template=CHART_THEME,
        hover_data=hover_cols
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_title=x_label,
        yaxis_title="Quantidade de Escolas",
        legend=dict(title="Grupo", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
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

def make_scatter_aprovacao_vs_saeb(
    df: pd.DataFrame,
    saeb_col: str = "SAEB_NOTA_MEDIA",
    saeb_label: str = "Nota Média SAEB (0-10)",
    group_col: str = "TIPO_GESTAO",
    title: str = "Relação: Taxa de Aprovação vs Desempenho SAEB"
):
    if group_col not in df.columns or "TAXA_APROVACAO" not in df.columns or saeb_col not in df.columns:
        return None
    df_valid = df.dropna(subset=["TAXA_APROVACAO", saeb_col, group_col])
    if df_valid.empty:
        return None
        
    hover_cols = [c for c in ["NO_MUNICIPIO", "REDE", "ETAPA", "ANO"] if c in df_valid.columns]
    fig = px.scatter(
        df_valid,
        x="TAXA_APROVACAO",
        y=saeb_col,
        color=group_col,
        color_discrete_map=COLOR_MAP,
        opacity=0.75,
        hover_name="NO_ESCOLA" if "NO_ESCOLA" in df_valid.columns else None,
        hover_data=hover_cols,
        title=title,
        labels={
            "TAXA_APROVACAO": "Taxa de Aprovação Escolar (%)",
            saeb_col: saeb_label,
            group_col: "Grupo"
        },
        template=CHART_THEME
    )
    
    media_aprov = df_valid["TAXA_APROVACAO"].mean()
    media_saeb = df_valid[saeb_col].mean()
    
    fig.add_vline(x=media_aprov, line_dash="dash", line_color="gray", annotation_text=f"Média Aprov.: {media_aprov:.1f}%")
    fig.add_hline(y=media_saeb, line_dash="dash", line_color="gray", annotation_text=f"Média {saeb_label}: {media_saeb:.2f}")
    
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_title="Taxa de Aprovação Escolar (%)",
        yaxis_title=saeb_label,
        legend=dict(title="Grupo", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_grade_approval_bars(df: pd.DataFrame, group_col: str = "TIPO_GESTAO", title: str = "Taxa de Aprovação Média por Série / Ano Escolar"):
    grade_cols = ["TAXA_APROVACAO_1", "TAXA_APROVACAO_2", "TAXA_APROVACAO_3", "TAXA_APROVACAO_4"]
    existing_cols = [c for c in grade_cols if c in df.columns]
    if not existing_cols or group_col not in df.columns:
        return None
        
    df_valid = df.dropna(subset=existing_cols, how="all")
    if df_valid.empty:
        return None
        
    etapa_predominante = df_valid["ETAPA"].mode()[0] if "ETAPA" in df_valid.columns and not df_valid["ETAPA"].empty else ""
    
    if "Médio" in str(etapa_predominante):
        label_map = {
            "TAXA_APROVACAO_1": "1ª Série (EM)",
            "TAXA_APROVACAO_2": "2ª Série (EM)",
            "TAXA_APROVACAO_3": "3ª Série (EM)",
            "TAXA_APROVACAO_4": "4ª Série (EM/Téc.)"
        }
    elif "Iniciais" in str(etapa_predominante):
        label_map = {
            "TAXA_APROVACAO_1": "1º/2º Ano (AI)",
            "TAXA_APROVACAO_2": "3º Ano (AI)",
            "TAXA_APROVACAO_3": "4º Ano (AI)",
            "TAXA_APROVACAO_4": "5º Ano (AI)"
        }
    else:
        label_map = {
            "TAXA_APROVACAO_1": "6º Ano (AF)",
            "TAXA_APROVACAO_2": "7º Ano (AF)",
            "TAXA_APROVACAO_3": "8º Ano (AF)",
            "TAXA_APROVACAO_4": "9º Ano (AF)"
        }
        
    records = []
    for col in existing_cols:
        sub = df_valid.dropna(subset=[col, group_col])
        if sub.empty:
            continue
        means = sub.groupby(group_col)[col].agg(media="mean", contagem="count").reset_index()
        for _, r in means.iterrows():
            records.append({
                "Série / Ano": label_map.get(col, col),
                "Grupo": r[group_col],
                "Taxa de Aprovação Média (%)": r["media"],
                "Amostra de Escolas": r["contagem"]
            })
            
    if not records:
        return None
        
    df_plot = pd.DataFrame(records)
    fig = px.bar(
        df_plot,
        x="Série / Ano",
        y="Taxa de Aprovação Média (%)",
        color="Grupo",
        barmode="group",
        color_discrete_map=COLOR_MAP,
        title=title,
        template=CHART_THEME,
        custom_data=["Amostra de Escolas"]
    )
    fig.update_traces(
        hovertemplate="Série: %{x}<br>Grupo: %{legendgroup}<br>Aprovação Média: %{y:.2f}%<br>Nº Escolas: %{customdata[0]}<extra></extra>",
        texttemplate="%{y:.1f}%",
        textposition="outside"
    )
    min_val = max(0, df_plot["Taxa de Aprovação Média (%)"].min() - 4)
    fig.update_layout(
        yaxis=dict(range=[min(min_val, 80), 105], ticksuffix="%"),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_approval_brackets_bar(df: pd.DataFrame, group_col: str = "TIPO_GESTAO", title: str = "Distribuição das Escolas por Faixa de Aprovação (%)"):
    if group_col not in df.columns or "TAXA_APROVACAO" not in df.columns:
        return None
    df_valid = df.dropna(subset=["TAXA_APROVACAO", group_col]).copy()
    if df_valid.empty:
        return None
        
    bins = [-np.inf, 85.0, 90.0, 95.0, 98.0, 99.99, 100.01]
    labels = ["< 85%", "85% a 90%", "90% a 95%", "95% a 98%", "98% a 99.9%", "100% (Plena)"]
    df_valid["FAIXA_APROV"] = pd.cut(df_valid["TAXA_APROVACAO"], bins=bins, labels=labels, right=False)
    
    grouped = df_valid.groupby([group_col, "FAIXA_APROV"], observed=False).size().reset_index(name="QTD")
    totals = df_valid.groupby(group_col).size().reset_index(name="TOTAL")
    grouped = grouped.merge(totals, on=group_col)
    grouped["PERCENTUAL"] = (grouped["QTD"] / grouped["TOTAL"]) * 100
    
    fig = px.bar(
        grouped,
        x="FAIXA_APROV",
        y="PERCENTUAL",
        color=group_col,
        barmode="group",
        color_discrete_map=COLOR_MAP,
        title=title,
        labels={"FAIXA_APROV": "Faixa de Aprovação", "PERCENTUAL": "Proporção de Escolas (%)", group_col: "Grupo"},
        template=CHART_THEME,
        custom_data=["QTD", "TOTAL"]
    )
    fig.update_traces(
        hovertemplate="Faixa: %{x}<br>Grupo: %{legendgroup}<br>Percentual: %{y:.1f}%<br>Escolas: %{customdata[0]} de %{customdata[1]}<extra></extra>",
        texttemplate="%{y:.1f}%",
        textposition="outside"
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        yaxis=dict(ticksuffix="%"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def make_time_series(df: pd.DataFrame, metric_col: str, title: str, y_label: str, group_col: str = "TIPO_GESTAO"):
    if group_col not in df.columns or metric_col not in df.columns or "ANO" not in df.columns:
        return None
    df_valid = df.dropna(subset=[metric_col, group_col, "ANO"])
    if df_valid.empty:
        return None
        
    resumo = df_valid.groupby(["ANO", group_col]).agg(
        media=(metric_col, "mean"),
        mediana=(metric_col, "median"),
        qtd=(metric_col, "count")
    ).reset_index()
    
    fig = go.Figure()
    grupos = sorted(resumo[group_col].unique().tolist())
    
    if "Cívico-Militar" in grupos:
        grupos.remove("Cívico-Militar")
        grupos = ["Cívico-Militar"] + grupos
        
    for tipo in grupos:
        sub = resumo[resumo[group_col] == tipo].sort_values("ANO")
        if sub.empty:
            continue
        cor = COLOR_MAP.get(tipo, "#555555")
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

