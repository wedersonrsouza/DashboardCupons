import os
import time
import tkinter as tk
from pathlib import Path
from pprint import pprint
from time import sleep
from tkinter import messagebox

import pandas as pd
import selenium.webdriver.chrome.service as service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

OS_NAME = 'linux' if 'posix' in os.name else 'windows'
DESKTOP = {'linux': os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'),
            'windows': os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}


class Produto:
    data_nf = ''
    nr_nf = ''
    cnpj_empresa = ''
    nome_empresa = ''
    descricao = ''
    qtd = 0
    unidade = ''
    valor = 0
    cod_produto = ''
    cod_ncm = ''
    genero = ''
    cfop = ''
    cod_ean = ''
    valor_un_tributavel = 0
    valor_un_comercializacao = 0
    valor_aprox_tributos = 0
    aliquota_icms = 0
    valor_icms = 0



# Main class
class Browser:
    def __init__(self, cupom_code) -> None:
        self.chrome_path = ".\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
        self.chromedriver_path = ".\\GoogleChromePortable\\App\\Chrome-bin\\chromedriver.exe"
        self.cupom_code = cupom_code
        
        self.start_url = f"https://www.nfce.sefin.ro.gov.br/consultanfce/consulta.jsp?p={cupom_code}"
        
                
        print(self.start_url)

        self.options = Options()
#         self.options.add_argument('--incognito')
        self.options.add_argument('log-level=3')  # Supress all warnings and ERRORS

        self.serv = service.Service(self.chromedriver_path)
        self.serv.start()
        self.capabilities = {'chrome.binary': self.chrome_path}

        self.driver = webdriver.Remote(self.serv.service_url, self.capabilities, options=self.options)
        pass

    def go(self, url):
        self.driver.get(url)
        
  
    def check_element(self, locator, locator_type=By.ID, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator))
            )
            return True
        except:
            return False
        
    def wait_for_captcha(self, captcha_class="captcha-form"):
        
        
        if self.check_element(captcha_class, By.CLASS_NAME):
            print("Captcha presente. Por favor, resolva o captcha.")
            
            self.wait_for_element_disappear("captcha-form", By.CLASS_NAME)
            
            
    def wait_for_element_disappear(self, locator, locator_type=By.ID):
        while True:
            try:
                self.driver.find_element(locator_type, locator)
                # Se o elemento for encontrado, aguarde um pouco e tente novamente
                time.sleep(1)
            except:
                # Se o elemento não for encontrado (ou seja, desapareceu), saia do loop
                break
            
    def wait_for_element(self, locator, locator_type=By.ID):
        print(f'Procurando pelo elemento {locator}')
        
        while True:
            if self.driver.find_element(locator_type, locator):
                print('encontrado')
                break
            
    
    


def CreatePopup(title, message):
     
     # Crie uma janela de diálogo GUI
    root = tk.Tk()
    # root.withdraw()  # Esconda a janela principal
    messagebox.showinfo(title, message)
    root.destroy()




if __name__ == '__main__':
            
    # # cupom_code = "11230804082624003686650180001906841365894182|2|1|4|E2589715C9B0D14ECE8B5DD91E2B1DB1B203406F"
    # # cupom_code = "11240505782891000360650090003204451113250163|2|1|4|E2589715C9B0D14ECE8B5DD91E2B1DB1B203406F"
    # #cupom_code = "11240505782891000360650100002677821490142970|2|1|1|3379808909C8A91A36174DB2C9C240514FF0BC8A"
    
    # cupom_code=  "11240504082624003686650150001924269367825023|2|1|09|6609B378672106F43E5BEFD37555EE7CA131AD9F"
    # # cupom_code=  "11241005782891000360650060005383691496332777|2|1|1|14346373515451045A7261719B2AD55C0022ECC0"
    # # cupom_code=  "11240904082624003686650160002666521387133425|2|1|4|A8994E96EEC0C0BCD38AC585B8518DA2AB61908C"
    # # cupom_code=  "11241004082624003686650160002679801230735381|2|1|4|05B45464619635E84AC223A69BCD5CE22E866385"
    
    list_cupom_code = [
        # "11240404082624003686650170001954331323898418|2|1|4|A42084CC166246081A6ECCFE898B09B3C06A71E1",
        # "11240404082624003686650040000789991085439673|2|1|4|3C43C7D2DAB5909D7A525019EDF40FB60B1A9231",
        # "11230804082624003686650180001906841365894182|2|1|4|E2589715C9B0D14ECE8B5DD91E2B1DB1B203406F",
        # "11240543152856000276650000000001601676855510|2|1|1|1D0930C8E58B9960A069EB535A1AE5D2B174E828",
        # "11240504082624003686650150001924269367825023|2|1|09|370.46|00000000000000000000000000000000000000000000000000000000|000004|6609B378672106F43E5BEFD37555EE7CA131AD9F",
        # "11240505782891000360650090003204451113250163|2|1|1|B98FC71D62ABC03BCA3A1A12105F91F255383169",
        # "11240505782891000360650100002677821490142970|2|1|1|3379808909C8A91A36174DB2C9C240514FF0BC8A",
        # "11240504082624003686650150001924269367825023|2|1|09|370.46|00000000000000000000000000000000000000000000000000000000|000004|6609B378672106F43E5BEFD37555EE7CA131AD9F",
        # "11241005782891000360650060005383691496332777|2|1|1|14346373515451045A7261719B2AD55C0022ECC0",
        # "11240904082624003686650160002666521387133425|2|1|4|A8994E96EEC0C0BCD38AC585B8518DA2AB61908C",
        # "11241004082624003686650160002679801230735381|2|1|4|05B45464619635E84AC223A69BCD5CE22E866385",
        # "11240975315333018660655180002319041048579174|2|1|1|61C748D5772510224DE6BB10C5E5F970466073CB",
        # "11240904082624004577650010000177411111506012|2|1|4|CEEAF78B4C94079C2A1A871D4212F93332665C40",
        # "11240904082624003686650160002666521387133425|2|1|4|A8994E96EEC0C0BCD38AC585B8518DA2AB61908C",
        # "11240904082624004577650090000137971255353599|2|1|4|7BCEFC26574388A14330CEE3CAE86E42821558D9",
        # "11241005782891000360650060005383691496332777|2|1|1|14346373515451045A7261719B2AD55C0022ECC0",
        # "11240805782891000360650020005371161763798898|2|1|1|6532AA3F65933C037184A7625A235164270D7C0F",
        # "11240805782891000360650020005358681891883737|2|1|1|89780338A3C6E4F0AE83BFD478C1240471B2746A",
        # "11240805782891000360650030002613151908245687|2|1|1|0B541640327F243EAEE2D149B5136E550B35F2B8",
        # "11240805782891000360650070004871931261980270|2|1|1|153B9D49CEA70B5E1FA9F25A578F0534AA01ABF7",
        # "11240805782891000360650020005329351609587331|2|1|1|452A58C6D03216E7EE463DB6B51F9007ED2733F9",
        # "11240805782891000360650080003178291484065624|2|1|1|DFCC9F9E4CB9420702D619DB2F6D614C98CA216D",
        # "11240804082624003686650110002092721322450288|2|1|4|C9AC64E177E2E1C0FCCD883842D9DE7D4073954F",
        # "11240805782891000360650070004876371486273600|2|1|1|590AE941774FB1F2B4668FD800DB9BA349C2CC99",
        # "11240804082624004577650150000045261338862428|2|1|4|F5C3F108A8DD8611C3680282987DF7626038AFE4",
        # "11240804082624004577650170000065571273213860|2|1|4|8A660487AB72FA33FF1F23E890A80410840608BD",
        # "11240704082624004577650120000016411049236426|2|1|4|0E668B95312D40CBF38EA468344BBDF974E36392",
        # "11240804082624004577650180000032041150605526|2|1|4|719026B1D9A2AC71E4ED3823E1DA08458E04FE9A",
        # "11240804082624003686650180002604141045857454|2|1|4|F0F287466931AA6B0071FEB9985A75497E79F4BF",
        ##"11240910695456000339650010000620999932082966|2|1|07|45.46|674f3138555a79384a2b657178573641336e7830514d2f4b552b453d|2|EBAC41D3CF39349F164DB3ED23A50B9150D74F11",
        "11240910695456000339650010000616421202830163|2|1|2|4E59D843506A8248C1C3A4F44854DD13E28045EC",
        # "11240905782891000360650030002677791719311950|2|1|1|3A11F28F3E02286EEC8CEE1A2FB7CF0740D212DF",
        # "11240904082624003686650160002657171045857456|2|1|4|8A2E8A53AF842271838622C77004F44846EA4FAA",
        # "11240904082624004577650050000025711076268189|2|1|4|8AF1F836E3596B8EFDAE4727F3EDDDA1A40B0AA6",
        # "11240875315333018660655130002830209048579176|2|1|28|21164|475371744A597266446359556A6330376D6C7A7344503758737A303D|1|224FAF448EC6BAFA8D0C2F0C010943049490B27311240875315333018660655130002830209048579176|2|1|28|21164|475371744A597266446359556A6330376D6C7A7344503758737A303D|1",
        # "11240904082624004577650170000101041130331708|2|1|4|88C1B004FF1ED00EC3FEFED2A31E7F8A6B57C754",
        # "11240804082624004577650140000069851348033918|2|1|4|BEBBE1DAA1965425AE136FCF6E297A691C57F248",
        # "11240904082624004577650160000093991036203250|2|1|4|D1E2E85D28B87F587F722FA2CE9CBDA18D8891EB",
        # "11240804082624003686650170002176401082060708|2|1|4|89869DFCDE305BCCB2E3C89EA778AB57F2F39FBD",
        # "11240904082624004577650150000113851379892775|2|1|4|E45794D290501BA7AEF1E3A298391619FB582DD1"
        ]
    
        
    
    for cupom_code in list_cupom_code:
        
    
        browser = Browser(cupom_code=cupom_code)
            
        browser.go(browser.start_url)
        
        driver = browser.driver
        
        browser.wait_for_captcha()
        
        if browser.check_element("conteudo", locator_type=By.ID):
            print("Elemento 'conteudo' encontrado. Continuando...")
            
            driver.find_element(By.XPATH, '//*[@id="botao_detalhada"]/a').click()
            
            
            browser.wait_for_element("sefin_NFCe", By.ID)
                    
            
            tabela_dados_nfe = None
            linhas_nfe = None
            tabela_dados_nfe = driver.find_element(By.ID, 'sefin_NFCe')
            linhas_nfe = tabela_dados_nfe.find_elements(By.TAG_NAME, 'tr')
            
            data_emissao = driver.find_elements(By.XPATH, '//*[@id="NFe"]/fieldset[1]/table/tbody/tr/td[4]/span')[0].text
            total_nf = driver.find_elements(By.XPATH, '//*[@id="NFe"]/fieldset[1]/table/tbody/tr/td[6]/span')[0].text
            cnpj_empresa = driver.find_elements(By.XPATH, '//*[@id="NFe"]/fieldset[2]/table/tbody/tr/td[1]/span')[0].text
            nome_empresa = driver.find_elements(By.XPATH, '//*[@id="NFe"]/fieldset[2]/table/tbody/tr/td[2]/span')[0].text
            numero_nf = driver.find_elements(By.XPATH, '//*[@id="NFe"]/fieldset[1]/table/tbody/tr/td[3]/span')[0].text
            print(data_emissao, total_nf, cnpj_empresa, nome_empresa, numero_nf)
            
            
            ### Aba Produtos
            driver.find_element(By.XPATH, '//*[@id="tab_tipo_aba"]/li[4]/a').click()
            
            browser.wait_for_element("Prod", By.ID)
            
            div_Prod = driver.find_element(By.ID, 'Prod')
            tabela_produtos = div_Prod.find_elements(By.TAG_NAME, 'table')
            
            lista_produtos = []

            # Percorra cada tabela e altere o atributo 'style'
            for tabela in tabela_produtos:
                driver.execute_script("arguments[0].style.display = 'table';", tabela)
                
        
            # for tabela in tabela_produtos:
                class_name = tabela.get_attribute('class')

                if 'toggle' in class_name or 'toggable' in class_name:
                    style = tabela.get_attribute('style')
                
                    if 'display: none;' in style:
                        print('Detalhes fechado, clicando...')
                        tabela.click()
                    
                    if 'toggle' in class_name:
                
                        tabela_toggle = tabela.find_elements(By.TAG_NAME, 'td')
                
                        ### Cria novo produto        
                        novo_produto =  Produto()
                        ### dados do NF
                        
                        novo_produto.data_nf = data_emissao
                        novo_produto.nr_nf = numero_nf
                        novo_produto.cnpj_empresa = cnpj_empresa
                        novo_produto.nome_empresa = nome_empresa            

                        print(tabela_toggle[1].text)

                        
                        novo_produto.descricao = tabela_toggle[1].text
                        novo_produto.qtd = tabela_toggle[2].text
                        novo_produto.unidade = tabela_toggle[3].text
                        novo_produto.valor = tabela_toggle[4].text

                        print(f'Carregando dados do produto {novo_produto.descricao}')

                    
                
                    elif 'toggable' in class_name:
                        print('A tabela é toggable.')

                        cod_ncm = None
                        cfop = None
                        
                        inside_table = tabela.find_elements(By.TAG_NAME, 'table')

                        table0 = inside_table[0].find_elements(By.TAG_NAME, 'td')
                        table1 = inside_table[1].find_elements(By.TAG_NAME, 'td')
                        
                        novo_produto.cod_produto = table0[0].find_element(By.TAG_NAME, 'span').text
                        novo_produto.cod_ncm = table0[1].find_element(By.TAG_NAME, 'span').text
                        novo_produto.genero = table0[2].find_element(By.TAG_NAME, 'span').text
                        novo_produto.cfop = table0[4].find_element(By.TAG_NAME, 'span').text

                        novo_produto.cod_ean = table1[4].find_element(By.TAG_NAME, 'span').text

                        novo_produto.valor_un_comercializacao = table1[7].find_element(By.TAG_NAME, 'span').text
                        novo_produto.valor_un_tributavel = table1[8].find_element(By.TAG_NAME, 'span').text
                        
                        novo_produto.valor_aprox_tributos = table1[12].find_element(By.TAG_NAME, 'span').text

                        novo_produto.aliquota_icms = table1[19].find_element(By.TAG_NAME, 'span').text
                        novo_produto.valor_icms = table1[20].find_element(By.TAG_NAME, 'span').text
                        
                        lista_produtos.append(novo_produto)
                        
                        

            df = pd.DataFrame([vars(p) for p in lista_produtos])
            # df['qtd'] = df['qtd'].str.replace(',', '.').astype(float)
            # df['valor'] = df['valor'].str.replace(',', '.').astype(float)
            # df['valor_un_comercializacao'] = df['valor_un_comercializacao'].str.replace(',', '.').astype(float)
            # df['valor_un_tributavel'] = df['valor_un_tributavel'].str.replace(',', '.').astype(float)
            # df['valor_aprox_tributos'] = df['valor_aprox_tributos'].str.replace(',', '.').astype(float)
            
            
            tmp_data = str(data_emissao).replace('/','').replace(':', '-')
            
            df.to_excel(f'cupom-{numero_nf}-{tmp_data}.xlsx')
                                        
          
                    
            
                    
            
        else:
            print("Elemento 'conteudo' não encontrado.")
        
            
        


        
            
        
        
            
        
        

