import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

def decode(image_path, output_dir):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        return

    f = np.fft.fft2(image) # Преобразование Фурье
    fshift = np.fft.fftshift(f) #  Центровка спектра частот
    magnitude_spectrum = np.log(np.abs(fshift) + 1) # Построение спектра амплитуд

    # Нормализация и сохранение результата
    output_image = np.uint8(255 * magnitude_spectrum / np.max(magnitude_spectrum))

    # Формирование имени файла для сохранения
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    output_path = os.path.join(output_dir, f"{name}_dec{ext}")

    # Сохранение изображения
    cv2.imwrite(output_path, output_image)

    # plt.figure()
    # plt.imshow(magnitude_spectrum, cmap='gray')
    # plt.show()


input_dir = "task/img"
output_dir = "task/dec_img"

os.makedirs(output_dir, exist_ok=True)

# Перебор всех файлов
for file_name in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file_name)
    decode(file_path, output_dir)
