#### CÓDIGO PARA FORMATAR ARQUIVO DE AERÓDROMOS PÚBLICOS - BASE DA ANAC ####
## OBS: ANTES DE RODAR O CÓDIGO, EXCLUIR A PRIMEIRA LINHA DA BASE DE DADOS E SALVAR O ARQUIVO EM FORMATO .XLSX ##

import pandas as pd
import re
import time

inicio = time.time()                    # começa a contar o tempo de processamento

### IMPORTAÇÃO DA BASE DE DADOS E VISUALIZAÇÃO

data = pd.read_excel('AD_PUB.xlsx', sheet_name='AD_PUB', index_col=None)
data = pd.DataFrame(data)
print('\n \033[1;30;43m Visualização do DatFrame: \033[m \n ', data.head())
print('\n \033[1;30;43m Tipos de dados do DatFrame: \033[m \n ',data.dtypes)


##### FORMATAÇÃO DOS DADOS

#### COORDENADAS ####

## 1: Remover espaços existentes nas coordenadas

lat_long = ['LATITUDE', 'LONGITUDE']
remove_space = lambda x: re.sub('\s', "", x)                                        # substitui espaços por nada
data_lat_long = [data[col].map(remove_space) for col in lat_long]                   # colunas de latitude e longitude sem espaços entre as coordenadas
data['LATITUDE'] = data_lat_long[0]                                                 # dataframe original com coordenadas sem espaços
data['LONGITUDE'] = data_lat_long[1]


## 2: Dividir as coordenadas de latitude e longitude e formatá-las para decimais

lats = []
for i in data['LATITUDE']:
    deg, min, sec, n, dir = re.split('[°\'"]', i)                                       # a divisão das coordenadas resulta em 5 'saídas': degrees, minutes, seconds, '', direction
    decimal = (float(deg)+float(min)/60+float(sec)/3600)*(-1 if dir in ['S'] else 1)    # caso a direção seja S, a coordenada em decimal é multiplicada por -1
    lats.append(decimal)
data['LATITUDE'] = lats

longs = []
for i in data['LONGITUDE']:
    deg, min, sec, n, dir = re.split('[°\'"]', i)
    decimal = (float(deg)+float(min)/60+float(sec)/3600)*(-1 if dir in ['W'] else 1)    # caso a direção seja W, a coordenada em decimal é multiplicada por -1
    longs.append(decimal)
data['LONGITUDE'] = longs

#### COLUNAS COM UNIDADES EM METROS ####

cols = [7,12,13,17,18,22,23]                                            # Número das colunas que possuem unidades de medida em metros
remove_unit = lambda x: re.sub("[ m]", '', x)                           # remove as unidades de medida
virg_ponto = lambda x: re.sub("[,]", '.', x)                            # substitui ',' por '.'
string_zero = lambda x: re.sub("[\-]", '0', x)                          # substitui '-' por '0'

data_sem_unit = [data.iloc[:,col].map(remove_unit).map(virg_ponto).map(string_zero).astype(float) for col in cols]          # A saída é uma lista com todas as colunas que tinham ' m', mas agora estão só com números float

for i, j in zip(cols, range(0,7)):                   # esse loop é para substituir as colunas com unidade pelas colunas formatadas, sem unidade
    data.iloc[:,i] = data_sem_unit[j]



#### EXPORTAR DATAFRAME PARA EXCEL ####
data.to_excel('AD_PUB_formatado.xlsx')

fim = time.time()           # fim do tempo de processamento
