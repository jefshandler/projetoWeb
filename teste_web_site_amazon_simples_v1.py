import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = "../driver/chromedriver.exe"

class TestAmazon():

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
    wait_time = 20
    self.driver.get("https://www.amazon.com.br/")
    #Criei estas variáveis para ficar prático a alteração.
    nome_produto = "HD Externo 1TB USB 3.0 Seagate Expansion Portátil (STEA1000400)"
    preco_produto = "336"
    preco_produto_carrinho = "R$ 336,90"

    campo_pesquisa = WebDriverWait(self.driver, wait_time).until(
      EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
    campo_pesquisa.click()
    # Tentei não usar o sleep, porem em alguns momentos ele demora um pouco.
    time.sleep(5)
    self.driver.find_element(By.ID, "twotabsearchtextbox").send_keys("hd externo 1tb")
    self.driver.find_element(By.ID, "nav-search-submit-button").click()
    time.sleep(5)
    elemento = self.driver.find_elements(By.XPATH,
                                        f"//span[contains(text(),'{nome_produto}')]")
    assert len(elemento) > 0
    assert self.driver.find_element(By.XPATH,
                                    f"//*[contains(text(), '{nome_produto}')]").text == nome_produto
    time.sleep(5)
    elemento_produto = self.driver.find_element(By.XPATH,
                                               f"//*[contains(text(), '{nome_produto}')]/ancestor::div[contains(@class, 's-include-content-margin')]")
    elemento_preco = elemento_produto.find_element(By.XPATH,
                                                 f".//span[contains(@class, 'a-price-whole') and contains(text(), '{preco_produto}')]")
    assert elemento_preco.text == preco_produto
    self.driver.find_element(By.XPATH,
                             f"//*[contains(text(), '{nome_produto}')]").click()
    assert self.driver.find_element(By.XPATH, "//span[@id='productTitle']").text \
           == nome_produto
    assert self.driver.find_element(By.CLASS_NAME, "a-price-whole").text == preco_produto
    self.driver.find_element(By.CSS_SELECTOR, "input[title='Adicionar ao carrinho']").click()
    assert self.driver.find_element(By.CSS_SELECTOR,
                                    "div[data-csa-c-content-id='NATC_SMART_WAGON_CONF_MSG_SUCCESS_CONTENT'] span").text \
           == "Adicionado ao carrinho"

    self.driver.find_element(By.XPATH, "//a[@href='/gp/cart/view.html?ref_=sw_gtc']").click()

    assert self.driver.find_element(By.CSS_SELECTOR, "span[data-a-word-break='normal'] span[aria-hidden='true']").text \
           == nome_produto

    assert self.driver.find_element(By.XPATH,
                                    "(//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap'][normalize-space()='R$ 336,90'])[1]").text \
           == preco_produto_carrinho


