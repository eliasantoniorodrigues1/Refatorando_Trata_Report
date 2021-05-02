import re
import pandas as pd
import os


def trata_produtos(arquivo):
    regexep_prod = re.compile(r'(|)(Produto: )(\d+)(\s+)(-?)(.*\b)', flags=re.M)

    with open(arquivo, 'r') as file:
        texto = file.read()
        produtos = []
        prod = {}
        for produto in regexep_prod.finditer(texto):
            prod['descricao'] = produto.group()
            prod['ref_inicio'] = produto.start()
            prod['ref_fim'] = produto.end()
            produtos.append(prod.copy())
            prod.clear()
    return produtos


def ref_datas(arquivo):
    regexp_data = re.compile(r'(?<=[|])\d+?/\d+?/\d+', flags=re.M)
    dts = []
    ref_datas = []
    dados = open(arquivo, 'r')
    texto = dados.read()
    dados.close()

    for data in regexp_data.finditer(texto):
        dts.append(data.group())
        ref_datas.append(data.end())
    return dts, ref_datas


def cria_dicionario_produtos(produtos):
    indice = 0
    prox_indice = 1
    stop = len(produtos) - 1
    ref_produtos = []
    dicionario_refs = {}

    for produto in produtos:
        limite_inicio_prod = produtos[indice]["ref_fim"]
        limite_prod = produtos[prox_indice]["ref_inicio"]

        dicionario_refs['descricao'] = produto["descricao"]
        dicionario_refs['inicio'] = limite_inicio_prod
        dicionario_refs['fim'] = limite_prod
        ref_produtos.append(dicionario_refs.copy())

        indice += 1
        prox_indice = indice + 1
        if prox_indice > stop:
            prox_indice = indice
    return ref_produtos


def uni_produtos_datas(lista_dicionario, lista_datas, lista_ref_datas):
    i = 0
    lista_produtos_datas = []
    # print(lista_ref_datas)
    inicio = 0
    datas_do_prod = []
    for item in lista_dicionario:
        limite = item['fim']
        limite_atualizado = len([l for l in lista_ref_datas if l <= limite]) + 1
        datas_do_prod = lista_datas[inicio:limite_atualizado]
        item['datas'] = datas_do_prod
        print(item)
        datas_do_prod.clear()
        inicio = limite_atualizado

    # for ref in lista_ref_datas:
    #     print(ref)
    #
    # print(lista_datas)

        # if i >= len(lista_datas):
        #     break
        # print(lista_ref_datas[i], item['fim'])
        # if lista_ref_datas[i] > item['fim']:
        #     while lista_ref_datas[i] > item['fim']:
        #         print(item)
        #         print(i, item['inicio'], item['descricao'], lista_datas[i], lista_ref_datas[i])
        # #         dsc_prod = item['descricao']
        # #         dd = lista_datas[i]
        # #         ref_dd = lista_ref_datas[i]
        # #         lista_produtos_datas.append(dsc_prod)
        # #         lista_produtos_datas.append(dd)
        # #         lista_produtos_datas.append(ref_dd)
        #         i += 1
        #         if i >= len(lista_ref_datas):
        #             break
        # else:
        #     while item['inicio'] < lista_ref_datas[i] < item['fim']:
        #         print(item)
        #         print(i, item['inicio'], item['descricao'], lista_datas[i], lista_ref_datas[i])
        #         # dsc_prod = item['descricao']
        #         # dd = lista_datas[i]
        #         # ref_dd = lista_ref_datas[i]
        #         # lista_produtos_datas.append(item['descricao'])
        #         # lista_produtos_datas.append(lista_datas[i])
        #         # lista_produtos_datas.append(lista_ref_datas[i])
        #         i += 1



    # for item in ref_produtos:
    #     print(item)
    #     if i >= len(datas):
    #         break
    #
    #     if ref_datas[i] > item['fim']:
    #         while ref_datas[i] > item['fim']:
    #             # print(i, item['inicio'], item['descricao'], datas[i], ref_datas[i])
    #             lista_produtos_datas.append(item['descricao'])
    #             lista_produtos_datas.append(datas[i])
    #             lista_produtos_datas.append(ref_datas[i])
    #             i += 1
    #             if i >= len(ref_datas):
    #                 break
    #     else:
    #         while item['inicio'] < ref_datas[i] < item['fim']:
    #             # print(i, item['inicio'], item['descricao'], datas[i], ref_datas[i])
    #             lista_produtos_datas.append(item['descricao'])
    #             lista_produtos_datas.append(datas[i])
    #             lista_produtos_datas.append(ref_datas[i])
    #             i += 1

    return lista_produtos_datas


def pega_datas(string):
    data = re.search(r'^\|\d{2}/\d{2}/\d{2}', string)
    if data:
        data = data.group()
        # ref_data = data.span
        data = data.replace('|', '')
    return data


def pega_notas(string):
    nota = re.search(r'(?<=\d{2}/\d{2}/\d{2}\|)\d{6}\d?', string)
    if nota:
        nota = nota.group()
    return nota


def pega_clientes(string):
    cliente = re.search(r'(?<=\d{2}/\d{2}/\d{2}\|).*\b', string)
    if cliente:
        cliente = cliente.group()
    return cliente


def pega_valores(string):
    valor = re.search(r'^\|\s+\|[0-9]+.*', string)
    if valor:
        valor = valor.group()
        valor = valor.split('|')
    return valor


def separa_lista(lista_valores, indice):
    """
        indice é o índice da coluna do relatório
    """
    nova_lista = []
    for lista in lista_valores:
        valor_lista = lista[indice]
        nova_lista.append(valor_lista.strip())
    return nova_lista


def salva_relatorio_excel(dicionario):
    df = pd.DataFrame(data=dicionario)
    df.to_excel('Relatorio_Consolidado.xlsx')
    caminho = os.path.abspath('Relatorio_Consolidado.xlsx')
    print(f'Seu relatório foi salvo em "{caminho}" com sucesso!')


def remove_lixo_produto(string):
    expressao = re.compile(r'^(Produto: )([0-9]+)(\s+-\s)(.*)$')
    return re.search(expressao, string).group(2), re.search(expressao, string).group(4)


def insere_dsc_produtos(lista):
    cod_produtos = []
    dsc_produtos = []
    print(lista)
    for d in lista_prod_dts[::3]:
        codigo, descricao = remove_lixo_produto(d)
        cod_produtos.append(codigo)
        dsc_produtos.append(descricao)

    return cod_produtos, dsc_produtos


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    for __root, _dir, files in os.walk(BASE_DIR):
        for file in files:
            if '.txt' in str(file).lower():
                arquivo = str(file)
    # Dados dos produtos
    referencia_produtos = cria_dicionario_produtos(trata_produtos(arquivo))
    # print(referencia_produtos)
    # print(referencia_produtos)  # Até aqui está correto
    d, ref_dts = ref_datas(arquivo)
    # print(ref_dts)
    # Inserindo o nome dos produtos na lista de datas:
    lista_prod_dts = uni_produtos_datas(referencia_produtos, d, ref_dts)
    # print(lista_prod_dts)

    # # ===================================================
    # with open(arquivo, 'r') as file:
    #     consolidado = {}
    #     datas = []
    #     notas = []
    #     clientes = []
    #     valores = []
    #
    #     for linha in file:
    #         # chamada das funções para criação das listas:
    #         data = pega_datas(linha)
    #         nota = pega_notas(linha)
    #         cliente = pega_clientes(linha)
    #         valor = pega_valores(linha)
    #         # -=-=--=-=-=-=-=-=-=-=-=-=-=-==-=
    #         # consolidação do retorno:
    #         if data:
    #             datas.append(data)
    #         if nota:
    #             notas.append(nota)
    #         if cliente:
    #             posicao = cliente.find('|') + 1
    #             clientes.append(cliente[posicao:])
    #         if valor:
    #             valores.append(valor)
    # # # ===================================================
    # # Separando os valores da lista valores por colunas para adicionar ao dataframe
    # tpo = separa_lista(valores, 2)
    # cfo = separa_lista(valores, 3)
    # vl_contabil = separa_lista(valores, 4)
    # ipi = separa_lista(valores, 5)
    # icms = separa_lista(valores, 6)
    # custo = separa_lista(valores, 7)
    # quantidade = separa_lista(valores, 8)
    # c_unit = separa_lista(valores, 9)
    # s_quantidade = separa_lista(valores, 10)
    # s_c_unit = separa_lista(valores, 11)
    # s_total = separa_lista(valores, 12)
    # saldo_quantidade = separa_lista(valores, 13)
    # saldo_c_unit = separa_lista(valores, 14)
    # saldo_total = separa_lista(valores, 15)
    # # ===================================================
    # lista_codigos, lista_descricao_prod = insere_dsc_produtos(lista_prod_dts)
    # print(lista_codigos)
    # consolidado = {'codigo': lista_codigos, 'descricao': lista_descricao_prod, 'data': datas, 'nota': notas,
    #                'cliente': clientes,
    #                'tpo': tpo, 'cfo': cfo,
    #                'vl_contabil': vl_contabil, 'ipi': ipi, 'icms': icms, 'custo': custo, 'quantidade': quantidade,
    #                'c_unit': c_unit, 's_quantidade': s_quantidade, 's_c_unit': s_c_unit, 's_total': s_total,
    #                'saldo_quantidade': saldo_quantidade, 'saldo_c_unit': saldo_c_unit, 'saldo_total': saldo_total}
    # salva_relatorio_excel(consolidado)
