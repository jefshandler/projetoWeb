import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from util.chrome_teste_base import ChromeBase


class TestAmazonTupla(ChromeBase):

    def teardown_method(self):
        self.driver.quit()

    lista_de_valores = [
        ('HD Portatil Externo 1TB', "HD Portátil Externo 1TB WD Western Digital USB 3.0",
         '371', 'Adicionado ao carrinho', 'R$ 371,11'),
        ('HD Portatil Externo 1TB', "SSD Externo Portátil Sandisk Extreme 1Tb",
         '720', 'Adicionado ao carrinho', 'R$ 720,00'),
    ]

    @pytest.mark.parametrize(
        'termo_pesquisa,produto_pesquisado,valor_produto,mensagem_de_sucesso,valor_carrinho',
        lista_de_valores)
    def test_amazon(self, termo_pesquisa, produto_pesquisado, valor_produto, mensagem_de_sucesso, valor_carrinho):
        wait_time = 10

        url = "https://www.amazon.com.br/"

        self.driver.get(url)
        campo_pesquisa = WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
        campo_pesquisa.click()
        time.sleep(5)
        self.driver.find_element(By.ID, "twotabsearchtextbox").send_keys(f"{termo_pesquisa}")
        self.driver.find_element(By.ID, "nav-search-submit-button").click()
        time.sleep(5)

        element = self.driver.find_elements(By.XPATH,
                                            f"//*[contains(text(), '{produto_pesquisado}')]")
        assert len(element) > 0
        print(f'{produto_pesquisado}')
        assert self.driver.find_element(By.XPATH, f"//*[contains(text(), '{produto_pesquisado}')]") \
                   .text == f"{produto_pesquisado}"
        time.sleep(5)
        elemento_produto = self.driver.find_element(By.XPATH,
                                                    f"//*[contains(text(), '{produto_pesquisado}')]/ancestor::div[contains(@class, 's-include-content-margin')]")
        elemento_preco = elemento_produto.find_element(By.XPATH,
                                                       f".//span[contains(@class, 'a-price-whole') and contains(text(), '{valor_produto}')]")

        print(f"Resultado do teste para o produto '{produto_pesquisado}':")

        if elemento_preco is not None and elemento_preco.text != valor_produto:
            print(
                f" - O preço para o produto '{produto_pesquisado}' não estava conforme o esperado. Preço encontrado: {elemento_preco.text}")
        else:
            print(
                f" - O preço para o produto '{produto_pesquisado}', com preço '{valor_produto}', estava conforme o esperado")


        self.driver.find_element(By.XPATH,
                                 f"//span[contains(text(),'{produto_pesquisado}')]").click()
        assert self.driver.find_element(By.XPATH, "//span[@id='productTitle']").text == f"{produto_pesquisado}"
        assert self.driver.find_element(By.CLASS_NAME, "a-price-whole").text == f"{valor_produto}"
        self.driver.find_element(By.CSS_SELECTOR, "input[title='Adicionar ao carrinho']").click()
        assert self.driver.find_element(By.CSS_SELECTOR,
                                        "div[data-csa-c-content-id='NATC_SMART_WAGON_CONF_MSG_SUCCESS_CONTENT'] span") \
                   .text == f"{mensagem_de_sucesso}"
        self.driver.find_element(By.XPATH, "//a[@href='/gp/cart/view.html?ref_=sw_gtc']").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "span[data-a-word-break='normal'] span[aria-hidden='true']") \
                   .text == f"{produto_pesquisado}"
        assert self.driver.find_element(By.CSS_SELECTOR,
                                           ".a-size-medium.a-color-base.sc-price.sc-white-space-nowrap.sc-product-price."
                                           "a-text-bold").text == f"{valor_carrinho}"