import os

import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env-task1'))

COOKIE = os.getenv("COOKIE")
URL = "https://auto.ru/"
HEADERS = f"""
Host: auto.ru
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: {COOKIE}
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
TE: trailers
"""


BRAND_COUNT = 10
ADVERT_COUNT = 10
IMAGE_MAX_COUNT = 5


def get_headers(headers: "str") -> "dict":
    headers_dict = {}

    for header in headers.strip().split('\n'):
        key, value = header.split(': ')
        headers_dict[key] = value

    return headers_dict


def get_autobase(headers: "dict"):
    autobase = {}
    counter = 1

    response_home = requests.get(URL, headers=headers)
    soup = bs(response_home.text, "html.parser")
    tags_a_brands = soup.select("a.IndexMarks__item", limit=BRAND_COUNT)

    for tag_brand in tags_a_brands:
        flag = True
        print(f"\nСбор данных по марке: {counter}/{BRAND_COUNT}")
        counter += 1

        brand_name = tag_brand.find("div", "IndexMarks__item-name").get_text().encode("ISO-8859-1").decode("utf-8")
        brand_url = tag_brand.get('href')
        response_brands = requests.get(brand_url, headers=headers)
        soup_advert = bs(response_brands.text, "html.parser")
        tags_a_advert = soup_advert.select("a.Link.ListingItemTitle__link", limit=ADVERT_COUNT)

        auto_names_and_images_list = []
        
        for tag_advert in tags_a_advert:
            auto_name = tag_advert.get_text().encode("ISO-8859-1").decode("utf-8")
            if flag:
                print(f"Получаем {ADVERT_COUNT} объявлений: ", end="", flush=True)
                flag = False
            auto_advert_url = tag_advert.get('href')
            response_images = requests.get(auto_advert_url, headers=headers)
            soup_images = bs(response_images.text, "html.parser")
            tags_img_images = soup_images.select("img.ImageGalleryDesktop__image, img.ImageGalleryDesktop__image_hidden", limit=IMAGE_MAX_COUNT)
            auto_images = [f"https:{image_tag.get('src')}" for image_tag in tags_img_images]
    
            auto_names_and_images_list.append((auto_name, auto_images))
            if not flag:
                print(".", end="", flush=True)

        autobase[brand_name] = auto_names_and_images_list

    print('\nГотово')
    return autobase


def save_image(autobase: "dict") -> int:
    print('\nСкачивание фото')
    counter_errors = 0
    for brand, adverts in autobase.items():
        print("\nМарка", brand)
        for advert in adverts:
            auto = advert[0]
            urls = advert[1]
            print("\n- Объявление", auto)

            base_path = os.path.join('task1', brand, auto)
            counter = 1
            while os.path.exists(base_path):
                base_path = os.path.join('task1', brand, auto + f" ({counter + 1})")
                counter += 1
            os.makedirs(base_path)

            for url in urls:
                try:
                    print(".", end='', flush=True)
                    response = requests.get(url)
                    file_path = f"{str(id(response))}.jpg"
                    
                    with open(os.path.join(base_path, file_path), 'wb') as file:
                        file.write(response.content)
                except:
                    print("*", end='', flush=True)
                    counter_errors += 1
        counter += 1
    return counter_errors

def main():
    print("-----------------")
    print("Начинаем парсинг")
    headers = get_headers(HEADERS)
    autobase = get_autobase(headers)

    errors = save_image(autobase)
    print("\n----------------")
    print("Парсинг завершён. Ошибок -", errors)


if __name__ == "__main__":
    main()
