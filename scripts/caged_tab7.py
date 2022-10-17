# -*- coding: utf-8 -*-
"""caged_tab7_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FVIx6vMWxRJmnC1jZ5fC5Fq7uojzbP2b
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
        print("Link:",link['href'])
        print("Url tabela: ", url_tabela+str(link['href']))
        url_tabela = url_tabela+str(link['href'])

print(url_tabela)

def excel_to_pandas2(URL, local_path, sheet, header):
    resp = requests.get(URL)
    with open(local_path, 'wb') as output:
        output.write(resp.content)
    df = pd.read_excel(local_path,sheet_name=sheet,header=header)
    return df

"""# Tabela 7"""

df_tab7 = excel_to_pandas2(url_tabela,'caged_tabela7.xlsx', 'Tabela 7', [4,5] )

colunas_tab7 = df_tab7.columns

meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro", "Dezembro"]

colunas_temp = colunas_tab7.to_list()
colunas = []
for i in colunas_temp:
  temp = str(i).replace("/", "'/")
  #print("TEMP:",temp)
  
  var = temp.split(',')[0].lstrip('(').strip().replace("'",'')
  #if (temp != "Unnamed: 0_level_0', 'Unnamed: 0_level_1"):
  #print("Coluna:", var)
  colunas.append(var)

colunas = colunas[2:]

colunas_filtered = []
for i in colunas:
  #print("Coluna:",i)
  temp = i.split('/')[0]
  if temp in meses:
    colunas_filtered.append(i)

col_set = set(colunas_filtered)

lista_uf = df_tab7['Região e UF'][:27].values.tolist()

ufs =[]
for var in lista_uf:
        ufs.append(var)

 # Algumas tabelas tem apenas as coluna de col1: Janeiro/2020
col1 = ['Estoque','Admissões', 'Desligamentos', 'Saldos']
col2 = ['Estoque','Admissões', 'Desligamentos', 'Saldos', 'Variação Relativa (%)']
frames = []
#print("Total de mes/ano:",len(col_set))
for i in col_set:
  try:
      print("Coluna:",i)
      if i == 'Janeiro/2020':
          temp = df_tab7[i][1:27][col1]
          temp['Variação Relativa (%)'] = 0.0
        
      elif i == 'Dezembro/2021':
          temp = df_tab7[i][1:27]
          temp.rename(columns={"Estoque***\n(Estoque de referência de 2022)":'Estoque'}, inplace=True)
          temp = temp[col2]  
      else:
          temp = df_tab7[i][1:27][col2]
      
      mes, ano = i.split('/')
      temp['data'] = i
      temp['mes'] = mes
      temp['ano'] = ano
      temp['uf'] = ufs[1:]
      frames.append(temp)
  except:
    
    print("\n\tError")
    print("Coluna:",i,"\n",temp)
   
df_tab7 = pd.concat(frames)

print(df_tab7.info())

p

#print("Dataset antes de mudar tipo:\n",df_tab7)

df_tab7['Saldos'] = df_tab7['Saldos'].replace('.','')
df_tab7['Saldos'] = df_tab7['Saldos'].astype('int32')
#
df_tab7['Admissões'] = df_tab7['Admissões'].replace('.','')
df_tab7['Admissões'] = df_tab7['Admissões'].astype('int32')
#
df_tab7['Desligamentos'] = df_tab7['Desligamentos'].replace('.','')
df_tab7['Desligamentos'] = df_tab7['Desligamentos'].astype('int32')
#
df_tab7['Estoque'] = df_tab7['Estoque'].replace('.','')
df_tab7['Estoque'] = df_tab7['Estoque'].astype('int32')
#
#df_tab7['Variação Relativa (%)'] = df_tab7['Variação Relativa (%)'].replace('.','')
df_tab7['Variação Relativa (%)'] = df_tab7['Variação Relativa (%)'].astype('float')

x=[]
for i in df_tab7['uf']:
  x.append(','.join(map(str,i)))

df_tab7['uf'] = x

#print(df_tab7.info())

#print("Depois de mudar tipo:\n",df_tab7)

#print("variacao_relativa:", df_tab7['Variação Relativa (%)'])

df_tab7.rename(columns={'Estoque':'estoque','Admissões':'admissoes', 'Desligamentos':'desligamentos', 'Saldos':'saldos', 'Variação Relativa (%)':'variacao_relativa'}, inplace=True)

#print("Colunas:", df_tab7.columns)

colunas = ['estoque', 'admissoes', 'desligamentos','saldos','mes', 'ano']
print("Colunas:\n", colunas)

print("Final:\n",df_tab7['colunas'].head())

df_tab7['colunas'].to_csv('df_caged_tab7.csv', index=False, encoding='latin')

df_tab7['colunas'].to_parquet("df_caged_tab7.parquet",engine='pyarrow')


#print("\nCriado df_caged_tab7.csv")
