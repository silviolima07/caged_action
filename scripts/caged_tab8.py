
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

"""# Tabela 8"""

df_tab8 = excel_to_pandas2(url_tabela,'caged_tabela8.xlsx', 'Tabela 8', [4,5] )

colunas_tab8 = df_tab8.columns

uf= df_tab8[['\nUF']][1:-9]
#
municipio = df_tab8[['\nMunicípio']][1:-9]

uf.columns = uf.columns.droplevel()
#
municipio.columns = municipio.columns.droplevel()

uf.rename(columns={'Unnamed: 1_level_1':'UF'}, inplace=True)
#
municipio.rename(columns={'Unnamed: 3_level_1':'Municipio'}, inplace=True)

meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro", "Dezembro"]

colunas_temp = colunas_tab8.to_list()
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

# Algumas tabelas tem apenas as coluna de col1: Janeiro/2020
col1 = ['Estoque','Admissões', 'Desligamentos', 'Saldos']
col2 = ['Estoque','Admissões', 'Desligamentos', 'Saldos', 'Variação Relativa (%)']
frames = []
for i in col_set:
  try:
      print("Coluna:",i)
      if i == 'Janeiro/2020':
          temp = df_tab8[i][1:5570]
          temp['Variação Relativa (%)'] = 0
          #print(temp.head())
          
      elif i == 'Dezembro/2021':
          temp = df_tab8[i][1:5570]  
          temp.columns = col2
          
          
      else:
          temp = df_tab8[i][1:5570][col2]
          #print(temp.head())
      
      mes, ano = i.split('/')
      #temp['data'] = i
      temp['mes'] = mes
      temp['ano'] = ano
      temp['uf'] = uf['UF']
      temp['municipio'] = municipio['Municipio']
      temp.dropna(inplace=True)
      
      frames.append(temp)
    
      
  except:
    
    print("Error")
    #print(temp)

df_tab8 = pd.concat(frames)

#df_tab8.dropna(inplace=True)

#print("Remover cedilha do nome do mes")
#df_tab8['mes'] = df_tab8['mes'].replace('Março','Marco')
#print("Removido cedilha")
#
#print("Coluna mes Março:\n",df_tab8.loc[df_tab8['mes']== 'Marco'])

print("Estoque")
df_tab8 = df_tab8.loc[df_tab8['Estoque'] != '---']
print('Shape:',df_tab8.shape)
#print('Estoque:\n', df_tab8['Estoque'] )                     
                      
#df_tab8['Estoque'] = df_tab8['Estoque'].astype('int32')
#
#print("Saldo")
df_tab8['Saldos'] = df_tab8['Saldos'].astype('int32')
#
#print("Admissoes")
df_tab8['Admissões'] = df_tab8['Admissões'].astype('int32')
#
#print("Desligamentos")
df_tab8['Desligamentos'] = df_tab8['Desligamentos'].astype('int32')
#
#print("Variacão")
df_tab8['Variação Relativa (%)'] = df_tab8['Variação Relativa (%)'].astype('float')
df_tab8['Variação Relativa (%)'] = round(df_tab8['Variação Relativa (%)'],2)


df_tab8.rename(columns={'Estoque':'estoque','Admissões':'admissoes', 'Desligamentos':'desligamentos', 'Saldos':'saldos', 'Variação Relativa (%)':'variacao_relativa'}, inplace=True)

#df_teste = df_tab8

print("Colunas:\n", df_tab8.columns)
print("Final:\n", df_tab8)

colunas = ['estoque', 'admissoes', 'desligamentos', 'saldos', 'variacao_relativa',
       'mes', 'ano', 'uf', 'municipio']

print("Colunas na tab8:\n", colunas)

df_tab8[colunas].to_csv('df_caged_tab8.csv', index=False, encoding='latin-1')

df_tab8[colunas].to_parquet("df_caged_tab8.parquet",engine='pyarrow')
