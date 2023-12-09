import xml.etree.ElementTree as ET


files = [
    'annotations.xml',
    'annotations-2.xml',
    'annotations-3.xml',
]

TREES = [ET.parse(file) for file in files]
ROOTS = [tree.getroot() for tree in TREES]

classes = list(set(class_.attrib.get('label') for root in ROOTS for class_ in root.findall(f'.//image/*')))

grab = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="grab"]')])
ignore = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="ignore"]')])
svetofor = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="Светофор на другой дороге"]')])
doubler = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="Дублирующий"]')])
vagon = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="vagon"]')])
basic = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="Основной"]')])
fur = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="fur"]')])
item = len([class_.attrib.get('label') for root in ROOTS for class_ in root.findall('.//image/*[@label="item"]')])

print(
    "\n------------------------\n"
    "\n Статистика по классам: \n",
   f"\n Классы: {classes}: \n",
   f"\n grab - {grab} шт"
   f"\n ignore - {ignore} шт"
   f"\n Светофор на другой дороге - {svetofor} шт"
   f"\n Дублирующий - {doubler} шт"
   f"\n Основной - {basic} шт"
   f"\n fur - {fur} шт"
   f"\n vagon - {vagon} шт"
   f"\n item - {item} шт\n"
    "\n------------------------\n"
)
