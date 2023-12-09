import xml.etree.ElementTree as ET

files = [
    'annotations.xml',
    'annotations-2.xml',
    'annotations-3.xml',
]

TREES = [ET.parse(file) for file in files]
ROOTS = [tree.getroot() for tree in TREES]

shapes = list(set(shape.tag for root in ROOTS for shape in root.findall(f'.//image/*')))

box = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/box')])
polygon = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/polygon')])

print(
    "\n------------------------\n"
    "\n Статистика по фигурам: \n",
   f"\n Фигуры: {shapes}: \n",
   f"\n box - {box} шт"
   f"\n polygon - {polygon} шт"
    "\n------------------------\n"
)