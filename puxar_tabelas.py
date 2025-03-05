import pandas as pd
import json
import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

# opções e inicia drive
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

# descobre quais sao os paises
url = 'https://wits.worldbank.org/tariff/trains/en/country/AFG'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
items = soup.find_all("h3",class_="countryHeading")
links = [item.find("a").get("href") for item in items]
paises = [re.search(r"/partner/([A-Z]{3})/", link).group(1) for link in links]

max_tries = 5

# pros EUA: quanto eles cobram de cada pais?
for pais_parceiro in paises:
    tries = 0
    while tries < max_tries: 
        try:
            url = f'https://wits.worldbank.org/tariff/trains/en/country/USA/year/2022/partner/{pais_parceiro}/product/All/pagenumber/1/pageSize/10000'
            driver.get(url)
            botao_baixar = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[5]/div/div/section/div[1]/a'))
            )
            botao_baixar.click()
            print(f"Baixado: {pais_parceiro}")
            break  # sai do loop de tentativas se funcionar

        except Exception as e:
            tries += 1
            print(f"Tentando novamente {pais_parceiro} ({tries}/{max_tries})... Erro: {e}")

            if tries >= max_tries:
                print(f"Pulando {pais_parceiro} após {max_tries} falhas.")
                break  # desiste dps da 3ra tentativa

# pra cada pais: quanto eles cobram dos EUA?
for pais_ref in paises:
    tries = 0
    while tries < max_tries: 
        try:
            url = f'https://wits.worldbank.org/tariff/trains/en/country/{pais_ref}/year/2022/partner/USA/product/All/pagenumber/1/pageSize/10000'
            driver.get(url)
            botao_baixar = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[5]/div/div/section/div[1]/a'))
            )
            botao_baixar.click()
            print(f"Baixado: {pais_ref}")
            break  # sai do loop de tentativas se funcionar

        except Exception as e:
            tries += 1
            print(f"Tentando novamente {pais_ref} ({tries}/{max_tries})... Erro: {e}")

            if tries >= max_tries:
                print(f"Pulando {pais_ref} após {max_tries} falhas.")
                break  # desiste dps da 3ra tentativa
    
time.sleep(5)
driver.close()
print("Concluído! :)")

# agora tem q transferir os arquivos da pasta /Downloads para sua pasta de escolha !