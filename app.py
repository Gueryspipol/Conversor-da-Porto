import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Conversor Porto Seguro",
    page_icon="📄",
    layout="wide"
)

# Título
st.title("📄 Conversor Porto Seguro")
st.write("Faça upload da fatura PDF e receba o Excel convertido.")

# Upload do PDF
arquivo = st.file_uploader(
    "Selecione o PDF",
    type=["pdf"]
)

if arquivo is not None:

    st.info("Processando arquivo...")

    todas_tabelas = []

    with pdfplumber.open(arquivo) as pdf:

        for numero_pagina, pagina in enumerate(pdf.pages, start=1):

            tabelas = pagina.extract_tables()

            st.write(
                f"Página {numero_pagina}: "
                f"{len(tabelas)} tabela(s) encontrada(s)"
            )

            for tabela in tabelas:

                if tabela:

                    tabela_corrigida = []

                    for linha in tabela:

                        nova_linha = []

                        for celula in linha:

                            if celula:

                                celula = str(celula)

                                # Troca quebra de linha por espaço
                                celula = celula.replace("\n", " ")

                                # Remove espaços duplicados
                                celula = " ".join(celula.split())

                            nova_linha.append(celula)

                        tabela_corrigida.append(nova_linha)

                    df = pd.DataFrame(tabela_corrigida)

                    todas_tabelas.append(df)

    st.write(
        f"Total de tabelas encontradas: {len(todas_tabelas)}"
    )

    if len(todas_tabelas) > 0:

        resultado = pd.concat(
            todas_tabelas,
            ignore_index=True
   
