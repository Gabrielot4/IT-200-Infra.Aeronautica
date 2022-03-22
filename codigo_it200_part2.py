##### CÓDIGO PARA FORMATAR ARQUIVO DE AERÓDROMOS PÚBLICOS - BASE DA ANAC #####


##### PARTE 2 - Ler os arquivos baixados
##### Leitura dos CSV baixados pelo procedimento de WebScraping acima
##### OBS: abrir os arquivos CSV, excluir a primeira linha de cada um deles e salvá-los em .xlsx

import os
import pandas as pd
import re
import time

inicio = time.time()                    # começa a contar o tempo de processamento

##### Identificar os arquivos CSV que estão no diretório onde está salvo este código
lista_dos_arquivos = []                                                                                               # lista que vai conter os nomes dos arquivos CSV
for files in os.listdir('.'):                                                                                         # arquivos devem estar no diretorio onde está salvo esse código
    if files.endswith('.xlsx'):                                                                                       # se o arquivo terminar com .csv
        lista_dos_arquivos.append(files)                                                                              # adiciono o arquivo com o nome na lista
print(f'Estes são os CSV no diretório atual: {lista_dos_arquivos} \n')

lista_das_bases_csv = []                            # lista que vai conter os dataframes das bases de dados baixadas da ANAC
for x in lista_dos_arquivos:
    data = pd.read_excel(x, index_col=None)         # leitura das bases de dados
    data = pd.DataFrame(data)                       # transformar as bases de dados em dataframe
    lista_das_bases_csv.append(data)                # adicionar cada dataframe na lista

    print('\n \033[1;30;43m Visualização da lista que contém os DataFrames: \033[m \n ', lista_das_bases_csv)


    ############################ FORMATAÇÃO DOS DADOS ############################

    ############## COORDENADAS ##############

    ###### 1: Remover espaços existentes nas coordenadas

    for w in range(0,len(lista_das_bases_csv)):

        # aqui pode fazer um IF como condição de ser uma base de dados específica. Ex: se for de aeródromos públicos, segue o código abaixo, senão segue outr (ai vou precisar fazer isso)

        data = lista_das_bases_csv[w]                                                       # salvar cada dataframe presente na lista separadamente
        print(f'\n \033[1;30;43m Visualização do DataFrame {w}, de nome {lista_dos_arquivos[w]}: \033[m \n ', data)

        lat_long = ['LATITUDE', 'LONGITUDE']
        remove_space = lambda x: re.sub('\s', "", x)                                        # substitui espaços por nada
        data_lat_long = [data[col].map(remove_space) for col in lat_long]                   # colunas de latitude e longitude sem espaços entre as coordenadas
        data['LATITUDE'] = data_lat_long[0]                                                 # dataframe original com coordenadas sem espaços
        data['LONGITUDE'] = data_lat_long[1]


        ###### 2: Dividir as coordenadas de latitude e longitude e formatá-las para decimais

        lats = []
        for j in data['LATITUDE']:
            deg, min, sec, n, dir = re.split('[°\'"]',j)  # a divisão das coordenadas resulta em 5 'saídas': degrees, minutes, seconds, '', direction
            decimal = (float(deg) + float(min) / 60 + float(sec) / 3600) * (-1 if dir in ['S'] else 1)  # caso a direção seja S, a coordenada em decimal é multiplicada por -1
            lats.append(decimal)
        data['LATITUDE'] = lats

        longs = []
        for k in data['LONGITUDE']:
            deg, min, sec, n, dir = re.split('[°\'"]', k)
            decimal = (float(deg) + float(min) / 60 + float(sec) / 3600) * (-1 if dir in ['W'] else 1)  # caso a direção seja W, a coordenada em decimal é multiplicada por -1
            longs.append(decimal)
        data['LONGITUDE'] = longs

        print('\n')


        ############## RETIRAR UNIDADE DAS COLUNAS COM UNIDADES EM METROS ##############

        cols = [7, 12, 13, 17, 18, 22, 23]  # Número das colunas que possuem unidades de medida em metros
        remove_unit = lambda x: re.sub("[ m]", '', x)  # remove as unidades de medida
        virg_ponto = lambda x: re.sub("[,]", '.', x)  # substitui ',' por '.'
        string_zero = lambda x: re.sub("[\-]", '0', x)  # substitui '-' por '0'

        data_sem_unit = [data.iloc[:, col].map(remove_unit).map(virg_ponto).map(string_zero).astype(float) for col in cols]  # A saída é uma lista com todas as colunas que tinham ' m', mas agora estão só com números float

        for i, j in zip(cols, range(0,7)):                  # esse loop é para substituir as colunas do dataframe com unidades de medida pelas colunas formatadas, sem unidade de medida
            data.iloc[:, i] = data_sem_unit[j]              # exemplo: data.iloc[:,7] = data_sem_unit.iloc[:,0], data.iloc[:,12] = data_sem_unit.iloc[:,1]


        print(f'\n \033[1;30;43m Visualização do DataFrame formatado: \033[m \n ', data)


        ############## EXPORTAR DATAFRAME PARA EXCEL ##############

        data.to_excel(f'AD_PUB_formatado_{w}.xlsx')                 # para cada iteração, um arquivo formatado é salvo

fim = time.time()  # fim do tempo de processamento
print('\n')
print('Tempo de Processamento [s]: ', fim - inicio)





