import pandas as pd
import json

class MenuItem:
    def __init__(self, base_id, idx, data):
        self.id = base_id * 100 + (idx + 1)
        self.name = data['item_name']
        self.description = data['description']
        self.price = int(data['price'])
        self.dietary = self.get_dietary(data['dietery'])
        self.features = self.get_features(data['features'])
        self.rating = data['rating']
        self.available = True

    @staticmethod
    def get_dietary(label):
        return ["veg"] if label.strip().lower() == "veg" else ["non-veg"]

    @staticmethod
    def get_features(label):
        cleaned = label.strip().lower()
        return ['Best Seller'] if cleaned == "['best seller']" else []

    def to_dict(self):
        return self.__dict__

class Restaurant:
    def __init__(self, idx, row):
        self.id = idx + 1
        self.name = row['restaurant_name']
        self.location = row['restaurant_location']
        self.rating = float(row['rating'])
        self.operating_hours = {
            "mon-fri": row['opening_hours'],
            "sat-sun": row['opening_hours']
        }
        self.contact = {
            "phone": f"+{row['phone_number']}"
        }
        self.menu = self.load_menu(row['menu_csv'])

    def load_menu(self, menu_csv):
        menu_df = pd.read_csv(menu_csv)
        return [MenuItem(self.id, i, item).to_dict() for i, item in menu_df.iterrows()]

    def to_dict(self):
        return self.__dict__

class RestaurantDataConverter:
    def __init__(self, info_csv):
        self.info_csv = info_csv
        self.restaurants = []

    def process(self):
        df = pd.read_csv(self.info_csv)
        for idx, row in df.iterrows():
            restaurant = Restaurant(idx, row)
            self.restaurants.append(restaurant.to_dict())

    def export_json(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.restaurants, f, indent=2, ensure_ascii=False)
        print(f"JSON file created at: {output_file}")

if __name__ == "__main__":
    converter = RestaurantDataConverter('restaurants_info.csv')
    converter.process()
    converter.export_json('restaurants.json')