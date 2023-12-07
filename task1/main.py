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


headers_dict = {}
for header in HEADERS.strip().split('\n'):
    key, value = header.split(': ')
    headers_dict[key] = value


def save_image(response: "requests.Response") -> None:
    if not os.path.exists(os.path.join('task1', 'images')):
        os.makedirs(os.path.join('task1', 'images'))

    with open(os.path.join("task1", "images", f"{str(id(response))}.jpg"), 'wb') as file:
        file.write(response.content)

    print('Downloaded successfully')


# Получаем первых 10 ссылок на марки авто
response_home = requests.get(URL, headers=headers_dict)
soup = bs(response_home.text, "html.parser")
tags_a_brands = soup.find_all("a", class_="IndexMarks__item", limit=10)
links_brands = [link.get('href') for link in tags_a_brands]


# Получаем первых 10 объявлений из каждой марки
for link_brands in links_brands:
    response_brands = requests.get(link_brands, headers=headers_dict)
    soup_advert = bs(response_brands.text, "html.parser")
    tags_a_advert = soup_advert.select("a.ListingItemTitle__link", limit=10)
    links_advert = [link.get('href') for link in tags_a_advert]


# TODO
# Получаем первые 5 фото каждого объявления
response_images = requests.get(links_advert[0], headers=headers_dict)
soup_images = bs(response_images.text, "html.parser")
tags_img_images = soup_images.select("img.ImageGalleryDesktop__image, img.ImageGalleryDesktop__image_hidden", limit=5)
images_urls = [f"https:{image_tag.get('src')}" for image_tag in tags_img_images]
for image_url in images_urls:
    response_image = requests.get(image_url)
    save_image(response_image)
