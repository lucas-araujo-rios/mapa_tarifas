import time
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

# rnaturalearth (paises com pop>10^6) + chatgpt + verificação manual 
paises = [
    "AFG", "AGO", "ALB", "ARE", "ARG", "ARM", "AUS", "AUT", "AZE", "BDI", "BEL", "BEN", "BFA", "BGD", "BGR", "BHR", "BIH",
    "BLR", "BOL", "BRA", "BWA", "CAF", "CAN", "CHE", "CHL", "CHN", "CIV", "CMR", "ZAR", "COG", "COL", "CRI", "CUB", "CYP",
    "CZE", "DEU", "DNK", "DOM", "DZA", "ECU", "EGY", "ERI", "ESP", "EST", "ETH", "FIN", "FRA", "GAB", "GBR", "GEO", "GHA",
    "GIN", "GMB", "GNB", "GNQ", "GRC", "GTM", "HKG", "HND", "HRV", "HTI", "HUN", "IDN", "IND", "IRL", "IRN", "IRQ", "ISR",
    "ITA", "JAM", "JOR", "JPN", "KAZ", "KEN", "KGZ", "KHM", "KOR", "KWT", "LAO", "LBN", "LBR", "LBY", "LKA", "LSO", "LTU",
    "LVA", "MAR", "MDA", "MDG", "MEX", "MKD", "MLI", "MMR", "MNG", "MOZ", "MRT", "MUS", "MWI", "MYS", "NAM", "NER", "NGA",
    "NIC", "NLD", "NOR", "NPL", "NZL", "OMN", "PAK", "PAN", "PER", "PHL", "PNG", "POL", "PRI", "PRK", "PRT", "PRY", "PSE",
    "QAT", "ROM", "RUS", "RWA", "SAU", "SDN", "SEN", "SGP", "SLE", "SLV", "SOM", "SER", "SSD", "SVK", "SVN", "SWE", "SWZ",
    "SYR", "TCD","TGO", "THA", "TJK", "TKM", "TTO", "TUN", "TUR", "TWN", "TZA", "UGA", "UKR", "URY", "USA", "UZB", "VEN",
    "VNM", "YEM", "ZAF", "ZMB", "ZWE"
]

# max de tentativas caso de erro
max_tries = 3

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
            time.sleep(2)
            print(f"Baixado (pais parceiro): {pais_parceiro}")
            break  # sai do loop de tentativas se funcionar

        except Exception as e:
            tries += 1
            print(f"Tentando novamente {pais_parceiro} ({tries}/{max_tries})... Erro: {e}")

            if tries >= max_tries:
                print(f"Pulando {pais_parceiro} após {max_tries} falhas.")
                break  # desiste dps da max tentativa

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
            time.sleep(2)
            print(f"Baixado (pais ref): {pais_ref}")
            break  # sai do loop de tentativas se funcionar

        except Exception as e:
            tries += 1
            print(f"Tentando novamente {pais_ref} ({tries}/{max_tries})... Erro: {e}")

            if tries >= max_tries:
                print(f"Pulando {pais_ref} após {max_tries} falhas.")
                break  # desiste dps da max tentativa
    
time.sleep(5)
driver.close()
print("Concluído! :)")

# agora tem q transferir os arquivos da pasta /Downloads para sua pasta de escolha !