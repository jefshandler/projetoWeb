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
        ('HD externo 1TB', "HD Externo 1TB USB 3.0 Seagate Expansion Portátil (STEA1000400)",
         '336', 'Adicionado ao carrinho', 'R$ 336,90'),
        ('HD externo 1TB', "M-Power Ssd 1tb E30 Portable 520Mbs Externo Portátil Tipo C",
         '814', 'Adicionado ao carrinho', 'R$ 814,47'),
    ]

    @pytest.mark.parametrize(
        'termo_pesquisa,produto_pesquisado,valor_produto,mensagem_de_sucesso,valor_carrinho',
        lista_de_valores)
    def test_amazon(self, termo_pesquisa, produto_pesquisado, valor_produto, mensagem_de_sucesso, valor_carrinho):
        wait_time = 20

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
        assert elemento_preco.text == valor_produto
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
