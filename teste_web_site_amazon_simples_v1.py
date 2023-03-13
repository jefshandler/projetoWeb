import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = "../driver/chromedriver.exe"

class TestNewTest():

  def setup_method(self, method):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537."

    chrome_options = Options()
    chrome_options.add_argument('--lang=pt-BR')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument(f'user-agent={user_agent}')
    self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    self.vars = {}


  def teardown_method(self, method):
    self.driver.quit()

  def test_amazon(self):
    # Abrindo site da amazon
    wait_time = 15
    self.driver.get("https://www.amazon.com.br/")
    nome_produto = "HD Portátil Externo 1TB WD Western Digital USB 3.0"
    preco_produto = "371"

    campo_pesquisa = WebDriverWait(self.driver, wait_time).until(
      EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
    campo_pesquisa.click()
    time.sleep(5)
    self.driver.find_element(By.ID, "twotabsearchtextbox").send_keys("HD Portátil Externo 1TB")
    self.driver.find_element(By.ID, "nav-search-submit-button").click()
    time.sleep(5)
    element = self.driver.find_elements(By.XPATH,
                                        f"//span[contains(text(),'{nome_produto}')]")
    assert len(element) > 0
    assert self.driver.find_element(By.XPATH,
                                    f"//*[contains(text(), '{nome_produto}')]").text == "HD Portátil Externo 1TB WD Western Digital USB 3.0"
    time.sleep(5)


    elemento_produto = self.driver.find_element(By.XPATH,
                                               f"//*[contains(text(), '{nome_produto}')]/ancestor::div[contains(@class, 's-include-content-margin')]")
    elemento_preco = elemento_produto.find_element(By.XPATH,
                                                 f".//span[contains(@class, 'a-price-whole') and contains(text(), '{preco_produto}')]")

    print(f"Resultado do teste para o produto '{nome_produto}':")

    if elemento_preco is not None and elemento_preco.text != preco_produto:
      print(
        f" - O preço para o produto '{nome_produto}' não estava conforme o esperado. Preço encontrado: {elemento_preco.text}")
    else:
      print(f" - O preço para o produto '{nome_produto}', com preço '{preco_produto}', estava conforme o esperado")

    self.driver.find_element(By.XPATH,
                             f"//*[contains(text(), '{nome_produto}')]").click()
    # Verifica se o título do produto está correto
    assert self.driver.find_element(By.XPATH, "//span[@id='productTitle']").text \
           == "HD Portátil Externo 1TB WD Western Digital USB 3.0"
    # Imprime o título do produto se a verificação passar
    print("Título do produto verificado com sucesso")

    # Verifica se o preço do produto está correto
    assert self.driver.find_element(By.CLASS_NAME, "a-price-whole").text == "371"
    # Imprime o preço do produto se a verificação passar
    print("Preço do produto verificado com sucesso")

    # Clica no botão "Adicionar ao carrinho"
    self.driver.find_element(By.CSS_SELECTOR, "input[title='Adicionar ao carrinho']").click()
    # Verifica se a mensagem de confirmação apareceu corretamente
    assert self.driver.find_element(By.CSS_SELECTOR,
                                    "div[data-csa-c-content-id='NATC_SMART_WAGON_CONF_MSG_SUCCESS_CONTENT'] span").text \
           == "Adicionado ao carrinho"
    # Imprime a mensagem de confirmação se a verificação passar
    print("Mensagem de confirmação do carrinho verificada com sucesso")

    # Clica no link do carrinho de compras
    self.driver.find_element(By.XPATH, "//a[@href='/gp/cart/view.html?ref_=sw_gtc']").click()
    # Verifica se o título do produto no carrinho está correto
    assert self.driver.find_element(By.CSS_SELECTOR, "span[data-a-word-break='normal'] span[aria-hidden='true']").text \
           == "HD Portátil Externo 1TB WD Western Digital USB 3.0"
    # Imprime o título do produto no carrinho se a verificação passar
    print("Título do produto no carrinho verificado com sucesso")

    # Verifica se o preço do produto no carrinho está correto
    assert self.driver.find_element(By.XPATH,
                                    "(//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap'][normalize-space()='R$ 371,11'])[1]").text \
           == "R$ 371,11"
    # Imprime o preço do produto no carrinho se a verificação passar
    print("Preço do produto no carrinho verificado com sucesso")
