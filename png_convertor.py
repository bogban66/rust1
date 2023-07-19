import os
from PIL import Image

# Шлях до папки з зображеннями
image_dir = 'D:/d/python/s/pythonProject/f/twitch_bot/11/rust/image'

# Отримання списку файлів зображень
image_files = os.listdir(image_dir)

# Проходження по кожному файлу зображення
for image_file in image_files:
    if image_file.endswith('.jpg') or image_file.endswith('.jpeg'):
        # Завантаження зображення
        image_path = os.path.join(image_dir, image_file)
        image = Image.open(image_path)

        # Генерація нового шляху для зображення у форматі PNG
        new_image_path = os.path.splitext(image_path)[0] + '.png'

        # Конвертація та збереження зображення у форматі PNG
        image.save(new_image_path, 'PNG')
        print(f"Зображення {image_file} конвертовано у формат PNG.")
