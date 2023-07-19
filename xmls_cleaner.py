import os
import shutil

source_dir = r'D:\d\python\s\pythonProject\f\twitch_bot\11\rust\image'
target_dir = r'D:\d\python\s\pythonProject\f\twitch_bot\11\rust\xmls'

# Перевірка наявності цільової папки, якщо не існує, то створюємо її
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Проходимо по всіх файлів у вихідній папці
for filename in os.listdir(source_dir):
    if filename.endswith('.xml'):
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        shutil.move(source_file, target_file)
        print(f'Файл {filename} перенесено у папку {target_dir}.')
