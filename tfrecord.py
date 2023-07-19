import os
import io
import pandas as pd
import tensorflow as tf
from PIL import Image

from object_detection.utils import dataset_util

def class_text_to_int(row_label, label_map_path):
    label_map_dict = {}
    with open(label_map_path, 'r') as f:
        name = None  # Ініціалізуємо змінну `name` як None
        for line in f:
            if 'name:' in line:
                name = line.split(':')[-1].strip().replace("'", "")
            elif 'id:' in line:
                class_id = int(line.split(':')[-1])
                if name is not None:  # Перевіряємо, чи змінна `name` була знайдена
                    label_map_dict[name] = class_id

    return label_map_dict.get(row_label)


def create_tf_example(row, image_dir, label_map_path):
    filename = row['filename']
    img_path = os.path.join(image_dir, filename)
    with tf.io.gfile.GFile(img_path, 'rb') as fid:
        encoded_image = fid.read()
    encoded_image_io = io.BytesIO(encoded_image)
    image = Image.open(encoded_image_io)
    width, height = image.size

    xmins = [row['xmin'] / width]
    xmaxs = [row['xmax'] / width]
    ymins = [row['ymin'] / height]
    ymaxs = [row['ymax'] / height]
    classes_text = [row['class'].encode('utf8')]
    classes = [class_text_to_int(row['class'], label_map_path)]

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename.encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(filename.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_image),
        'image/format': dataset_util.bytes_feature(b'jpeg'),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example

def create_tfrecord(csv_input, image_dir, label_map_path, output_path):
    writer = tf.io.TFRecordWriter(output_path)
    examples = pd.read_csv(csv_input)
    for _, row in examples.iterrows():
        tf_example = create_tf_example(row, image_dir, label_map_path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    print('Successfully created TFRecord file:', output_path)

# Шлях до CSV файлу зі всіма мітками
all_labels_csv = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/csv/all/annotations.csv'

# Шлях до папки з зображеннями
image_dir = 'D:\\d\\python\\s\\pythonProject\\f\\twitch_bot\\11\\rust\\image'

# Шлях до labelmap.pbtxt
label_map_path = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/labelmap.pbtxt'

# Вихідний шлях для TFRecord файлу
output_tfrecord = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/output.tfrecord'

# Створення TFRecord файлу
create_tfrecord(all_labels_csv, image_dir, label_map_path, output_tfrecord)
