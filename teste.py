import re
import pandas as pd
import os


# # def trata_produtos(arquivo):
# regexep_prod = re.compile(r'(|)(Produto: )(\d+)(\s+)(-?)(.*\b)', flags=re.M)
#
# with open('Relatorio Completo.V1.TXT', 'r') as file:
#     texto = file.read()
#     produtos = []
#     prod = {}
#     for produto in regexep_prod.finditer(texto):
#         prod['descricao'] = produto.group()
#         prod['ref_inicio'] = produto.start()
#         prod['ref_fim'] = produto.end()
#         print(produto.group())
#         # print(produto.start())
#         # print(produto.end())
#         produtos.append(prod.copy())
#         prod.clear()
# # return produtos
lista = [1, 2, 3, 4, 5]
p = 1
t = len(lista)
for i in range(t):
    p = i + 1
    if p >= t:
        p = t - 1
    print(lista[i], lista[p])