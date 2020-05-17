from selenium import webdriver
import re # expresiones regulares
import pandas as pd
from random import uniform, randint
from time import sleep, time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytesseract
import requests
from PIL import Image
import numpy as np

def wait_between(a,b):
    rand=uniform(a, b) 
    sleep(rand)
    
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
    
start_time = time()

list_direccion = []
list_id = []

#*********DATOS**********

info_path = 'file'
dfClientes = pd.read_excel(info_path, header=0, encoding='latin1',dtype = 'str')
lst_id = dfClientes['id'].tolist()


for idni in lst_id:
 
    #Pagina a scrapear
    print('Cargar página')

    binary = FirefoxBinary('User/victor/Applications/Firefox.app')
    driver = webdriver.Firefox(executable_path='data/geckodriver')

    url = 'url'
    driver.get(url)
    
    wait_between(3,5)

    btnClose = driver.find_element_by_xpath("//button[@class='pushcrew-chrome-style-notification-btn pushcrew-btn-close']")
    btnClose.click()

    #Cantidad de iFrame
    seq = driver.find_elements_by_tag_name('iframe')
    print('Cantidad de iframe')
    print(len(seq))

    #Primer iframe para el formulario
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])
    print('Dropbox')

    #Seleccionar las opciones de Tipo documento
    select = Select(driver.find_element_by_xpath("//select[@id='iddoc']"))

    print('Seleccion de opciones')

    #Seleccionar opciones

    wait_between(2,4)
    select.select_by_value('DNI')

    wait_between(2,4)

    #Ingresar los valores de input
    driver.find_element_by_xpath("//input[@id='numdoc']").send_keys(idni)
    driver.find_element_by_xpath("//input[@id='numdoc']").send_keys(Keys.RETURN)


    #Dar click a consultar para entrar al portal

    btnCont = driver.find_element_by_xpath("//input[@class='btn btn-turquesa btn-xlarge']")
    btnCont.click()
    
    #Mostrar todos los direcciones

    wait_between(2,4)
    
    if check_exists_by_xpath("//a[@id='showme']"):
        btnShowme = driver.find_element_by_xpath("//a[@id='showme']")
        btnShowme.click()
    
        seq_tr = driver.find_elements_by_tag_name('tr')
        seq_td = 2
        
        print(len(seq_tr))
        #print(len(seq_td))
        

        for j in range(len(seq_tr)-1):
            for i in range(seq_td):
                tTable = driver.find_element_by_xpath("//div[@class='body-table']/table/tbody/tr[{0}]/td[{1}]".format(j+1,i+1)).text
                tTable = tTable[2:]
                if tTable[:1] == '9':
                    list_direccion.append(tTable)
                    list_id.append(idni)
                    print(idni)
                    print(tTable)
                    
        if check_exists_by_xpath("//a[@class='paginate_button next']"):
            btnNext = driver.find_element_by_xpath("//a[@class='paginate_button next']")
            btnNext.click()
            
            print('Siguiente Página')
            
            seq_tr = driver.find_elements_by_tag_name('tr')
            seq_td = 2

            print(len(seq_tr))
            #print(len(seq_td))


        for j in range(len(seq_tr)-1):
            for i in range(seq_td):
                tTable = driver.find_element_by_xpath("//div[@class='body-table']/table/tbody/tr[{0}]/td[{1}]".format(j+1,i+1)).text
                if tTable[:1] == '9':
                    list_direccion.append(tTable)
                    list_id.append(idni)
                    print(idni)
                    print(tTable)
    
    wait_between(4,6)
    
    if check_exists_by_xpath("//div[@class='box-btn']/a"):
        btnCont = driver.find_element_by_xpath("//div[@class='box-btn']/a")
        btnCont.click()
    else:
        print('Sin Datos')
    
    driver.quit()

dfResultado = pd.DataFrame([list_id,list_direccion])
dfResultado = dfResultado.T

dfResultado.columns = ['id','direccion']

dfResultado.to_csv("resultado.csv")

elapsed_time = time() - start_time
print("Tiempo de ejecución: %.10f seconds." % elapsed_time)