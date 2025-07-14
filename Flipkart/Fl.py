import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options   
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class Flipkart_Scraper:
    def __init__(self,driver=None):
        if driver is None:
            self.setup_driver()
        else:
            self.driver = driver

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=chrome_options)

    def serach_product(self,product_name=None):
        try:
            search_box = self.driver.find_element(By.NAME,"q")
            search_box.clear()
            search_box.send_keys(product_name)
            search_box.submit()
        except Exception as e:
            return
        time.sleep(2)
        
    def scroll_down(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  
            last_height = new_height

    def next_page(self):
        try:
            
            next_button = self.driver.find_element(By.XPATH,"//a[@class='_9QVEpD']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            self.driver.execute_script("arguments[0].click();", next_button)
            return True
        except Exception as e:
            print("No more pages to load.")
            return False

    def get_product_details(self):
        prodcts = self.driver.find_elements(By.XPATH,"//div[@class='tUxRFH']")
        product_details = []
        for prduct in prodcts:
            try:
                title = prduct.find_element(By.XPATH,".//div[@class='KzDlHZ']").text
                price = prduct.find_element(By.XPATH,".//div[@class='Nx9bqj _4b5DiR']").text
                rating = prduct.find_element(By.XPATH,".//div[@class='XQDdHH']").text
                product_details.append({
                    'title': title,
                    'price': price,
                    'rating': rating
                })
            except Exception as e:
                continue
        return product_details
    
    def save_csv(self,product_data,filename="flipkart_products.csv"):
        df = pd.DataFrame(product_data)
        if not os.path.exists(filename):
            df.to_csv(filename,index=False)
        else:
            df.to_csv(filename,mode='a',header=False,index=False)
        print(f"Data saved to {filename}")


    def run(self,product_name):
        self.driver.get("https://www.flipkart.com/")
        time.sleep(2)
        self.serach_product(product_name)

        while True:
            self.scroll_down()
            product_data = self.get_product_details()
            if product_data:
                self.save_csv(product_data)
            else:
                print("No products Found")
            next_button = self.next_page()
            if not next_button:
                break
            self.driver.quit()


 
if __name__ == "__main__":
    scraper = Flipkart_Scraper()
    product_name = "laptop"
    scraper.run(product_name)

