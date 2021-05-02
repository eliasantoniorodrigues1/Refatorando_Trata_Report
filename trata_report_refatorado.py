import re
import pandas as pd
import os


def altera_referencia(dicionario):
    next = 1
    i = 0
    dict_list = list(dicionario.values())
    t = len(dict_list)
    for i in range(t):
        next = i + 1
        if next >= t:
            next = t - 1
        # Consultas posteriores para conferencia:
        # print(dict_list[i]['codigo'], dict_list[i]['descricao'], dict_list[i]['ref_inicial'],
        #       dict_list[i]['ref_final'], dict_list[next]['ref_inicial'])

        dict_list[i]['ref_final_tratada'] = dict_list[next]['ref_inicial']
    return dict_list


def trata_produtos(arquivo):
    regexp_produto = re.compile(r'(\|)(Produto: )(\d+)(\s+)(-?)(.*\b)', flags=re.M)
    regexp_ref_data = re.compile(r'(?<=[|])\d+?/\d+?/\d+', flags=re.M)
    regexp_nota = re.compile(r'(?<=\d{2}/\d{2}/\d{2}\|)\d{6}\d?', flags=re.M)
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
        lista_ref_datas = [data.end() for data in regexp_ref_data.finditer(texto)]
        lista_notas = [nota.group() for nota in regexp_nota.finditer(texto)]
        datas_notas = list(zip(lista_datas, lista_ref_datas, lista_notas))

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
        # cons_tratado = altera_referencia(consolidado)

    return consolidado, datas_notas


def pega_data(referencia):
    ...


if __name__ == '__main__':
    arquivo = 'Relatorio Completo.V1.TXT'
    dict_produtos, datas_notas = trata_produtos(arquivo)
    teste = altera_referencia(dict_produtos)
    for dados in teste:
        print(teste[0]['codigo'], teste[0]['ref_final_tratada'], end=' ')

        while datas_notas[0][1] < teste[0]['ref_final_tratada']:
            print(datas_notas[0][0])
    # for dados in dict_produtos:
    #     print(dados)
    #
    # for d in datas_notas[0]:
    #     print(d)
    # for valores in dict_produtos.values():
    #     print(valores)
