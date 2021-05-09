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
        # ------------------------------------------------------------------------------------------
        lista_valores = [valor.group().split('|') for valor in regexp_valor.finditer(texto)]
        # ------------------------------------------------------------------------------------------
        # datas_notas_valores = list(zip(lista_datas, lista_ref_datas, lista_notas, lista_valores))
        # datas_notas_valores = list(zip(lista_datas, lista_ref_datas, lista_notas))
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
    return consolidado, lista_datas, lista_ref_datas


def uni_produtos_datas(dicionario, lista_datas, lista_ref_datas):
    ref_produtos = dicionario
    ref_datas = lista_ref_datas
    datas = lista_datas
    fim_prod = dicionario['ref_final_tratada']
    i = 0
    lista_produtos_datas = []
    for item in ref_produtos:
        if i >= len(datas):
            break
        controle_ref_datas = ref_datas[i]
        if controle_ref_datas > fim_prod:
            while controle_ref_datas > fim_prod:
                # print(i, item['inicio'], item['descricao'], datas[i], ref_datas[i])
                lista_produtos_datas.append(datas[i])
                i += 1
                controle_ref_datas = ref_datas[i]
                if i >= len(ref_datas):
                    break
        else:
            while controle_ref_datas < fim_prod:
                # print(i, item['inicio'], item['descricao'], datas[i], ref_datas[i])
                lista_produtos_datas.append(datas[i])
                i += 1
                controle_ref_datas = ref_datas[i]

    return lista_produtos_datas


# def pega_nota(lista, inicio_produto, fim_produto):
#     lista_notas = [lista[i][2] if inicio_produto < lista[i][1] < fim_produto
#                    else lista[i][2] for i in range(len(lista))]
#     return lista_notas
#
#
# def pega_valor(lista, inicio_produto, fim_produto):
#     lista_valores = [lista[i][3] if inicio_produto < lista[i][1] < fim_produto
#                      else lista[i][3] for i in range(len(lista)) if
#                      inicio_produto < lista[i][1] < fim_produto]
#     return lista_valores


if __name__ == '__main__':
    arquivo = 'teste.txt'
    dict_produtos, lista_datas, ref_datas = trata_produtos(arquivo)
    lista_de_produtos = altera_referencia(dict_produtos)
    consolida_produto = {}
    l = []
    contador = 0
    indice = 0

    for i, dict in enumerate(lista_de_produtos):
        # print(i, dict['codigo'], dict['descricao'], dict['ref_final_tratada'])
        ref_prod = dict['ref_final_tratada']
        l, k = uni_produtos_datas(dict, lista_datas, ref_datas)
        indice = k
        dict['data'] = l

    for dados in lista_de_produtos:
        print(dados)

    # inicio = lista_de_produtos[k]['ref_inicial']
    # fim = lista_de_produtos[k]['ref_final_tratada']
    # l, i = pega_data(datas_notas_valores, inicio, fim, contador)
    # n = pega_nota(datas_notas_valores, inicio, fim)
    # v = pega_valor(datas_notas_valores, inicio, fim)
    # print(i)
    # print(l)
    # contador = i
    # print(n)
    # print(v)

    # consolida_produto['indice'] = k
    # consolida_produto['codigo'] = lista_de_produtos[k]['codigo']
    # consolida_produto['descricao'] = lista_de_produtos[k]['descricao']
