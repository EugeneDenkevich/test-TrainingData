import os
import shutil
import xml.etree.ElementTree as ET

from colorama import Fore
from colorama import Style
from PIL import Image
from PIL import ImageDraw


def init() -> "dict":
    base_path = os.path.join("task3", "Задание2")

    if not os.path.exists(base_path):
        zip_file_path = os.path.join("task3", "task3.zip")
        extract_folder = os.path.join("task3")

        shutil.unpack_archive(zip_file_path, extract_folder, "zip")

    file = os.path.join(base_path, "masks.xml")
    tree = ET.parse(file)
    root = tree.getroot()
    images = root.findall(".//image")

    colors = root.findall("./meta/task/labels//label")
    colors_dict = {}
    for color in colors:
        key = color.find("./name").text
        value = color.find("./color").text
        colors_dict[key] = value

    black_folder = os.path.join("task3", "changes", "black")
    alpha_folder = os.path.join("task3", "changes", "alpha")

    folders = [
        black_folder,
        alpha_folder,
    ]
    return {
        "base_path": base_path,
        "images": images,
        "colors": colors_dict,
        "folders": folders,
    }


def hex_to_rgb(color: "str") -> "tuple":
    numbers = color.lstrip("#")
    rgb_color = tuple(int(numbers[i : i + 2], 16) for i in (0, 2, 4))
    return rgb_color


def get_coords(polygon: "ET.Element") -> "list":
    coords = []
    row_coords = polygon.attrib.get("points").split(";")
    for coord in row_coords:
        x = float(coord.split(",")[0])
        y = float(coord.split(",")[1])
        coords.append((x, y))
    return coords


def create_images(
    transparency: "tuple",
    folder: "str",
    images: "list",
    base_path: "str",
    colors: "dict",
) -> "None":
    for image in images:
        image_name = image.attrib.get("name").split("/")[-1]
        image_path = os.path.join(base_path, "images", image_name)
        image_origin = Image.open(image_path).convert("RGBA")
        mask = Image.new(
            mode="RGBA", size=image_origin.size, color=(0, 0, 0, transparency)
        )
        drow = ImageDraw.Draw(mask)

        for polygon in image.findall("./polygon"):
            label = polygon.attrib.get("label")
            color = colors[label]
            rgb_color = hex_to_rgb(color)
            coordinates = get_coords(polygon)

            if label == "Ignore":
                drow.polygon(coordinates, fill=(0, 0, 0, transparency))
            else:
                drow.polygon(coordinates, fill=rgb_color)
        new_image_name = (
            image_name.split(image_name[image_name.rfind(".jpg")])[0] + ".png"
        )

        if not os.path.exists(folder):
            os.makedirs(folder)

        folder_black = os.path.join(folder, new_image_name)
        Image.alpha_composite(image_origin, mask).save(folder_black)


if __name__ == "__main__":
    print("---------------------")
    print("Программа работает...")
    entrypoint = init()
    folders = entrypoint["folders"]
    images = entrypoint["images"]
    base_path = entrypoint["base_path"]
    colors = entrypoint["colors"]

    for transparency, folder in zip((255, 0), folders):
        create_images(transparency, folder, images, base_path, colors)
    shutil.rmtree(base_path)
    print(Fore.GREEN + "Готово.")
    print(Style.RESET_ALL, "---------------------")
