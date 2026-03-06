import streamlit as st
import pandas as pd
import re
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(page_title="Extrator de Egressos CAPES", layout="wide")

st.title("📄 Extrator de Dados de Egressos (PDF → CSV)")
st.write(
"""
Carregue um relatório PDF e o aplicativo irá extrair:

• Nome completo do egresso  
• Ano do egresso  
• Nível do egresso (Mestrado/Doutorado)
"""
)

uploaded_file = st.file_uploader("Carregar PDF", type=["pdf"])


# -----------------------------
# Função de extração
# -----------------------------
def extrair_egressos(pdf_file):

    reader = PdfReader(pdf_file)

    registros = []

    for page in reader.pages:

        texto = page.extract_text()

        if texto is None:
            continue

        texto = texto.replace("\r", "\n")

        nomes = re.findall(r"Egresso:\s*(.+)", texto)
        anos = re.findall(r"Ano do Egresso:\s*(\d{4})", texto)
        niveis = re.findall(r"Nível:\s*([A-Za-zÀ-ÿ]+)", texto)

        nomes = [n.strip() for n in nomes]
        anos = [a.strip() for a in anos]
        niveis = [n.strip() for n in niveis]

        n = min(len(nomes), len(anos), len(niveis))

        for i in range(n):
            registros.append(
                {
                    "Nome": nomes[i],
                    "Ano do egresso": anos[i],
                    "Nível do egresso": niveis[i],
                }
            )

    df = pd.DataFrame(registros)
    df = df.drop_duplicates()

    return df


# -----------------------------
# Execução
# -----------------------------
if uploaded_file:

    st.info("Extraindo dados do PDF...")

    df = extrair_egressos(uploaded_file)

    st.success(f"{len(df)} egressos encontrados")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Baixar CSV",
        csv,
        file_name="egressos_extraidos.csv",
        mime="text/csv",
    )
