import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonSenseData(unittest.TestCase):

    #Executado no inicio de cada teste
    def setUp(self):
        self.driver = webdriver.Chrome()

    def login(self, driver, username="standard_user", password="secret_sauce"):
        driver.get("https://www.saucedemo.com")
        self.assertIn("Swag Labs", driver.title)
        
        #Username
        inputName = driver.find_element_by_name("user-name")
        inputName.send_keys(username)

        #Password
        inputPassword = driver.find_element_by_name("password")
        inputPassword.send_keys(password)

        #Login Button
        loginButton = driver.find_element_by_xpath('//*[@id="login-button"]')
        loginButton.click()

    def test_login(self):
        driver = self.driver
        #Abre a página
        self.login(driver)

        #Assertiva - Verifica se encontrou o botão de logout
        logout = driver.find_element_by_xpath('//*[@id="logout_sidebar_link"]')
        self.assertIsNotNone(logout)
        self.assertEqual(driver.current_url, 'https://www.saucedemo.com/inventory.html')
        print("LOGIN - OK")

    def test_login_fails(self):
        driver = self.driver
        self.login(driver, "priscila", "123456")

        #Assertiva - Verifica se encontrou o botão de logout
        error = driver.find_element_by_xpath('//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.assertIsNotNone(error)
        print("Falha Login - OK")

    def test_order_produtcs(self):
        driver = self.driver
        self.login(driver)

        #Verifica se o produto original é o Sauce Labs Backpack
        productElem = driver.find_element_by_xpath('//*[@class="inventory_item_name"][1]')
        productName = productElem.get_attribute('innerHTML')
        self.assertEqual(productName, 'Sauce Labs Backpack')

        #Option (Low to High)
        option = driver.find_element_by_xpath('//*[@id="header_container"]/div[2]/div[2]/span/select/option[3]')
        option.click()

        #Verifica se o produto final após clicar no botão é o Sauce Labs Onesie
        productElem = driver.find_element_by_xpath('//*[@class="inventory_item_name"][1]')
        productName = productElem.get_attribute('innerHTML')
        self.assertEqual(productName, 'Sauce Labs Onesie')
        print("Orderna os produtos - OK")

    def test_select_product(self):
        driver = self.driver
        self.login(driver)

        #Option (Low to High)
        option = driver.find_element_by_xpath('//*[@id="header_container"]/div[2]/div[2]/span/select/option[3]')
        option.click()

        #Seleciona os produtos
        driver.find_element_by_xpath('//*[@id="add-to-cart-sauce-labs-onesie"]').click()
        driver.find_element_by_xpath('//*[@id="add-to-cart-test.allthethings()-t-shirt-(red)"]').click()

        #valida
        numberCart = driver.find_element_by_xpath('//*[@id="shopping_cart_container"]/a/span')
        number = numberCart.get_attribute('innerHTML')
        self.assertEqual(number, "2")
        print("Seleciona os produtos - OK")

    def test_finish_shop(self):
        driver = self.driver
        self.login(driver)

        #Option (Low to High)
        option = driver.find_element_by_xpath('//*[@id="header_container"]/div[2]/div[2]/span/select/option[3]')
        option.click()

        #Seleciona os produtos
        driver.find_element_by_xpath('//*[@id="add-to-cart-sauce-labs-onesie"]').click()
        driver.find_element_by_xpath('//*[@id="add-to-cart-test.allthethings()-t-shirt-(red)"]').click()

        #Vai para o carrinho
        driver.find_element_by_xpath('//*[@id="shopping_cart_container"]/a').click()

        #Finaliza a compra
        checkoutButton = driver.find_element_by_xpath('//*[@id="checkout"]')
        self.assertIsNotNone(checkoutButton) #Chegou na página de compra

        checkoutButton.click()

        #Chegou na página final
        self.assertEqual('https://www.saucedemo.com/checkout-step-one.html', driver.current_url)
        print("Concluir Compra - OK")

    #Executado no final de cada teste
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()