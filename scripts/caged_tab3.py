# -*- coding: utf-8 -*-
"""caged_tab3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bGuAhMaLzQIEKHjK6JRLuZTsqKk8FnVx
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

df_tab3 = excel_to_pandas2(url_tabela,'caged_tabela3.xlsx', 'Tabela 3',[5])

temp = excel_to_pandas2(url_tabela,'caged_tabela3.xlsx', 'Tabela 3',[1])

temp1 = temp.columns.to_list()[1:2]
print(temp1)
data = str(temp1).split('-')[2].strip().replace(' DE ','_').replace(']','').replace("'",'').lower()
data

df_tab3

df_tab3.rename(columns={'Unnamed: 1':'UF', 'Unnamed: 3':'Município'}, inplace=True)

colunas = ['UF', 'Município','Admissões',	'Desligamentos',	'Saldos',	'Variação Relativa (%)']

df_tab3= df_tab3[1:][colunas].dropna()

df_tab3.loc[df_tab3.UF != 'Não identificado']
df_tab3['Admissões'] = df_tab3['Admissões'].astype('int')
df_tab3['Desligamentos'] = df_tab3['Desligamentos'].astype('int')
df_tab3['Saldos'] = df_tab3['Saldos'].astype('int')
df_tab3['data'] = data

df_tab3['Variação Relativa (%)'] = df_tab3['Variação Relativa (%)'].replace('---',0)
df_tab3['Variação Relativa (%)'] = df_tab3['Variação Relativa (%)'].astype('float')
df_tab3['Variação Relativa (%)'] = np.round(df_tab3['Variação Relativa (%)'],2)

#print(df_tab3.info())
df_tab3.rename(columns={'UF':'uf', 'Município: 3':'municipio', 'Admissões':'admissoes', 'Desligamentos': 'desligamentos', 'Saldos': 'saldos', 'Variação Relativa (%)': 'variacao_relativa'}, inplace=True)

#df_tab3.to_csv("df_caged_tab3_"+data+".csv", index=False, encoding='utf-8')
df_tab3.to_csv("df_caged_tab3.csv", index=False, encoding='utf-8')
df_tab3.to_parquet("df_caged_tab3.parquet",engine='pyarrow')
