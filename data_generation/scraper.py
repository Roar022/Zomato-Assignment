from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import re

class RestaurantDataScraper:
    def __init__(self):
        pass

    def clean_filename(self, name):
        return re.sub(r'[^a-zA-Z0-9_\-]', '_', name.strip()) if name else "unknown_restaurant"

    def clean_opening_hours(self, hours):
        if hours:
            return re.sub(r'\s*\(.today.\)', '', hours, flags=re.IGNORECASE).strip()
        return ""

    def extract_info(self, url, phone_class, hours_class, name_class, address_class, rating_class):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        info = {
            "restaurant_name": "",
            "restaurant_location": "",
            "phone_number": "",
            "opening_hours": "",
            "rating": ""
        }
        if name_class:
            for el in driver.find_elements(By.CLASS_NAME, name_class):
                if el.text.strip():
                    info["restaurant_name"] = el.text.strip()
                    print(el.text.strip())
                    break
        if address_class:
            for el in driver.find_elements(By.CLASS_NAME, address_class):
                if el.text.strip():
                    info["restaurant_location"] = el.text.strip()
                    break
        if phone_class:
            for el in driver.find_elements(By.CLASS_NAME, phone_class):
                if el.text.strip():
                    info["phone_number"] = el.text.strip()
                    break
        if hours_class:
            for el in driver.find_elements(By.CLASS_NAME, hours_class):
                if el.text.strip():
                    info["opening_hours"] = self.clean_opening_hours(el.text.strip())
                    break
        if rating_class:
            for el in driver.find_elements(By.CLASS_NAME, rating_class):
                if el.text.strip():
                    info["rating"] = el.text.strip()
                    break
        driver.quit()
        return info

    def extract_menu(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        names = driver.find_elements(By.CLASS_NAME, "dwSeRx")
        prices = driver.find_elements(By.CLASS_NAME, "chixpw")
        descriptions = driver.find_elements(By.CLASS_NAME, "gCijQr")
        svg = driver.find_elements(By.CLASS_NAME, "sc-jxOSlx")
        rating = driver.find_elements(By.CLASS_NAME, "bTHhpu")
        menu_items = []
        for i in range(min(len(names), len(prices), len(descriptions), len(svg), len(rating))):
            features = []
            dietery = "Veg"
            s = svg[i].find_element(By.TAG_NAME, "use").get_attribute("xlink:href")
            s_trim = s[:-2]
            if s_trim == "/food/sprite-CiiAtHUR.svg#bestseller":
                features.append("Best Seller")
            s_type = s[-6:]
            if s_type == "NonVeg":
                dietery = "Non Veg"
            menu_items.append({
                "item_name": names[i].text,
                "price": prices[i].text,
                "description": descriptions[i].text,
                "dietery": dietery,
                "features": features,
                "rating": rating[i].text
            })
        driver.quit()
        return menu_items

    def save_data(self, info, menu, idx):
        menu_csv_filename = self.clean_filename(info["restaurant_name"]) + ".csv" if info["restaurant_name"] else f"restaurant{idx+1}.csv"
        with open(menu_csv_filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["item_name", "price", "description", "dietery", "features", "rating"])
            writer.writeheader()
            writer.writerows(menu)
        return menu_csv_filename

def main():
    restaurant_pairs = [
        (),
        # Add more pairs as needed
    ]

    scraper = RestaurantDataScraper()
    restaurant_info_list = []
    for idx, (zomato_url, swiggy_url, phone_class, hours_class, name_class, address_class, rating_class) in enumerate(restaurant_pairs):
        info = scraper.extract_info(zomato_url, phone_class, hours_class, name_class, address_class, rating_class)
        menu = scraper.extract_menu(swiggy_url)
        menu_csv_filename = scraper.save_data(info, menu, idx)
        restaurant_info_list.append({
            "restaurant_name": info["restaurant_name"],
            "restaurant_location": info["restaurant_location"],
            "phone_number": info["phone_number"],
            "opening_hours": info["opening_hours"],
            "rating": info["rating"],
            "menu_csv": menu_csv_filename,
        })

    with open("restaurants_info.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["restaurant_name", "restaurant_location", "phone_number", "opening_hours", "rating", "menu_csv"])
        writer.writeheader()
        writer.writerows(restaurant_info_list)

    print(f"Saved {len(restaurant_info_list)} restaurants to restaurants_info.csv")

if __name__ == "__main__":
    main()