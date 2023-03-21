from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

from behave import *

@given('que eu acesse a página da Amazon e comparamos o titulo')
def abrir_homepage(self):
    driver_path = "../driver/chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument('--lang=pt-BR')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--mute-audio")

    self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    self.driver.get("https://www.amazon.com.br/")
    assert "Amazon.com.br" in self.driver.title


@when('eu pesquisar por um produto "{termo_pesquisa}"')
def pesquisa_produto(self, termo_pesquisa):
    campo_pesquisa = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
    campo_pesquisa.click()
    time.sleep(5)
    campo_pesquisa.send_keys(termo_pesquisa)
    self.driver.find_element(By.ID, "nav-search-submit-button").click()


@then('o produto pesquisado deve ser exibido na página de resultados "{produto_pesquisado}"')
def consulta_produto(self, produto_pesquisado):
    encontou_produto = (By.XPATH, f"//*[contains(text(), '{produto_pesquisado}')]")
    time.sleep(3)
    produto = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(encontou_produto))
    assert produto.text == produto_pesquisado


@when('eu seleciono o produto pesquisado "{produto_pesquisado}"')
def escolher_produto(self, produto_pesquisado):
    self.driver.find_element(By.XPATH, f"//span[contains(text(),'{produto_pesquisado}')]").click()


@then('o produto e preço, do produto  selecionado deve estar correto "{produto_pesquisado}", "{valor_produto}"')
def preco_produto_escolhido(self, produto_pesquisado, valor_produto):
    assert self.driver.find_element(By.XPATH, "//span[@id='productTitle']").text == produto_pesquisado
    assert self.driver.find_element(By.CLASS_NAME, "a-price-whole").text == valor_produto


@when('eu adicionar o produto ao carrinho')
def adicionar_produto_carrinho(self):
    self.driver.find_element(By.CSS_SELECTOR, "input[title='Adicionar ao carrinho']").click()


@then('a mensagem de sucesso deve ser exibida "{mensagem_de_sucesso}"')
def mensagem_produto_adicionado(self, mensagem_de_sucesso):
    assert self.driver.find_element(By.CSS_SELECTOR,
                                    "div[data-csa-c-content-id='NATC_SMART_WAGON_CONF_MSG_SUCCESS_CONTENT'] span")\
                                    .text == mensagem_de_sucesso

@when('eu acessar o carrinho')
def abrir_carrinho(self):
    self.driver.find_element(By.XPATH, "//a[@href='/gp/cart/view.html?ref_=sw_gtc']").click()


@then('o produto adicionado deve estar no carrinho "{produto_pesquisado}"')
def compara_produto_carrinho(self, produto_pesquisado):
    assert self.driver.find_element(By.CSS_SELECTOR, "span[data-a-word-break='normal'] span[aria-hidden='true']") \
               .text == produto_pesquisado


@then('o preço do produto no carrinho deve estar correto "{valor_carrinho}"')
def compara_preco_produto_carrinho(self, valor_carrinho):
    assert self.driver.find_element(By.CSS_SELECTOR,
                                    ".a-size-medium.a-color-base.sc-price.sc-white-space-nowrap.sc-product-price."
                                    "a-text-bold").text == valor_carrinho


@then('eu fecho o navegador')
def fechar_navegador(self):
    self.driver.close()