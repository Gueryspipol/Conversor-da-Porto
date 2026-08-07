import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Conversor da Porto",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Conversor da Porto")
st.write("Faça upload da fatura PDF da Porto e baixe o Excel convertido.")

arquivo = st.file_uploader(
    "Selecione o PDF",
    type=["pdf"]
)

if arquivo is not None:

    todas_tabelas = []

    with pdfplumber.open(arquivo) as pdf:

        for numero_pagina, pagina in enumerate(pdf.pages, start=1):

            tabelas = pagina.extract_tables()

            for tabela in tabelas:

                if tabela:

                    df = pd.DataFrame(tabela)

                    todas_tabelas.append(df)

    if len(todas_tabelas) > 0:

        resultado = pd.concat(
            todas_tabelas,
            ignore_index=True
        )

        # Limpeza básica
        resultado = resultado.replace("", pd.NA)
        resultado = resultado.dropna(how="all")
        resultado = resultado.dropna(axis=1, how="all")
        resultado = resultado.reset_index(drop=True)

        st.success("✅ Conversão concluída!")

        st.dataframe(resultado.head(20))

        excel = BytesIO()

        resultado.to_excel(
            excel,
            index=False,
            engine="openpyxl"
        )

        st.download_button(
            label="📥 Baixar Excel",
            data=excel.getvalue(),
            file_name="Resultado_PDF_Tabela.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:

        st.error("Nenhuma tabela encontrada no PDF.")
