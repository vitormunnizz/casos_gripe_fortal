import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho do arquivo CSV
file_path = "INFLUD24-CE.csv"

try:
    df = pd.read_csv(file_path)

    # Dicionários de Substituição dos Dados
    substituicoes = {
        "VACINA": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "VACINA_COV": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "HOSPITAL": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "UTI": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "EVOLUCAO": {1: "Cura", 2: "Óbito", 3: "Óbito por outras causas", 9: "Ignorado"},
        "CLASSI_FIN": {
            1: "SRAG por influenza",
            2: "SRAG por outro vírus respiratório",
            3: "SRAG por outro agente etiológico",
            4: "SRAG não especificado",
            5: "SRAG por covid-19",
        },
        "AMOSTRA": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "PCR_RESUL": {
            1: "Detectável",
            2: "Não Detectável",
            3: "Inconclusivo",
            4: "Não Realizado",
            5: "Aguardando Resultado",
            9: "Ignorado",
        },
        "PCR_ADENO": {1: "Marcado", 0: "Não Marcado"},
        "PCR_BOCA": {1: "Marcado", 0: "Não Marcado"},
        "PCR_METAP": {1: "Marcado", 0: "Não Marcado"},
        "PCR_RINO": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA1": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA2": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA3": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA4": {1: "Marcado", 0: "Não Marcado"},
        "PCR_SARS2": {1: "Marcado", 0: "Não Marcado"},
        "PCR_VSR": {1: "Marcado", 0: "Não Marcado"},
        "PCR_OUTRO": {1: "Marcado", 0: "Não Marcado"},
        "RES_AN": {
            1: "Positivo",
            2: "Negativo",
            3: "Inconclusivo",
            4: "Não Realizado",
            5: "Aguardando Resultado",
            9: "Ignorado",
        },
        "AN_ADENO": {1: "Marcado", 0: "Não Marcado"},
        "AN_PARA1": {1: "Marcado", 0: "Não Marcado"},
        "AN_PARA2": {1: "Marcado", 0: "Não Marcado"},
        "AN_PARA3": {1: "Marcado", 0: "Não Marcado"},
        "AN_SARS2": {1: "Marcado", 0: "Não Marcado"},
        "AN_VSR": {1: "Marcado", 0: "Não Marcado"},
        "AN_OUTRO": {1: "Marcado", 0: "Não Marcado"},
        "CRITERIO": {
            1: "Laboratorial",
            2: "Clínico Epidemiológico",
            3: "Clínico",
            4: "Clínico Imagem",
        },
        "TP_IDADE": {1: "Dia", 2: "Mês", 3: "Ano"},
        "CS_SEXO": {1: "Masculino", 2: "Feminino", 9: "Ignorado"},
    }

    # Aplicando as Substituições no DataFrame
    df.replace(substituicoes, inplace=True)

    # Substituindo Valores Nulos nas Colunas numéricas por 0
    df[df.select_dtypes(include=['number']).columns] = df.select_dtypes(
        include=['number']).fillna(0)

    # Substituindo Valores Nulos nas Colunas de Tipo Objeto por "Indefinido"
    df[df.select_dtypes(include=['object']).columns] = df.select_dtypes(
        include=['object']).fillna("Indefinido")

    # Substituindo Valores float por int
    df[df.select_dtypes(include=['float']).columns] = df.select_dtypes(
        include=['float']).astype('int')

    # Filtrando as linhas onde SG_UF_NOT é igual a 'CE'
    df_filtrado_regional = df.loc[df['ID_REGIONA']
                                  == '1 CRES FORTALEZA'].reset_index(drop=True)

    # Criando nova coluna 'QTD_HAT' com as quantidades de habitantes das cidades
    habitantes = {'FORTALEZA': 2428678}

    df_filtrado_regional['QTD_HAT'] = df_filtrado_regional['ID_MUNICIP'].map(
        habitantes)

    # Título do Painel
    st.title("Painel de Indicadores")

    if st.checkbox("Exibir Indicadores Epidemiológicos"):

        # Lista de Colunas a Manter para Epidemiológicos
        colunas_para_manter = [
            'ID_MUNICIP', 'CLASSI_FIN', 'CRITERIO', 'NU_IDADE_N', 'CS_SEXO',
            'VACINA', 'VACINA_COV', 'SEM_PRI', 'QTD_HAT'
        ]

        df_filtrado_Epidemiologicos = df_filtrado_regional[colunas_para_manter]

        # Contar as ocorrências de cada valor em 'ID_MUNICIP'
        municipios_count = df_filtrado_Epidemiologicos['ID_MUNICIP'].value_counts().iloc[0]

        # Definindo as faixas etárias Jovens (0-19), Adultos (20-59), Idosos (60+)
        bins = [0, 19, 59, 150]
        labels = ['Jovens', 'Adultos', 'Idosos']

        # Criando a nova coluna com a faixa etária
        df_filtrado_Epidemiologicos['FAIXA_ETARIA'] = pd.cut(
            df_filtrado_Epidemiologicos['NU_IDADE_N'], bins=bins, labels=labels)

        st.write(f'O total de casos de síndrome respiratória aguda graves hospitalizados em Fortaleza é de {municipios_count} casos')

        # Calculando a Taxa de incidência por habitantes

        incid_hab = (5125 / 2428678) * 100000

        st.write(f'Taxa de incidência de casos é de {incid_hab:.2f} por 100.000 habitantes')

        st.write('Gráfico da distribuição de casos por sexo')

        # Criando gráfico (Casos de Gripe por Sexo e Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos,
                      x='ID_MUNICIP', hue='CS_SEXO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Casos por Sexo e Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de Casos', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Sexo', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico da distribuição de casos por faixa etária')

        # Criando o gráfico (Casos de Gripe por Faixa Etária e Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos,
                      x='ID_MUNICIP', hue='FAIXA_ETARIA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Casos por Faixa Etária e Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de Casos', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Faixa Etária', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico do histórico vacinal')

        # Criando o gráfico (Vacinação por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos,
                      x='ID_MUNICIP', hue='VACINA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação por local da residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade Pessoas Vacidas', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Vacinação', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico do histórico vacinal de COVID')

        # Criando o gráfico (Vacinação de COVID por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos,
                      x='ID_MUNICIP', hue='VACINA_COV', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação de COVID por local da residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade Pessoas Vacidas contra COVID', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Vacinação contra COVID', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico da quantidade de casos por semana epidemiológica (1 até 52)')

        # Criando gráfico (Casos de Gripe por Semana Epidemiológica Cruz (1 até 52))
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos,
                      x='ID_MUNICIP', hue='SEM_PRI', palette='Set1', ax=ax, legend=False)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Casos por Semana Epidemiológica Cruz (1 até 52)',
                     fontsize=16, color='white')
        ax.set_xlabel('Semana Epidemiológica', color='white')
        ax.set_ylabel('Quantidade de Casos', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

    if st.checkbox("Exibir Indicadores Vigilância Laboratorial"):

        # Lista de colunas a manter para Vigilância Laboratorial
        colunas_para_manter = [
            'ID_MUNICIP', 'AMOSTRA', 'PCR_RESUL', 'RES_AN'
        ]

        df_filtrado_vig_lab = df_filtrado_regional[colunas_para_manter]

        # Filtrar as linhas onde SG_UF_NOT é igual a 'CE' e restaurar o índice
        df_filtrado_regional_teste_realizado = df_filtrado_regional.loc[df_filtrado_regional['AMOSTRA'] == 'Sim'].reset_index(drop=True)

        
        teste_realizado = df_filtrado_regional_teste_realizado['AMOSTRA'].value_counts().iloc[0]
        
        st.write(f'Número de testes realizados de síndrome respiratória aguda graves em Fotaleza é de {teste_realizado} testes')

        st.write('Gráfico dos resultados do teste de RT-PCR')

        # Criando gráfico (Resultado do Teste de RT-PCR por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vig_lab,
                      x='ID_MUNICIP', hue='PCR_RESUL', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Resultado do Teste de RT-PCR por Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de Teste de RT-PCR', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Resultado do Teste de RT-PCR', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico dos resultados do teste Antigênico')

        # Criando gráfico (Resultado do Teste Antigênico por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vig_lab,
                      x='ID_MUNICIP', hue='RES_AN', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Resultado do Teste Antigênico por Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de Teste de Antigênico', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Resultado do Teste de Antigênico', frameon=False,
                  fontsize=12, title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

    # Filtro de "Mortalidade"
    if st.checkbox("Exibir Indicadores de Mortalidade"):

        # Lista de colunas a manter para Mortalidade
        colunas_para_manter = [
            'ID_MUNICIP', 'CLASSI_FIN', 'EVOLUCAO'
        ]

        df_filtrado_mortalidade = df_filtrado_regional[colunas_para_manter]

        st.write('Gráfico do desfechos clínicos dos casos')

        # Criando gráfico (Desfechos Clínicos por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_mortalidade,
                      x='ID_MUNICIP', hue='EVOLUCAO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Desfechos Clínicos por Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de Cura, Óbito...', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Desfechos Clínicos', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        # Filtrar dados de óbitos
        df_obito = df_filtrado_mortalidade.loc[
            (df_filtrado_mortalidade['EVOLUCAO'] == 'Óbito') |
            (df_filtrado_mortalidade['EVOLUCAO'] == 'Óbito por outras causas')
        ]
        
        # Contar o número de registros de obitos
        num_obitos = df_obito.shape[0]
        
        st.write(f'A quantidade de óbitos é de {num_obitos} óbitos')

        # Calculando a Taxa de incidência de obitos por 100.000 habitantes
        incid_hab = (294 / 2428678) * 100000

        st.write(f'Taxa de incidência de óbitos é de {incid_hab:.2f} por 100.000 habitantes')

    # Filtro de "Clínicos e Assistenciais"
    if st.checkbox("Exibir Indicadores de Hospitalização e UTI"):

        # Lista de colunas a manter para Clínicos e Assistenciais
        colunas_para_manter = [
            'ID_MUNICIP', 'HOSPITAL', 'UTI', 'EVOLUCAO'
        ]

        df_filtrado_clinico_assistencia = df_filtrado_regional[colunas_para_manter]

        st.write('Gráfico da Taxa de hospitalização')

        # Criando gráfico (Taxa de hospitalização por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_clinico_assistencia,
                      x='ID_MUNICIP', hue='HOSPITAL', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Taxa de hospitalização por Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de hospitalização', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Taxa de hospitalização', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico da Taxa de hospitalização em UTI')

        # Criando gráfico (Taxa de hospitalização em UTI por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_clinico_assistencia,
                      x='ID_MUNICIP', hue='UTI', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Taxa de hospitalização em UTI por Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de hospitalização em UTI', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Taxa de hospitalização em UTI', frameon=False,
                  fontsize=12, title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico do desfechos clínicos dos casos')

        # Criando gráfico (Desfechos Clínicos por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_clinico_assistencia,
                      x='ID_MUNICIP', hue='EVOLUCAO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Desfechos Clínicos por Local da Residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade de Cura, Óbito...', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Desfechos Clínicos', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

    if st.checkbox("Exibir Indicadores de Vacinação e Tempo de Resposta"):

        # Lista de colunas a manter para Clínicos e Assistenciais
        colunas_para_manter = [
            'ID_MUNICIP', 'VACINA', 'VACINA_COV', 'DT_SIN_PRI', 'DT_NOTIFIC', 
            'DT_COLETA', 'DT_PCR'
        ]

        df_filtrado_vacinacao_resposta = df_filtrado_regional[colunas_para_manter]

        st.write('Gráfico do histórico vacinal')

        # Criando gráfico (Vacinação por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vacinacao_resposta,
                      x='ID_MUNICIP', hue='VACINA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação por local da residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade Pessoas Vacidas', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Vacinação', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        st.write('Gráfico do histórico vacinal de COVID')

        # Criando o gráfico (Vacinação de COVID por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vacinacao_resposta,
                      x='ID_MUNICIP', hue='VACINA_COV', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação de COVID por local da residência',
                     fontsize=16, color='white')
        ax.set_xlabel('Local da Residência (Cidade)', color='white')
        ax.set_ylabel('Quantidade Pessoas Vacidas contra COVID', color='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='white')
        ax.legend(title='Vacinação contra COVID', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        st.pyplot(fig)

        # Converte as colunas para o tipo datetime
        df_filtrado_vacinacao_resposta['DT_SIN_PRI'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_SIN_PRI'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vacinacao_resposta['DT_NOTIFIC'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_NOTIFIC'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vacinacao_resposta['DT_COLETA'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_COLETA'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vacinacao_resposta['DT_PCR'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_PCR'], errors='coerce', format='%d/%m/%Y')


        # Subtração das datas
        df_filtrado_vacinacao_resposta['DIFERENCA_NOTIFIC_SIN_PRI'] = df_filtrado_vacinacao_resposta['DT_NOTIFIC'] - \
            df_filtrado_vacinacao_resposta['DT_SIN_PRI']

        df_filtrado_vacinacao_resposta['DIFERENCA_NOTIFIC_SIN_PRI'] = df_filtrado_vacinacao_resposta['DIFERENCA_NOTIFIC_SIN_PRI'].dt.days

        
        df_filtrado_vacinacao_resposta['DIFERENCA_test_result'] = df_filtrado_vacinacao_resposta['DT_PCR'] - \
            df_filtrado_vacinacao_resposta['DT_COLETA']

        df_filtrado_vacinacao_resposta['DIFERENCA_test_result'] = df_filtrado_vacinacao_resposta['DIFERENCA_test_result'].dt.days


        diferenca_NOTIFIC_SIN_PRI = df_filtrado_vacinacao_resposta.groupby('ID_MUNICIP')['DIFERENCA_NOTIFIC_SIN_PRI'].mean().round()
        valor_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.loc['FORTALEZA']
        
        st.write(f'O tempo médio do aparecimento de sintomas até a notificação em Fortaleza é de {valor_diferenca_NOTIFIC_SIN_PRI} dias')
        
        diferenca_coleta_PCR = df_filtrado_vacinacao_resposta.groupby('ID_MUNICIP')['DIFERENCA_test_result'].mean().round()
        diferença_test_result = diferenca_coleta_PCR.loc['FORTALEZA']

        st.write(f'O tempo médio entre coleta do teste e resultado é de {diferença_test_result} dia')

except FileNotFoundError:
    st.error(f"O arquivo no caminho '{
             file_path}' não foi encontrado. Verifique o caminho e tente novamente.")
