import datetime
import re
import pandas as pd
import os
import csv


def altera_referencia(dicionario):
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


def trata_produtos(arquivo):
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
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    nome_arquivo = f'{time_stamp}.csv'
    arquivo = 'teste.txt'
    dict_produtos, referencias, datas, notas, clientes, valores = trata_produtos(arquivo)
    lista_de_produtos = altera_referencia(dict_produtos)
    # Altera o último elemento do dicionário para ter como referencia final a ultima referencia +1 da lista de
    # referencias.
    lista_de_produtos[-1]['ref_final'] = referencias[-1] + 1
    consolida_produto = {}
    codigo = []
    descricao = []
    data = []
    nota = []
    valor = []
    c = []
    cabecalho = ['CODIGO', 'DESCRICAO', 'DATA', 'NOTA', 'CLIENTE', 'TPO', 'CFO', 'VL_CONTABIL',
                 'IPI', 'ICMS', 'CUSTO', 'QUANTIDADE', 'C_UNIT', 'S_QUANTIDADE', 'S_C_UNIT', 'S_TOTAL'
        , 'SALDO_QUANTIDADE', 'SALDO_C_UNIT', 'SALDO_TOTAL']
    with open(nome_arquivo, 'w', newline='') as arquivo:
        escreve = csv.writer(
            arquivo,
            delimiter=';'
            # quotechar='"',
            # quoting=csv.QUOTE_ALL
        )
        escreve.writerow(cabecalho)
        for dados in lista_de_produtos:
            inicio = dados['ref_inicial']
            fim = dados['ref_final']
            # print(dados['codigo'], dados['descricao'])
            for i, ref in enumerate(referencias):
                if inicio < ref < fim:
                    # tpo,cfo,vl_contabil,ipi,icms,custo,quantidade,c_unit,s_quantidade,s_c_unit,s_total,saldo_quantidade,
                    # saldo_c_unit,saldo_total = valores[i]
                    print(valores[i][2:])
                        # f"{dados['codigo']};{dados['descricao']};{datas[i]};{notas[i]};{clientes[i]}{valores[i]}")
                    # txt = f"{dados['codigo']};{dados['descricao']};{datas[i]};{notas[i]};{clientes[i]}{';'.join([str(v).strip() for v in valores[i]])}"
                    # arquivo.write(txt)
                    # arquivo.write('\n')