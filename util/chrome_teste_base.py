from selenium import webdriver
from selenium.webdriver.chrome.options import Options


driver_path = "../drivers/chromedriver.exe"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537."

chrome_options = Options()
chrome_options.add_argument('--lang=pt-BR')
chrome_options.add_argument('--incognito')
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument(f'user-agent={user_agent}')


class ChromeBase:

    def setup_method(self, method):
        self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        self.vars = {}
