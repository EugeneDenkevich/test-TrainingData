import os
import shutil
import xml.etree.ElementTree as ET

files = [
    os.path.join("task2", "annotations.xml"),
    os.path.join("task2", "annotations-2.xml"),
    os.path.join("task2", "annotations-3.xml"),
]

new_path = os.path.join("task2", "changes")
if not os.path.exists(new_path):
    os.makedirs(new_path)

ch_files = []

for file in files:
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    ch_files.append(shutil.copy2(file, new_path))

TREES = [ET.parse(file) for file in ch_files]
ROOTS = [tree.getroot() for tree in TREES]


def reverse_ids(root: "ET.Element") -> "None":
    images = root.findall(".//image")
    for i, image in enumerate(images):
        reversed_image_id = image.attrib["id"][::-1]
        image.attrib["id"] = reversed_image_id


def jpg_to_png(root: "ET.Element") -> "None":
    images = root.findall(".//image")
    for image in images:
        image_name = image.attrib["name"]
        old_ext = "jpg"
        new_ext = "png"
        position = image_name.rfind(old_ext)
        new_image_name = image_name[:position] + new_ext
        image.attrib["name"] = new_image_name


def left_only_name(root: "ET.Element") -> "None":
    images = root.findall(".//image")
    for image in images:
        only_image_name = image.attrib["name"].split("/")[-1]
        image.attrib["name"] = only_image_name


for root, file in zip(ROOTS, ch_files):
    reverse_ids(root)
    jpg_to_png(root)
    left_only_name(root)
    with open(file, "wb") as new_file:
        tree = ET.ElementTree(root)
        tree.write(
            new_file,
            encoding="utf-8",
            xml_declaration=True,
            short_empty_elements=False,
        )
