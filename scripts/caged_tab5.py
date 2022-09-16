# -*- coding: utf-8 -*-
"""caged_tab5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Oj4ViV0loPSCyzf2vULitf7xtnrTDA1J
"""

import pandas as pd
import numpy as np
import requests
import io
from bs4 import BeautifulSoup
import urllib.request

url_caged = "http://pdet.mte.gov.br/novo-caged"
parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib.request.urlopen(url_caged)
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
url_tabela='http://pdet.mte.gov.br'
for link in soup.find_all('a', href=True):
  if "tabelas.xlsx" in link['href']:
        #print("Link:",link['href'])
        #print("Url tabela: ", url_tabela+str(link['href']))
        url_tabela = url_tabela+str(link['href'])

print(url_tabela)

def excel_to_pandas2(URL, local_path, sheet, header):
    resp = requests.get(URL)
    with open(local_path, 'wb') as output:
        output.write(resp.content)
    df = pd.read_excel(local_path,sheet_name=sheet,header=header)
    return df

def excel_to_pandas(URL, local_path, sheet, header,colunas):
    resp = requests.get(URL)
    with open(local_path, 'wb') as output:
        output.write(resp.content)
    df = pd.read_excel(local_path,sheet_name=sheet,header=header, usecols= colunas)
    return df

colunas = ['Mês',	'Estoque',	'Admissões',	'Desligamentos',	'Saldos',	'Variação Relativa (%)']

df_tab5 = excel_to_pandas(url_tabela,'caged_tabela5_original.xlsx', 'Tabela 5', 4, colunas)

df_tab5.dropna(inplace=True)

primeiro_mes = df_tab5['Mês'].head(1).tolist()
#
ultimo_mes = df_tab5['Mês'].tail(1).tolist()

ultimo_mes

mes = str(primeiro_mes).split('/')[0].replace("['",'')
#
ano = str(primeiro_mes).split('/')[1].replace("']",'')
#
primeiro_mes = mes+'_'+ano
#
#
mes = str(ultimo_mes).split('/')[0].replace("['",'')
#
ano = str(ultimo_mes).split('/')[1].replace("']",'')
#
ultimo_mes = mes+'_'+ano

print("de ",primeiro_mes, " a ",ultimo_mes)

data = str(primeiro_mes)+'_a_'+str(ultimo_mes)

df_tab5['Estoque'] = df_tab5['Estoque'].astype('int32')
#
df_tab5['Admissões'] = df_tab5['Admissões'].astype('int32')
#
df_tab5['Desligamentos'] = df_tab5['Desligamentos'].astype('int32')
#
df_tab5['Saldos'] = df_tab5['Saldos'].astype('int32')
#
df_tab5['Variação Relativa (%)'] = df_tab5['Variação Relativa (%)'].replace('----',0)
df_tab5['Variação Relativa (%)'] = np.round(df_tab5['Variação Relativa (%)'],2)

#df_tab5.to_csv("df_caged_tab5_"+data+'.csv', index=False, encoding='utf-8')
df_tab5.to_csv("df_caged_tab5.csv", index=False, encoding='utf-8')