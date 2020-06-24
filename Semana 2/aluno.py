import streamlit as sl

def main() :
    sl.title('Hello World')

    sl.markdown('Testes de Aplicação')

    botao = sl.button('botão')
    if botao:
        sl.markdown('Clicado!')

    check = sl.checkbox('ok')
    if check:
        sl.markdown("Checked!")

    radio = sl.radio('selecione uma opcao:', ['opção 1', 'opção 2'])
    if radio == 'opção  1':
        sl.markdown('Ok opcao 1!')
    else :
        sl.markdown('Ok opcao 2!')

    selectBox = sl.selectbox('Quando:', ['ontem', 'hoje', 'amanhã'])
    if selectBox == 'ontem':
        sl.markdown('ontem')
    elif selectBox ==  'hoje':
        sl.markdown('hoje')
    else:
        sl.markdown('amanhã')

    multiSelect = sl.multiselect('Outra escolha', ['1 escolha', '2 escolha'])
    if multiSelect == '1 escolha':
        sl.markdown('1 - boa escolha')
    if multiSelect == '2 escolha':
        sl.markdown('2 - excelente escolha')

    file_in = sl.file_uploader('Escoha um arquivo ".csv":', type='csv')
    if file_in is not None :
        sl.markdown('Novo arquivo carregado!')



if __name__ == "__main__":
    main()

