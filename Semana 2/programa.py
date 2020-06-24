import streamlit as sl
import pandas as pd
import base64


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href


def main():
    sl.image('logo.png', width=200 )
    sl.title( 'Resposta desafio: Semana 2')
    file_in = sl.file_uploader('Escolha um arquivo "csv":', type='csv')
    if file_in is not None :
        df = pd.read_csv(file_in)
        
        sl.markdown('**Número de linhas e colunas**')
        lin, col = df.shape
        sl.markdown(str(lin)+ ' linhas e '+ str(col)+ ' colunas')

        max_lin_slider = df.shape[0] if df.shape[0] < 150 else 150
        slider = sl.slider('Escolha a quantidade de linhas para espiar:',
                            min_value=1, max_value=max_lin_slider, value=10)
        sl.dataframe(df.head(slider))

        sl.subheader('Médias das colunas:')
        aux = df.iloc[0:slider]
        sl.table(df.groupby('species').agg({'sepal_length':'mean',
                                            'sepal_width':'mean',
                                            'petal_length':'mean',
                                            'petal_width':'mean'}) )

        sl.markdown('**Nome das colunas**')
        sl.markdown(list(df.columns))
        
        exploration = pd.DataFrame({'names': df.columns, 
                                    'types': df.dtypes, 
                                    'NA #': df.isna().sum(), 
                                    'NA %': (df.isna().sum()/
                                            lin*100)})

        sl.markdown('**Quantidade de Tipos**')
        sl.write(exploration.types.value_counts())

        sl.markdown('**Nomes das colunas do tipo int64:**')
        sl.markdown(list(exploration[exploration['types'] == 'int64']
                ['names']))

        sl.markdown('**Nomes das colunas do tipo float64:**')
        sl.markdown(list(exploration[exploration['types'] == 'float64']
                ['names']))

        sl.markdown('**Nomes das colunas do tipo object:**')
        sl.markdown(list(exploration[exploration['types'] == 'object']
                ['names']))

        sl.markdown('**Percentual dos dados faltantes:**')
        sl.table(exploration[exploration['NA #'] != 0 ]
                [['types', 'NA %']])

        sl.subheader('Imputação de dados numéricos faltantes')
        percentage = sl.slider('Escolha o limite percentual faltante das colunas a serem prenchidas:', 
                min_value=0, max_value=100, value=0)
        col_list = list(exploration[exploration['NA %'] <= percentage]['names'])
        
        select_method = sl.radio('Escolha um método de preenchimento:', 
                ('Média', 'Mediana'))
        imputed_df = df[col_list].fillna(df[col_list].mean() if\
                select_method == 'Média' else df[col_list].median())
        impputed_exploration = pd.DataFrame({'names': imputed_df.columns,
                                            'types': imputed_df.dtypes,
                                            'NA #': imputed_df.isna().sum(),
                                            'NA %': (imputed_df.isna().sum() / lin * 100)})
        sl.table(impputed_exploration[impputed_exploration['types'] != 'object']['NA %'])

        sl.subheader('Arquivo com os dados imputados:')
        sl.markdown(get_table_download_link(imputed_df), unsafe_allow_html=True)


if __name__ == "__main__":
    main()