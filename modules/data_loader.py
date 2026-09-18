from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"

@st.cache_data(show_spinner="Carregando cadastro de escolas do Paraná...")
def load_cadastro() -> pd.DataFrame:
    """
    Carrega o cadastro unificado de todas as 5.966 escolas do Paraná.
    """
    file_path = PROCESSED_DIR / "escolas_cadastro.parquet"
    if not file_path.exists():
        file_path = DATA_DIR / "escolas_cadastro.parquet"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_parquet(file_path)
    df["codigo_inep"] = df["codigo_inep"].astype(int)
    return df

@st.cache_data(show_spinner="Carregando matriz histórica temporal CCM...")
def load_historico_ano() -> pd.DataFrame:
    """
    Carrega a matriz histórica anualizada (1.407 registros: 201 escolas x 7 anos 2020-2026).
    """
    file_path = PROCESSED_DIR / "historico_ccm_por_ano.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    df["codigo_inep"] = df["codigo_inep"].astype(int)
    df["ano"] = df["ano"].astype(int)
    return df

@st.cache_data(show_spinner="Carregando eventos documentais auditados...")
def load_historico_eventos() -> pd.DataFrame:
    """
    Carrega a cronologia auditada de eventos e editais CCM (384 eventos).
    """
    file_path = PROCESSED_DIR / "historico_ccm_eventos.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    # Trata codigo_inep que pode ser nulo para atos gerais
    df["codigo_inep_num"] = pd.to_numeric(df["codigo_inep"], errors="coerce")
    return df

@st.cache_data(show_spinner="Carregando catálogo de evidências documentais...")
def load_historico_evidencias() -> pd.DataFrame:
    """
    Carrega os metadados dos atos normativos e evidências documentais.
    """
    file_path = PROCESSED_DIR / "historico_ccm_evidencias.csv"
    if not file_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    df["codigo_inep_num"] = pd.to_numeric(df["codigo_inep"], errors="coerce")
    return df

@st.cache_data(show_spinner="Carregando microdados de proficiência SAEB...")
def load_saeb_tidy() -> pd.DataFrame:
    """
    Carrega a série histórica do SAEB do Paraná (2005 a 2023).
    """
    file_path = PROCESSED_DIR / "saeb" / "saeb_escolas_parana_tidy.parquet"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_parquet(file_path)
    df["ID_ESCOLA"] = df["ID_ESCOLA"].astype(int)
    df["ANO_SAEB"] = df["ANO_SAEB"].astype(int)
    return df

@st.cache_data(show_spinner="Carregando indicadores de rendimento escolar...")
def load_rendimento_tidy() -> pd.DataFrame:
    """
    Carrega as taxas de aprovação, reprovação e abandono do Censo Escolar (2017 a 2023).
    """
    file_path = PROCESSED_DIR / "rendimento" / "rendimento_escolas_parana_tidy.parquet"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_parquet(file_path)
    df["ID_ESCOLA"] = df["ID_ESCOLA"].astype(int)
    df["ANO"] = df["ANO"].astype(int)
    return df

@st.cache_data(show_spinner="Carregando série histórica do IDEB...")
def load_ideb_tidy() -> pd.DataFrame:
    """
    Carrega o IDEB observado e metas projetadas pelo MEC (2005 a 2023).
    """
    file_path = PROCESSED_DIR / "ideb" / "ideb_escolas_parana_tidy.parquet"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_parquet(file_path)
    df["ID_ESCOLA"] = df["ID_ESCOLA"].astype(int)
    df["ANO_IDEB"] = df["ANO_IDEB"].astype(int)
    return df

@st.cache_data(show_spinner="Carregando base integrada de séries históricas...")
def load_integrated_serie() -> pd.DataFrame:
    """
    Carrega a base integrada de séries históricas para as escolas CCM auditadas.
    """
    file_path = PROCESSED_DIR / "ccm_saeb_rendimento_ideb_serie_completa.parquet"
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_parquet(file_path)
    df["codigo_inep"] = df["codigo_inep"].astype(int)
    return df

@st.cache_data(show_spinner="Carregando base de dados legada...")
def load_tidy_data() -> pd.DataFrame:
    """
    Mantido para compatibilidade reversa com visualizações legadas.
    """
    file_path = DATA_DIR / "escolas_tidy.parquet"
    if not file_path.exists():
        return pd.DataFrame()
    return pd.read_parquet(file_path)

@st.cache_data
def load_wide_data(etapa_slug: str) -> pd.DataFrame:
    """
    Mantido para compatibilidade reversa com visualizações legadas.
    """
    file_path = DATA_DIR / f"escolas_wide_{etapa_slug}.parquet"
    if not file_path.exists():
        return pd.DataFrame()
    return pd.read_parquet(file_path)

def get_filter_options(df: pd.DataFrame):
    """
    Retorna listas únicas para preenchimento de seletores.
    """
    anos = sorted(df["ANO"].dropna().unique().tolist(), reverse=True) if "ANO" in df.columns else []
    etapas = sorted(df["ETAPA"].dropna().unique().tolist()) if "ETAPA" in df.columns else []
    redes = sorted(df["REDE"].dropna().unique().tolist()) if "REDE" in df.columns else []
    municipios = sorted(df["NO_MUNICIPIO"].dropna().unique().tolist()) if "NO_MUNICIPIO" in df.columns else []
    return {
        "anos": anos,
        "etapas": etapas,
        "redes": redes,
        "municipios": municipios,
        "tipos_gestao": ["Todas", "Cívico-Militar", "Não Cívico-Militar"],
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
    """
    Aplica filtros padronizados mantendo a consistência dos dados.
    """
    filtered = df.copy()
    
    ano_col = "ANO" if "ANO" in filtered.columns else ("ano" if "ano" in filtered.columns else None)
    if anos and ano_col:
        if isinstance(anos, (list, tuple)):
            filtered = filtered[filtered[ano_col].isin(anos)]
        else:
            filtered = filtered[filtered[ano_col] == anos]
            
    etapa_col = "ETAPA" if "ETAPA" in filtered.columns else ("etapa_ensino" if "etapa_ensino" in filtered.columns else None)
    if etapas and etapa_col:
        if isinstance(etapas, (list, tuple)):
            filtered = filtered[filtered[etapa_col].isin(etapas)]
        else:
            filtered = filtered[filtered[etapa_col] == etapas]
            
    rede_col = "REDE" if "REDE" in filtered.columns else ("rede_ensino" if "rede_ensino" in filtered.columns else None)
    if redes and rede_col:
        filtered = filtered[filtered[rede_col].isin(redes)]
        
    mun_col = "NO_MUNICIPIO" if "NO_MUNICIPIO" in filtered.columns else ("municipio" if "municipio" in filtered.columns else None)
    if municipios and mun_col:
        filtered = filtered[filtered[mun_col].isin(municipios)]
        
    gestao_col = "TIPO_GESTAO" if "TIPO_GESTAO" in filtered.columns else ("status_ccm_atual" if "status_ccm_atual" in filtered.columns else None)
    if tipo_gestao and tipo_gestao != "Todas" and gestao_col:
        if gestao_col == "TIPO_GESTAO":
            filtered = filtered[filtered["TIPO_GESTAO"] == tipo_gestao]
        elif gestao_col == "status_ccm_atual":
            if tipo_gestao == "Cívico-Militar":
                filtered = filtered[filtered["status_ccm_atual"].isin(["SIM", "FUTURO_2026"])]
            elif tipo_gestao == "Não Cívico-Militar":
                filtered = filtered[filtered["status_ccm_atual"].isin(["NAO_CCM", "INDETERMINADO"])]
                
    if search_query:
        q = search_query.strip().lower()
        nome_col = "NO_ESCOLA" if "NO_ESCOLA" in filtered.columns else ("nome_escola" if "nome_escola" in filtered.columns else None)
        inep_col = "ID_ESCOLA" if "ID_ESCOLA" in filtered.columns else ("codigo_inep" if "codigo_inep" in filtered.columns else None)
        
        cond_nome = filtered[nome_col].astype(str).str.lower().str.contains(q, na=False) if nome_col else False
        cond_inep = filtered[inep_col].astype(str).str.contains(q, na=False) if inep_col else False
        filtered = filtered[cond_nome | cond_inep]
        
    return filtered

@st.cache_data(show_spinner="Carregando base comparativa integrada...")
def load_comparisons_dataset() -> pd.DataFrame:
    """
    Carrega e unifica os dados para a seção de Comparações:
    - Base censitária e SAEB (tidy de 2005 a 2023)
    - Metadados cadastrais e auditoria dos editais CCM
    - Indicadores complementares de rendimento (reprovação e abandono)
    """
    df_tidy = load_tidy_data()
    if df_tidy.empty:
        return pd.DataFrame()
        
    df_cad = load_cadastro()
    df_rend = load_rendimento_tidy()
    
    # Merge com metadados do cadastro auditado
    cad_cols = ["codigo_inep", "status_ccm_atual", "is_ccm", "ano_inicio_ccm", "nre"]
    cad_subset = df_cad[[c for c in cad_cols if c in df_cad.columns]].drop_duplicates(subset=["codigo_inep"])
    df = df_tidy.merge(cad_subset, left_on="ID_ESCOLA", right_on="codigo_inep", how="left")
    
    # Merge com dados do Censo para reprovação e abandono
    rend_cols = ["ID_ESCOLA", "ANO", "ETAPA", "TAXA_REPROVACAO", "TAXA_ABANDONO"]
    rend_avail = [c for c in rend_cols if c in df_rend.columns]
    if len(rend_avail) == len(rend_cols):
        rend_subset = df_rend[rend_avail].drop_duplicates(subset=["ID_ESCOLA", "ANO", "ETAPA"])
        df = df.merge(rend_subset, on=["ID_ESCOLA", "ANO", "ETAPA"], how="left")
        
    # Colunas derivadas
    if "TAXA_APROVACAO" in df.columns:
        df["TAXA_NAO_APROVACAO"] = 100.0 - pd.to_numeric(df["TAXA_APROVACAO"], errors="coerce")
        
    if "IDEB_OBSERVADO" in df.columns and "IDEB_PROJECAO" in df.columns:
        df["DELTA_META_IDEB"] = pd.to_numeric(df["IDEB_OBSERVADO"], errors="coerce") - pd.to_numeric(df["IDEB_PROJECAO"], errors="coerce")
        
    return df

@st.cache_data(show_spinner=False)
def load_ccm_mapping() -> pd.DataFrame:
    """
    Carrega o mapeamento oficial das escolas Cívico-Militares do Paraná (306 unidades).
    """
    file_path = DATA_DIR / "mapeamento_escolas_civico_militares.csv"
    if not file_path.exists():
        return pd.DataFrame()
    return pd.read_csv(file_path, sep=";")

def get_school_ccm_status(codigo_inep: int, esc_row: pd.Series = None) -> tuple[bool, int | None, str]:
    """
    Retorna (is_ccm: bool, ano_transicao: int | None, coorte_label: str) para uma escola.
    Identifica de forma robusta e integrada as coortes:
    - 2021: Programa Inicial (Lei nº 20.338/2020 / relação oficial dos 306 colégios)
    - 2024: Expansão da Rede (Editais 2023 / 106 escolas ativas em 2024)
    - 2026: Expansão Futura (Editais 2025 / 33 escolas com implantação em 2026)
    """
    if esc_row is None:
        try:
            df_cad = load_cadastro()
            sub = df_cad[df_cad["codigo_inep"] == codigo_inep]
            esc_row = sub.iloc[0] if not sub.empty else {}
        except Exception:
            esc_row = {}

    ano_inicio = esc_row.get("ano_inicio_ccm") if hasattr(esc_row, "get") else None
    if pd.notna(ano_inicio) and str(ano_inicio).strip() in ["2021", "2024", "2026"]:
        ano = int(str(ano_inicio).strip())
        if ano == 2021:
            return True, 2021, "Coorte 2021 (Programa Inicial)"
        elif ano == 2024:
            return True, 2024, "Coorte 2024 (Expansão)"
        elif ano == 2026:
            return True, 2026, "Coorte 2026 (Consulta Pública)"

    # Checar na base oficial dos 306 colégios cívico-militares do PR
    df_map = load_ccm_mapping()
    if not df_map.empty and "ID_ESCOLA" in df_map.columns:
        if codigo_inep in df_map["ID_ESCOLA"].dropna().astype(int).values:
            return True, 2021, "Coorte 2021 (Programa Inicial)"

    # Checar se no cadastro auditado consta como CCM
    if hasattr(esc_row, "get") and bool(esc_row.get("is_ccm", False)):
        return True, 2024, "Coorte 2024 (Expansão Auditada)"

    return False, None, "Escola Regular (Não Cívico-Militar)"

