import os
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = []
    for obj in root.findall('object'):
        # Отримання даних про об'єкт
        name = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)

        # Додавання даних в список
        data.append({
            'filename': os.path.basename(xml_file).replace('.xml', '.jpg'),
            'width': root.find('size/width').text,
            'height': root.find('size/height').text,
            'class': name,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax
        })

    # Створення DataFrame зі списку даних
    df = pd.DataFrame(data)
    return df

def convert_xml_to_csv(xml_folder, csv_output):
    xml_files = []
    for root, dirs, files in os.walk(xml_folder):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))

    for xml_file in xml_files:
        csv_file = os.path.join(csv_output, os.path.basename(xml_file).replace('.xml', '.csv'))
        df = xml_to_csv(xml_file)
        df.to_csv(csv_file, index=False)
        print('Successfully converted XML to CSV:', csv_file)

# Задайте шлях до папки з XML файлами та шлях до вихідної папки для CSV файлів
xml_folder = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/xmls'
csv_output = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/csv'

# Виклик функції конвертування
convert_xml_to_csv(xml_folder, csv_output)
