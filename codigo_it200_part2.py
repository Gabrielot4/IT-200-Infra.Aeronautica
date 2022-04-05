##### CÓDIGO PARA FORMATAR ARQUIVO DE AERÓDROMOS PÚBLICOS - BASE DA ANAC #####


##### PARTE 2 - Ler os arquivos baixados
##### Leitura dos CSV baixados pelo procedimento de WebScraping acima
##### OBS: após executar o código, dois arquivos são criados no diretório que este código está salvo
##### OB: se quiser executar o código novamente, é preciso excluir esses dois arquivos criados
##### OBS: abrir os arquivos CSV, excluir a primeira linha de cada um deles (caso o método skiprows=1 não funcione) e salvá-los em .xlsx >> não precisa mais

import os
import pandas as pd
import re
import time

inicio = time.time()                                                                                                # começa a contar o tempo de processamento

##### Identificar os arquivos CSV que estão no diretório onde está salvo este código
lista_dos_arquivos_csv = []                                                                                          # lista que vai conter os nomes dos arquivos xlsx
for files in os.listdir('.'):                                                                                        # arquivos devem estar no diretorio onde está salvo esse código
    if files.endswith('.csv'):                                                                                       # se o arquivo terminar com .csv
        lista_dos_arquivos_csv.append(files)                                                                         # adiciono o arquivo com o nome na lista
print(f'Estes são os CSV no diretório atual: {lista_dos_arquivos_csv} \n')

lista_das_bases_csv = []                                                    # lista que vai conter os dataframes das bases de dados baixadas da ANAC
for x in lista_dos_arquivos_csv:
    data = pd.read_csv(x, sep=';', skiprows=1)                              # separador dos arquivos é ';'
    data = pd.DataFrame(data)
    lista_das_bases_csv.append(data)

    print('\n \033[1;30;43m Visualização da lista que contém os DataFrames: \033[m \n ', lista_das_bases_csv)


    ############################ FORMATAÇÃO DOS DADOS ############################


    for w in range(0,len(lista_das_bases_csv)):

        # aqui pode fazer um IF como condição de ser uma base de dados específica. Ex: se for de aeródromos públicos, segue o código abaixo, senão segue outr (ai vou precisar fazer isso)

        data = lista_das_bases_csv[w]                                                       # salvar cada dataframe presente na lista separadamente
        data = data.fillna("NA")
        print(f'\n \033[1;30;43m Visualização do DataFrame {w}, de nome {lista_dos_arquivos_csv[w]}: \033[m \n ', data)

        """############## LIMPAR DADOS: REMOVER CARACTERES ESPECIAIS E SUBSTITUI-LOS POR "_" ##############

        punctuation = lambda x: re.sub('[%s]' % re.escape(string.punctuation), "_", x)  # remove pontuações de qualquer tipo das strings e as substitui por nada "_"

        data = [data[col].map(punctuation).str.replace(" ", "_").str.lower() for col in data.columns]  # aplica as funções lambda acima em cada coluna, conforma o loop itera sobre as colunas do dataframe, e deixa tudo minúsculo
        data = pd.DataFrame(data).transpose()  # precisa transpor, senão os atributos viram linhas e vice-versa
        data[cols] = data[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))  # remove os acentos das palavras
"""
        ############## COORDENADAS ##############
        ###### 1: Remover espaços existentes nas coordenadas

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


        print(f'\n \033[1;30;43m Visualização do DataFrame {w} de nome {lista_dos_arquivos_csv[w]} formatado: \033[m \n ', data)


        ############## EXPORTAR DATAFRAME PARA EXCEL ##############

        data.to_excel(f'{lista_dos_arquivos_csv[w]}_formatado.xlsx', index=False)                                       # index=False é para não sair com uma coluna com núemro das linhas
        data.to_csv(f'{lista_dos_arquivos_csv[w]}_formatado.csv', index=False, encoding='utf-8-sig', sep=';')               # sep=';' para salvar os dados já separados


fim = time.time()  # fim do tempo de processamento
print('\n')
print('Tempo de Processamento [s]: ', fim - inicio)





