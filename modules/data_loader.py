from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@st.cache_data
def load_tidy_data() -> pd.DataFrame:
    file_path = DATA_DIR / "escolas_tidy.parquet"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}. Execute preprocess_data.py primeiro.")
    df = pd.read_parquet(file_path)
    return df

@st.cache_data
def load_wide_data(etapa_slug: str) -> pd.DataFrame:
    file_path = DATA_DIR / f"escolas_wide_{etapa_slug}.parquet"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return pd.read_parquet(file_path)

def get_filter_options(df: pd.DataFrame):
    anos = sorted(df["ANO"].dropna().unique().tolist(), reverse=True)
    etapas = sorted(df["ETAPA"].dropna().unique().tolist())
    redes = sorted(df["REDE"].dropna().unique().tolist())
    municipios = sorted(df["NO_MUNICIPIO"].dropna().unique().tolist())
    tipos_gestao = ["Todas", "Cívico-Militar", "Não Cívico-Militar"]
    return {
        "anos": anos,
        "etapas": etapas,
        "redes": redes,
        "municipios": municipios,
        "tipos_gestao": tipos_gestao,
    }

def apply_filters(
    df: pd.DataFrame,
    anos=None,
    etapas=None,
    redes=None,
    municipios=None,
    tipo_gestao="Todas",
    search_query=""
) -> pd.DataFrame:
    filtered = df.copy()
    
    if anos:
        if isinstance(anos, (list, tuple)):
            filtered = filtered[filtered["ANO"].isin(anos)]
        else:
            filtered = filtered[filtered["ANO"] == anos]
            
    if etapas:
        if isinstance(etapas, (list, tuple)):
            filtered = filtered[filtered["ETAPA"].isin(etapas)]
        else:
            filtered = filtered[filtered["ETAPA"] == etapas]
            
    if redes:
        filtered = filtered[filtered["REDE"].isin(redes)]
        
    if municipios:
        filtered = filtered[filtered["NO_MUNICIPIO"].isin(municipios)]
        
    if tipo_gestao and tipo_gestao != "Todas":
        filtered = filtered[filtered["TIPO_GESTAO"] == tipo_gestao]
        
    if search_query:
        q = search_query.strip().lower()
        filtered = filtered[
            filtered["NO_ESCOLA"].astype(str).str.lower().str.contains(q) |
            filtered["ID_ESCOLA"].astype(str).str.contains(q)
        ]
        
    return filtered
