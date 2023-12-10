import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image
from PIL import ImageDraw

if not os.path.exists(os.path.join("Задание2")):
    zip_file_path = "task3.zip"
    extract_folder = "."

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

file = os.path.join("Задание2", "masks.xml")
tree = ET.parse(file)
root = tree.getroot()
IMAGES = root.findall(".//image")

colors = root.findall("./meta/task/labels//label")
COLORS = {}
for color in colors:
    key = color.find("./name").text
    value = color.find("./color").text
    COLORS[key] = value

black_folder = os.path.join("changes", "black")
alpha_folder = os.path.join("changes", "alpha")

FOLDERS = [
    black_folder,
    alpha_folder,
]


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


def create_images(transparency: "tuple", folder: "str") -> "None":
    for image in IMAGES:
        image_name = image.attrib.get("name").split("/")[-1]
        image_path = os.path.join("Задание2", "images", image_name)
        image_origin = Image.open(image_path).convert("RGBA")
        mask = Image.new(
            mode="RGBA", size=image_origin.size, color=(0, 0, 0, transparency)
        )
        drow = ImageDraw.Draw(mask)

        for polygon in image.findall("./polygon"):
            label = polygon.attrib.get("label")
            color = COLORS[label]
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
    for transparency, folder in zip((255, 0), FOLDERS):
        create_images(transparency, folder)
    shutil.rmtree("Задание2")
