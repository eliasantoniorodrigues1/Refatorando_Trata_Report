import datetime
import re
import os
import csv


def define_referencia_produto(dicionario):
    """
        Essa função é responsável por definir os limites de um produto.
        Ex: produto 1 inicia na posicao 150  e  finaliza na posição 300
            produto 2 inicia na posicao 301  e  finaliza na posição 400
        Essa função define o fim do primeiro produto como sendo o ínicio do segundo, ficando assim:
            produto 1 inicia na posicao 150  e  finaliza na posição 301
            produto 2 inicia na posicao 301  e  finaliza na posição 400
            Isso foi feito para garantir que eu não pegaria a data de outro produto, ou a nota de outro
            produto e assim por diante.
    """
    next = 1
    i = 0
    dict_list = list(dicionario.values())
    t = len(dict_list)
    for i in range(t):
        next = i + 1
        if next >= t:
            next = t - 1
        dict_list[i]['ref_final'] = dict_list[next]['ref_inicial']
    return dict_list


def executa_expressao_regular(arquivo):
    """
        Esse trecho de código executa as expressões regulares trazendo no seu retorno
        uma lista de código, descricao, referencia,  data, nota e uma lista de lista contendo os valores daquela linha.
    """
    regexp_produto = re.compile(r'(\|)(Produto: )(\d+)(\s+)(-?)(.*\b)', flags=re.M)
    regexp_ref_data = re.compile(r'(?<=[|])\d+?/\d+?/\d+', flags=re.M)
    regexp_nota = re.compile(r'(?<=\d{2}/\d{2}/\d{2}\|)\d{6}\d?', flags=re.M)
    regexp_cliente = re.compile(r'(?<=\d{2}/\d{2}/\d{2}\|).*\b', flags=re.M)
    regexp_valor = re.compile(r'^\|\s+\|[0-9]+.*', flags=re.M)

    with open(arquivo, 'r') as file:
        texto = file.read()
        lista_cod_produto = [produto.group(3).strip() for produto in regexp_produto.finditer(texto)]
        lista_dsc_produto = [produto.group(6).strip() for produto in regexp_produto.finditer(texto)]
        lista_ref_produto = [produto.start() for produto in regexp_produto.finditer(texto)]
        lista_ref_final_produto = [produto.end() for produto in regexp_produto.finditer(texto)]
        produtos = list(zip(lista_cod_produto, lista_dsc_produto, lista_ref_produto, lista_ref_final_produto))
        # ------------------------------------------------------------------------------------------
        lista_datas = [data.group() for data in regexp_ref_data.finditer(texto)]
        lista_referencias = [data.end() for data in regexp_ref_data.finditer(texto)]
        lista_notas = [nota.group() for nota in regexp_nota.finditer(texto)]
        lista_clientes = [str(cliente.group())[str(cliente.group()).find('|') + 1:] for cliente in
                          regexp_cliente.finditer(texto)]
        # ------------------------------------------------------------------------------------------
        lista_valores = [valor.group().split('|') for valor in regexp_valor.finditer(texto)]
        # ------------------------------------------------------------------------------------------
        i = 0
        consolidado = {}
        prod = {}
        for produto in produtos:
            codigo = produto[0]
            descricao = produto[1]
            ref_inicial = produto[2]
            ref_final = produto[3]
            prod['codigo'] = codigo
            prod['descricao'] = descricao
            prod['ref_inicial'] = ref_inicial
            prod['ref_final'] = ref_final
            consolidado[i] = prod.copy()
            i += 1
    return consolidado, lista_referencias, lista_datas, lista_notas, lista_clientes, lista_valores


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    hora_inicio = datetime.datetime.now()
    nome_arquivo = f'ABC-{time_stamp}.csv'
    caminho_completo = os.path.join(BASE_DIR, nome_arquivo)
    arquivo = input('Por favor, digite o nome do arquivo de texto sem a extensão: ')
    arquivo += '.txt'
    print('Processando...', end='')
    # -----------------------------------------------------------------------------------------------
    dict_produtos, referencias, datas, notas, clientes, valores = executa_expressao_regular(arquivo)
    lista_de_produtos = define_referencia_produto(dict_produtos)
    # ------------------------------------------------------------------------------------------------
    """
        Altera o último elemento do dicionário para ter como referencia final a ultima referencia +1 da lista de
        referencias.
        Essa trecho foi feito para resolver o excesso de while que eu havia criado no código anterior com apenas
        um if simples, sendo este inicio < referencia < fim
                - Inicio é a referencia de início do produto
                - Fim é a referência fim do produto já ajustada pela primeira função 
                  desse programa (define_referencia_produto).
    """
    lista_de_produtos[-1]['ref_final'] = referencias[-1] + 1
    # Definição dos cabeçalhos do arquivo CSV.
    cabecalho = ['CODIGO', 'DESCRICAO', 'DATA', 'NOTA', 'CLIENTE', 'TPO', 'CFO', 'VL_CONTABIL',
                 'IPI', 'ICMS', 'CUSTO', 'QUANTIDADE', 'C_UNIT', 'S_QUANTIDADE', 'S_C_UNIT', 'S_TOTAL'
        , 'SALDO_QUANTIDADE', 'SALDO_C_UNIT', 'SALDO_TOTAL']

    with open(nome_arquivo, 'w', newline='') as arquivo:
        escreve = csv.writer(
            arquivo,
            delimiter=';'
        )
        escreve.writerow(cabecalho)
        contador = 0
        for dados in lista_de_produtos:
            inicio = dados['ref_inicial']
            fim = dados['ref_final']
            '''
            Foi observado que quando um produto não tem data, nem saldo as referencias dele não batem com a lista
            de referência, pois ele não tem data, nesse caso o if abaixo irá ignorar ele completamente e não irá
            inseri-lo no arquivo final.
            
            '''
            for i, ref in enumerate(referencias):
                if inicio < ref < fim:
                    txt = f"{dados['codigo']};{dados['descricao']};{datas[i]};{notas[i]};{clientes[i]}" \
                          f";{';'.join([str(v).strip() for v in valores[i][2:]])}"
                    arquivo.write(txt)
                    arquivo.write('\n')
            contador += 1
    delta = str(datetime.datetime.now() - hora_inicio)[:-7]
    print(f'Relatório salvo com sucesso em {caminho_completo}')
    print(f'Tempo total decorrido: {delta}')
