##### CÓDIGO PARA FORMATAR ARQUIVO DE AERÓDROMOS PÚBLICOS - BASE DA ANAC #####

##### PARTE 1 - Fazer o download da base de dados de AD Públicos e AD Privados do site da ANAC por meio de WebScraping #####
##### OBS: o chromedriver precisar estar atualizado conforme a versão do Chrome: site para baixar o chromedriver: https://chromedriver.chromium.org/downloads | copiar o arquivo.exe e colar na pasta Arquivo de programas x86 do disco C#####
##### OBS²: caso os arquivos baixados não vão para o diretório especificado em "download.default_directory", será necessário salvar os arquivos na pasta onde o código de nome: "codigo_it200_part2" está salvo

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

dir = r"D:\15.1 Mestrado\1.4 - Semestre\IT200 - Infraestrutura Aeronáutica\it200_codigo\\"           # esse vai ser o direório para onde o arquivo vai após o download. Para ir para outro diretório, modificar o caminho.

chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": dir,         # precisa colocar a letra r antes e os dois \\ no final do caminho para poder ir para a pasta desejada
         "directory_upgrade": True
         }
chrome_options.add_experimental_option('prefs', prefs)

path = Service("C:\Program Files (x86)\chromedriver.exe")                        # local onde o chromedriver está instalado. Se estiver instalado em outro local, modificar o caminho.
driver = webdriver.Chrome(service=path, options=chrome_options)

## Entrar no site que tem a base de dados
url = "https://www.gov.br/anac/pt-br/assuntos/regulados/aerodromos/lista-de-aerodromos-civis-cadastrados"
driver.get(url)         # acessar o site


### ACEITAR OS COOKIES DO SITE DA ANAC
try:
    cookie = driver.find_element(by=By.XPATH, value="//*[@id='lgpd-cookie-banner-janela']/div[2]/button")           # aceitar os cookies da página
    cookie.click()
    print('Cookies aceitos com sucesso! \n')
except NoSuchElementException:
    print("Não foi possível encotrar o caminho para aceitar os cookies! \n")
time.sleep(2)       # tempo de 2 segundoS para executar o outro click

### DOWNLOAD DO ARQUIVO DE AERÓDROMOS PRIVADOS
try:
    ad_priv = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[1]/main/div[2]/div/div[5]/div/p[3]/a[1]")           # clicar no link dos aeródromos privados
    ad_priv.click()
    print('Download da base de aeródromos públicos realizado com sucesso! \n')
except NoSuchElementException:
    print("Não foi possível encontrar o caminho do arquivo para realizar o Download da base de aeródromos públicos!")

time.sleep(2)

### DOWNLOAD DO ARQUIVO DE AERÓDROMOS PRIVADOS
try:
    ad_pub = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[1]/main/div[2]/div/div[5]/div/p[4]/a[1]")           # clicar no link dos aeródromos públicos
    ad_pub.click()
    print('Download da base de aeródromos privados realizado com sucesso!')
except NoSuchElementException:
    print("Não foi possível encontrar o caminho do arquivo para realizar o Download da base de aeródromos privados!")


time.sleep(2)
driver.close()      # para fechar a página web aberta após clicar nos links
