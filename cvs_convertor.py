import os
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(xml_folder):
    xml_files = os.listdir(xml_folder)
    data = []

    for xml_file in xml_files:
        if not xml_file.endswith('.xml'):
            continue

        xml_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for obj in root.findall('object'):
            # Отримання даних про об'єкт
            name = obj.find('name').text
            xmin = int(obj.find('bndbox/xmin').text)
            ymin = int(obj.find('bndbox/ymin').text)
            xmax = int(obj.find('bndbox/xmax').text)
            ymax = int(obj.find('bndbox/ymax').text)

            # Додавання даних в список
            data.append({
                'filename': xml_file.replace('.xml', '.jpg'),
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
    df = xml_to_csv(xml_folder)
    df.to_csv(csv_output, index=False)
    print('Successfully converted XML to CSV:', csv_output)

# Задайте шлях до папки з XML файлами та шлях до вихідного CSV файлу
xml_folder = "D:\d\python\s\pythonProject\f\twitch_bot\11\rust\xmls"
csv_output = 'шлях/до/вихідного.csv'

# Виклик функції конвертування
convert_xml_to_csv(xml_folder, csv_output)
