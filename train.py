import os
import tensorflow as tf
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from google.protobuf import text_format
from object_detection.utils import label_map_util
from object_detection import model_lib

def load_labelmap(label_map_path):
    with open(label_map_path, 'r') as fid:
        label_map_string = fid.read()
    label_map = label_map_util.string_int_label_map_pb2.StringIntLabelMap()
    label_map = text_format.Parse(label_map_string, label_map)
    return label_map

def load_xml_labels(xml_path, label_map):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    labels = []
    for obj in root.findall('object'):
        label = obj.find('name').text
        for item in label_map.item:
            if item.name == label:
                labels.append(item.id)

    return np.array(labels, dtype=np.int32)

# Шлях до папки з зображеннями та мітками
image_dir = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/image'
xml_dir = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/xmls'

# Завантаження списку файлів зображень та міток
image_files = os.listdir(image_dir)
xml_files = os.listdir(xml_dir)

# Шлях до файлу labelmap.pbtxt
label_map_path = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/labelmap.pbtxt'

# Завантаження мапи міток з файлу labelmap.pbtxt
label_map = load_labelmap(label_map_path)

# Створення списків для зберігання даних
train_images = []
train_labels = []

# Розмір, до якого потрібно змінити зображення
target_size = (224, 224)

# Проходження по кожному файлу зображення
for image_file in image_files:
    if image_file.endswith('.jpg') or image_file.endswith('.png'):
        # Завантаження зображення
        image_path = os.path.join(image_dir, image_file)
        image = Image.open(image_path)
        
        # Зміна розміру та каналів кольору зображення
        resized_image = image.resize(target_size)
        if resized_image.mode != 'RGB':
            resized_image = resized_image.convert('RGB')
        
        # Конвертація зображення в масив та попередня обробка
        image_array = tf.keras.preprocessing.image.img_to_array(resized_image)
        image_array = tf.keras.applications.imagenet_utils.preprocess_input(image_array, mode='tf')
        
        # Отримання відповідного файлу мітки XML
        xml_file = image_file[:-4] + '.xml'
        if xml_file in xml_files:
            # Завантаження та обробка мітки XML
            xml_path = os.path.join(xml_dir, xml_file)
            xml_label = load_xml_labels(xml_path, label_map)
            
            # Додавання зображення та мітки до списків, тільки якщо мітка існує
            if len(xml_label) > 0:
                train_images.append(image_array)
                train_labels.append(xml_label)

# Перевірка, чи всі зображення мають мітки
if len(train_images) != len(train_labels):
    raise ValueError('Some images do not have corresponding labels.')

# Перетворення списків у тензори з використанням stack
train_images = tf.stack(train_images)

# Завантаження конфігураційного файлу моделі
config_path = 'D:\\d\\python\\s\\pythonProject\\f\\twitch_bot\\11\\rust\\faster_rcnn_inception_v2_pets.config'

model = model_lib.TFODModel(config_path)
model.build_model()
# Компіляція моделі
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Тренування моделі
model.fit(train_images, train_labels, epochs=10, batch_size=32)

# Збереження моделі
model_dir = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/model'
model.save(os.path.join(model_dir, 'tree_detection_model.h5'))
