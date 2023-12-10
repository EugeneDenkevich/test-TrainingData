import xml.etree.ElementTree as ET

files = [
    "annotations.xml",
    "annotations-2.xml",
    "annotations-3.xml",
]

TREES = [ET.parse(file) for file in files]
ROOTS = [tree.getroot() for tree in TREES]

images = [image for root in ROOTS for image in root.findall(".//image")]
images_count = len(images)
images_marked = len(list(filter(lambda image: len(image) > 0, images)))
images_unmarked = images_count - images_marked
shapes_count = sum(len(root.findall(".//image/*")) for root in ROOTS)

max_image = max(
    images,
    key=lambda image: int(image.attrib.get("width"))
    * int(image.attrib.get("height")),
)
max_image_name = max_image.attrib.get("name")
max_image_width = max_image.attrib.get("width")
max_image_height = max_image.attrib.get("height")
max_images_count = len(
    list(
        filter(
            lambda image: image.attrib.get("width") == max_image_width
            and image.attrib.get("height") == max_image_height,
            images,
        )
    )
)

min_image = min(
    images,
    key=lambda image: int(image.attrib.get("width"))
    * int(image.attrib.get("height")),
)
min_image_name = min_image.attrib.get("name")
min_image_width = min_image.attrib.get("width")
min_image_height = min_image.attrib.get("height")
min_images_count = len(
    list(
        filter(
            lambda image: image.attrib.get("width") == min_image_width
            and image.attrib.get("height") == min_image_height,
            images,
        )
    )
)

print(
    "\n",
    "1. Всего изображений -",
    images_count,
    "\n\n",
    "2. Всего изображений размечено -",
    images_marked,
    "\n\n",
    "3. Всего изображений не размечено -",
    images_unmarked,
    "\n\n",
    "5. Всего фигур -",
    shapes_count,
    "\n\n",
    "6. Самое большое изображение -",
    max_image_name,
    "\n",
    "   его ширина -",
    max_image_width,
    "\n",
    "   его высота -",
    max_image_height,
    "\n",
    "   таких в документах -",
    max_images_count,
    "\n\n",
    "   Самое маленькое изображение -",
    min_image_name,
    "\n",
    "   его ширина -",
    min_image_width,
    "\n",
    "   его высота -",
    min_image_height,
    "\n",
    "   таких в документах -",
    min_images_count,
    "\n",
)
