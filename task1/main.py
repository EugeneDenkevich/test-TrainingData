import os
import requests
from bs4 import BeautifulSoup as bs


URL = "https://auto.ru/"
HEADERS = """
Host: auto.ru
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: suid=ca216e250f7d5287636c1f5824f504cd.970294b40e428b74362ab2feb7f8dc51; autoru_sid=a%3Ag65709fc129elu56hve41o7u87t6deqe.2964f89112513b63a08d345d0fc49259%7C1701879745381.604800.kQae0lmO3myiYXT8aIWW4A.9_2Zy9XSjktEtk6pw0zeUw2BaXsPxVlvd13jOcrZjHE; autoruuid=g65709fc129elu56hve41o7u87t6deqe.2964f89112513b63a08d345d0fc49259; _yasc=m184DcpNLlAony98Y9VXPUFO54KPq5ytGYhX13KX2Nw2EZ3eZAzyVNyu9RFs0uXZusuQhJOOPnnK; yandex_login=; i=sluyAyG/7PIT5kM9ZD0SrtKewsN0AZ6b9ybINYWbFY+BN77YxjeT+bXnue+/Cao2L/0mN/X3QwRr9XoqbSqd3yup4fQ=; yandexuid=1494474761701709086; mda2_beacon=1701883829427; layout-config={"screen_height":1050,"screen_width":1680,"win_width":485,"win_height":909}; yaPassportTryAutologin=1; popups-dr-shown-count=1; fp=5e40101444c0e79591edc3e23c95eff9%7C1701879803558; crookie=YmC+5LeE5Ait9TYASIQpChgAQSwuob2wHyHLaQkIq3vaTQt0vTecqN4IfrZKzWFbmVQcWiRNiSZM2eemluHa3ZCiuaA=; cmtchd=MTcwMTg3OTgxMDY1Nw==; los=1; bltsr=1; coockoos=1; autoru-visits-count=2; spravka=dD0xNzAxODgyODEwO2k9MzcuMjE1LjAuMTE0O0Q9NjcxNzIzRTU1MjM1MTVGREJCMEVGQjEyNDgxNEYxRThERTNGOUMyREFGRjVEMDQ0REYyMTU1M0IxOTRFODFDRTkzOUIzRUMyNTBBQ0Q2QTBGQTQ3RjkyM0VBNjhGRUE0QjMyQzBCQ0RDMzQ4OUJFMjI4M0Q3MUU4RjlDNkUyNjgyODVCQkMyRUM1OTcyN0RGNjE7dT0xNzAxODgyODEwNTgzMDc2NzY4O2g9ZWFhZDE0YjY5ZGMzMGVhZmVjYjQyODg3YTA4N2ExZGI=; _csrf_token=85d05bceaae6c65303374535142c7faf4e0ff4e203c5933b; from_lifetime=1701931672078; from=direct; ys=c_chck.1603343754; _arsus=true; autoru_sso_blocked=1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
TE: trailers
"""


BRAND_COUNT = 2
ADVERT_COUNT = 10
IMAGE_COUNT = 5


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
            tags_img_images = soup_images.select("img.ImageGalleryDesktop__image, img.ImageGalleryDesktop__image_hidden", limit=IMAGE_COUNT)
            auto_images = [f"https:{image_tag.get('src')}" for image_tag in tags_img_images]
    
            auto_names_and_images_list.append((auto_name, auto_images))
            if not flag:
                print(".", end="", flush=True)

        autobase[brand_name] = auto_names_and_images_list

    print('\nГотово')
    return autobase


def save_image(autobase: "dict") -> None:
    print('\nСкачивание фото')
    for brand, adverts in autobase.items():
        for advert in adverts:
            auto = advert[0]
            urls = advert[1]

            base_path = os.path.join('task1', brand, auto)
            counter = 1
            while os.path.exists(base_path):
                base_path = os.path.join('task1', brand, auto + f" ({counter + 1})")
                counter += 1
            os.makedirs(base_path)

            for url in urls:
                response = requests.get(url)
                file_path = f"{str(id(response))}.jpg"
                
                with open(os.path.join(base_path, file_path), 'wb') as file:
                    file.write(response.content)


def main():
    print("-----------------")
    print("Начинаем парсинг")
    headers = get_headers(HEADERS)
    autobase = get_autobase(headers)

    save_image(autobase)
    print("----------------")
    print("Парсинг завершён")


if __name__ == "__main__":
    main()
