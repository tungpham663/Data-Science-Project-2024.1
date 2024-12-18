from selenium import webdriver
import pandas as pd
import time
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm


class brandCrawler:
    def __init__(self, brand_path, config):
        # Initialize the WebDriver
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # Data
        self.data = pd.DataFrame(columns=["manufacturer", "Link"])
        self.brand_path = brand_path
        self.config = config

    # get manufacturer link from config file
    def extract_manufacturer(self):
        with open(self.config, "r") as f:
            data = json.load(f)
        for manufacturer, link in data.items():
            new_row = {
                "manufacturer": manufacturer,
                "Link": link
            }
            self.data = self.data._append(new_row, ignore_index=True)

    # get html file from link
    def get_brand_html(self):
        for index, link in enumerate(self.data['Link']):
            self.driver.get(link)
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'Button_root__LQsbl') and contains(@class, 'Button_btnSmall__aXxTy') and contains(@class, 'Button_whitePrimary__nkoMI') and contains(@class, 'Button_btnIconRight__4VSUO')]"))
            )
            while True:
                try:
                    ActionChains(self.driver).move_to_element(button).click().perform()
                    time.sleep(1)  # Allow DOM to update
                except:
                    break
            # Save the page source to a file
            with open(f"{self.brand_path}/{self.data.loc[index, 'manufacturer']}.html", 'w',
                      encoding='utf-8') as f:
                f.write(self.driver.page_source)
            # add the path to the DataFrame
            self.data.loc[
                index, 'html_file'] = f"{self.brand_path}/{self.data.loc[index, 'manufacturer']}.html"
            print(f"Finished loading the page {link}")

    # parse html file to get some information of laptops
    def parse_brand_html(self):
        df = pd.DataFrame(columns=["Title", "Now Price", "Link", 'Manufacturer'])
        for index, html in enumerate(self.data['html_file']):
            try:
                file = open(html, "r", encoding="utf-8").read()
                soup = BeautifulSoup(file, "html.parser")
                temp = soup.find("div", class_="grow")
                boxs = temp.find_all("div", class_="ProductCard_cardInfo__r8zG4")
                print(len(boxs))
                for box in boxs:
                    title = box.find("h3", class_="ProductCard_cardTitle__HlwIo").a.get("title")
                    now_price = box.find("p", class_="Price_currentPrice__PBYcv").get_text() if box.find("p",
                                                                                                         class_="Price_currentPrice__PBYcv") else "Hàng sắp về"
                    link = box.find("h3", class_="ProductCard_cardTitle__HlwIo").a.get('href')
                    # add to df
                    new_row = {
                        "Title": title,
                        "Now Price": now_price,
                        "Link": "https://fptshop.com.vn/" + link,
                        "Manufacturer": self.data.loc[index, 'manufacturer']
                    }
                    df = df._append(new_row, ignore_index=True)
            except Exception as e:
                print(f"Error at {self.data.loc[index, 'manufacturer']}\n{e}")
        return df

    # close driver
    def close(self):
        """Closes the WebDriver."""
        print("Closing the WebDriver")
        self.driver.quit()

    def crawl(self):
        """Main method to run the crawler."""
        self.extract_manufacturer()
        self.get_brand_html()
        results = self.parse_brand_html()
        self.close()
        results.to_csv('data/data.csv', index=False)


class laptopCrawler:

    def __init__(self, data, link_laptop_html):
        # Initialize the WebDriver
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.data = pd.read_csv(data)
        self.link_laptop_html = link_laptop_html

    def get_laptop_html(self):
        manufacturer_index = 1
        current_manufacturer = self.data.loc[manufacturer_index, 'Manufacturer']
        """Loads the product pages with Selenium and waits for them to fully render."""
        for index, link in tqdm(enumerate(self.data['Link'])):
            if self.data.loc[index, 'Manufacturer'] not in ["lenovo", "msi"]:
                continue  # Uncomment this line to skip some manufacturers
            self.driver.get(link)
            try:
                button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(@class, 'text-blue-blue-7') and contains(@class, 'b2-medium')]"))
                )
                ActionChains(self.driver).move_to_element(button).click().perform()
                time.sleep(1)
            except Exception as e:
                print(f"Error at {link}\n{e}")
                continue
            # current_manufacturer = self.data.loc[index, 'Manufacturer']
            # manufacturer_index = len(self.data[self.data["Manufacturer"] == current_manufacturer])+1
            # Save the page source to a file
            if self.data.loc[index, 'Manufacturer'] != current_manufacturer:
                manufacturer_index = 1
                current_manufacturer = self.data.loc[index, 'Manufacturer']
            else:
                manufacturer_index += 1
            file_path = f"{self.link_laptop_html}/{current_manufacturer}+{manufacturer_index}.html"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            # add the path to the DataFrame
            self.data.loc[index, 'html_file'] = file_path
            print(f"Finished loading the page {link}")

    def parse_laptop_htmls(self):
        for index, html in enumerate(self.data['html_file']):
            file = open(html, "r", encoding="utf-8").read()
            soup = BeautifulSoup(file, "html.parser")
            # Find the product details
            boxs = soup.find_all("div", class_="flex gap-2 border-b border-dashed border-b-iconDividerOnWhite py-1.5")
            specs = {
                'CPU manufacturer': "NA",
                'CPU Speed (GHz)': "NA",
                'CPU': "NA",
                'RAM (GB)': "NA",
                'RAM Type': "NA",
                'Storage (GB)': "NA",
                'Screen Size (inch)': "NA",
                'Screen Resolution': "NA",
                'Refresh Rate (Hz)': "NA",
                'GPU manufacturer': "NA",
                "GPU": "NA",
                'Weight (kg)': "NA",
                'Battery': "NA",
                "Charging": "NA"
            }
            for box in boxs:
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Hãng CPU":
                    specs['CPU manufacturer'] = box.find("span",
                                                           class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Tốc độ CPU tối thiểu":
                    specs['CPU Speed (GHz)'] = box.find("span", class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Loại CPU":
                    specs['CPU'] = box.find("span", class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Dung lượng RAM":
                    specs['RAM (GB)'] = box.find("span", class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Loại RAM":
                    specs['RAM Type'] = box.find("div", class_="flex flex-1 flex-col py-0.5").p.text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Dung lượng":
                    specs['Storage (GB)'] = box.find("span", class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Tần số quét":
                    specs['Refresh Rate (Hz)'] = box.find("span",
                                                          class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div",
                            class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Kích thước màn hình":
                    specs["Screen Size (inch)"] = box.find("span",
                                                           class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Độ phân giải":
                    specs["Screen Resolution"] = box.find("div", class_="flex flex-1 flex-col py-0.5").p.text
                if box.find("div",
                              class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Hãng (Card rời)":

                    specs["GPU manufacturer"] = box.find("span",
                                                         class_="flex-1 text-textOnWhitePrimary b2-regular").text
                elif box.find("div",
                            class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Hãng (Card Oboard)":
                    specs["GPU manufacturer"] = box.find("span",
                                                         class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Model (Card rời)":
                    specs["GPU"] = box.find("span", class_="flex-1 text-textOnWhitePrimary b2-regular").text
                elif box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Model (Card Oboard)":
                    specs["GPU"] = box.find("span", class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Dung lượng pin":
                    specs["Battery"] = box.find("div", class_="flex flex-1 flex-col py-0.5").p.text
                if box.find("div",
                            class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Power Supply":
                    specs["Charging"] = box.find("span",
                                                    class_="flex-1 text-textOnWhitePrimary b2-regular").text
                if box.find("div", class_="w-2/5 text-textOnWhiteSecondary b2-regular").span.text == "Trọng lượng sản phẩm":
                    specs["Weight (kg)"] = box.find("div", class_="flex flex-1 flex-col py-0.5").p.text
            # Add the extracted data to the DataFrame
            for key, value in specs.items():
                self.data.loc[index, key] = value

    def close(self):
        """Closes the WebDriver."""
        print("Closing the WebDriver")
        self.driver.quit()

    def crawl(self, csv_file_path):
        """Main method to run the crawler."""
        # self.get_laptop_html()
        # self.close()
        # print column name of data
        self.parse_laptop_htmls()

        self.data.to_csv(csv_file_path, index=True)
