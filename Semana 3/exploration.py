import streamlit as st
import pandas as pd
import numpy as np
import base64


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href


def main():
    st.image('logo.png', width=200)
    st.title('Resposta desafio: Semana 2')
    file_in = st.file_uploader('Escolha um arquivo "csv":', type='csv')
    if file_in is not None:
        df = pd.read_csv(file_in)

        st.markdown('**Número de linhas e colunas**')
        lin, col = df.shape
        st.markdown(str(lin) + ' linhas e ' + str(col) + ' colunas')

        max_lin_slider = df.shape[0] if df.shape[0] < 100 else 100
        slider = st.slider('Escolha a quantidade de linhas para espiar:',
                           min_value=1, max_value=max_lin_slider, value=10)
        st.dataframe(df.head(slider))

        st.markdown('**Informações das colunas:**')
        exploration = pd.DataFrame({'types': df.dtypes,
                                    'NA #': df.isna().sum(),
                                    'NA %': (df.isna().sum() /
                                             lin*100)})
        exploration.reset_index(inplace=True)
        exploration.rename(columns={'index': 'names'}, inplace=True)
        st.dataframe(exploration)

        st.markdown('**Detalhes das colunas numéricas:**')
        st.dataframe(df.describe())

        st.markdown('**Quantidade de Tipos**')
        st.write(exploration.types.value_counts())

        st.markdown('**Nomes das colunas do tipo object:**')
        st.text(list(exploration[exploration['types'] == 'object']
                     ['names']))

        st.markdown('**Nomes das colunas do tipo int64:**')
        st.text(list(exploration[exploration['types'] == 'int64']
                     ['names']))

        st.markdown('**Nomes das colunas do tipo float64:**')
        st.text(list(exploration[exploration['types'] == 'float64']
                     ['names']))

        st.subheader('Análise univariada')
        selected_column = st.selectbox('Escolha uma coluna para análise univariada:',
                                       list(exploration[exploration['types'] != 'object']['names']))
        hist_bin = 100 if (df[selected_column].nunique() <= 100)\
            else round(df[selected_column].nunique() / 10)
        hist_values = np.histogram(df[selected_column], bins=hist_bin)
        hist_frame = pd.DataFrame(hist_values[0], index=hist_values[1][:-1])
        st.bar_chart(hist_frame)

        col_describe = df[selected_column].describe()
        col_more = pd.Series({'skew': df[selected_column].skew(),
                              'kurtosis': df[selected_column].kurtosis()},
                             name=col_describe.name)
        st.write(pd.concat([col_more, col_describe]))

        st.subheader('Cálculos das colunas numéricas:')
        typeCalc = {'Média': '.mean()',
                    'Mediana': '.median()',
                    'Desvio Padrão': '.std()'}
        calc_choosed = st.selectbox('Escolha o tipo de cálculo para as colunas numéricas:',
                                    ['', 'Média', 'Mediana', 'Desvio Padrão'])
        if calc_choosed is not '':
            exec("st.table(df[exploration[exploration['types']!='object']['names']]{0})"
                 .format(typeCalc[calc_choosed]))

        st.markdown('**Percentual dos dados faltantes:**')
        st.table(exploration[exploration['NA #'] != 0]
                 [['types', 'NA %']])

        st.subheader('Imputação de dados numéricos faltantes')
        percentage = st.slider('Escolha o limite percentual faltante das colunas a serem prenchidas:',
                               min_value=0, max_value=100, value=0)
        col_list = list(
            exploration[exploration['NA %'] <= percentage]['names'])

        select_method = st.radio('Escolha um método de preenchimento:',
                                 ('Média', 'Mediana'))
        imputed_df = df[col_list].fillna(df[col_list].mean() if
                                         select_method == 'Média' else df[col_list].median())
        impputed_exploration = pd.DataFrame({'names': imputed_df.columns,
                                             'types': imputed_df.dtypes,
                                             'NA #': imputed_df.isna().sum(),
                                             'NA %': (imputed_df.isna().sum() / lin * 100)})
        st.table(
            impputed_exploration[impputed_exploration['types'] != 'object']['NA %'])

        st.subheader('Arquivo com os dados imputados:')
        st.markdown(get_table_download_link(
            imputed_df), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
