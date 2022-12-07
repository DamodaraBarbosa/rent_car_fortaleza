from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

options = Options()
options.add_argument('window-size= 400, 800')
browser = webdriver.Chrome(options= options)
browser.get('https://www.rentcars.com/pt-br/')
rent_car = BeautifulSoup(browser.page_source, 'html.parser')
timeout = 3

# três segundos para garantir que a página carregue:
sleep(3)

city = 'Fortalez'
search_bar = WebDriverWait(browser, timeout).until(
    EC.presence_of_element_located((By.XPATH, '//input[@translate= "translate"]'))
)
# o nome da cidade é inserido:
search_bar.send_keys(city)

# tempo para que o html carregue e se obtenha o autocomplete:
sleep(3)

autocompletes = browser.find_elements(
    By.XPATH,
    "//ul[@class= 'ui-autocomplete ui-front ui-menu ui-widget ui-widget-content autocomplete-content']//li"
)
# a opção desejada é selecionada:
autocompletes[0].click()

# para fechar o disclaimer:
WebDriverWait(browser, timeout).until(
    EC.presence_of_element_located((By.XPATH, 
    "//*[@id='main-footer']/div[2]/div/a"))
).click()

# para enfim realizar a pesquisa:
WebDriverWait(browser, timeout).until(
    EC.presence_of_element_located((By.XPATH, 
    "//*[@id='formPesquisa']/div[5]/button"))
).click()

# tempo que as opções de carro carreguem:
sleep(30)

print(rent_car.prettify())


# search_buttom = browser.find_element(By.XPATH, '//*[@id="formPesquisa"]/div[5]/button')
# search_buttom.click()

# para clicar na barra de pesquisa:

# sleep(5)
# search = browser.find_element(By.XPATH, '//*[@id="site-content"]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/div/div/div/div[2]/button/div/div/svg/path')
# search.click()

# para inserir o local em que se deseja pesquisar os imóveis:

# air_bnb.send_keys('Fortaleza, Ceará')

