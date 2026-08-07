import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Conversor Porto Seguro",
    page_icon="📄"
)

st.title("📄 Conversor Porto Seguro")
st.write("Faça upload do PDF para converter em Excel.")

arquivo = st.file_uploader(
    "Selecione o PDF",
    type=["pdf"]
)

if arquivo is not None:

    todas_tabelas = []

    with pdfplumber.open(arquivo) as pdf:

        for numero_pagina, pagina in enumerate(pdf.pages, start=1):

            tabelas = pagina.extract_tables()

            st.write(
                f"Página {numero_pagina}: {len(tabelas)} tabela(s) encontrada(s)"
            )

            for tabela in tabelas:

                if tabela:

                    tabela_corrigida = []

                    for linha in tabela:

                        nova_linha = []

                        for celula in linha:

                            if celula:

                                celula = str(celula)
                                celula = celula.replace("\n", " ")
                                celula = " ".join(celula.split())

                            nova_linha.append(celula)

                        tabela_corrigida.append(nova_linha)

                    df = pd.DataFrame(tabela_corrigida)

                    todas_tabelas.append(df)

    st.write(f"Total de tabelas encontradas: {len(todas_tabelas)}")

    if len(todas_tabelas) > 0:

        resultado = pd.concat(
            todas_tabelas,
            ignore_index=True
        )

        resultado = resultado.replace("", pd.NA)
        resultado = resultado.dropna(how="all")
        resultado = resultado.dropna(axis=1, how="all")
        resultado = resultado.reset_index(drop=True)

        st.success("✅ Conversão concluída!")

        st.dataframe(resultado.head(50))

        excel = BytesIO()

        resultado.to_excel(
            excel,
            index=False,
            engine="openpyxl"
        )

        excel.seek(0)

        st.download_button(
            "📥 Baixar Excel",
            data=excel,
            file_name="Resultado_PDF_Porto.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:

        st.error("Nenhuma tabela encontrada no PDF.")
