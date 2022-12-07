from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from time import sleep

options = Options()
options.add_argument('window-size= 400, 800')
browser = webdriver.Chrome(options= options)
browser.get('https://www.rentcars.com/pt-br/')
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
sleep(25)

dict_car = dict()
list_cars = list()
last_height = browser.execute_script('return document.body.scrollHeight')
# a quantidade de carros disponíveis obtida na página é uma string que é fatiada e convertida para int:
cars_count = int(browser.find_element(By.XPATH, '//div[@class= "filter_sort__counter_2M0zUC3N"]').text[:3])

while len(list_cars) <= cars_count:
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    sleep(1)

    new_height = browser.execute_script('return document.body.scrollHeight')

    if new_height == last_height:
        break

    last_height = new_height

    cars = browser.find_elements(By.XPATH, '//section[@id]')

    for index, car in enumerate(cars):
        if index == 5:
            if 'card' in car.get_attribute('id'):
                model = (car.find_element(By.XPATH, '//h2[@data-gtm-event]').text).split()
                dict_car['model'] = model[1]
                dict_car['brand'] = model[0]
                dict_car['category'] = car.find_element(
                    By.XPATH, '//span[@class= "card-result__header-category_3I38Oj2x"]'
                ).text
                rental_img = browser.find_element(By.XPATH, '//div[@class= "rental_1vvswSUn"]//img')
                dict_car['car_rental'] = rental_img.get_attribute('alt')
                dict_car['car_rental_review'] = browser.find_element(
                    By.XPATH, '//span[@class= "review-indice_2AMfvnVl"]'
                ).text

                features = browser.find_elements(By.XPATH, '//ul[@class= "features-list_377lEgCb"]')
                
                list_cars.append(dict_car.copy())

print(list_cars)
print(len(list_cars))

browser.quit()


# search_buttom = browser.find_element(By.XPATH, '//*[@id="formPesquisa"]/div[5]/button')
# search_buttom.click()

# para clicar na barra de pesquisa:

# sleep(5)
# search = browser.find_element(By.XPATH, '//*[@id="site-content"]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/div/div/div/div[2]/button/div/div/svg/path')
# search.click()

# para inserir o local em que se deseja pesquisar os imóveis:

# air_bnb.send_keys('Fortaleza, Ceará')

