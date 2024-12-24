import cv2
import os
import numpy as np

def decode(image_path, output_dir):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    if image is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        return

    # Разделяем каналы: амплитудный спектр (R), фаза (G)
    magnitude_spectrum = image[:, :, 0].astype(np.float32)  # Канал R
    angle = image[:, :, 1].astype(np.float32)  # Канал G
    
    # Восстанавливаем амплитудный спектр
    magnitude = np.exp(magnitude_spectrum / 20)  # Убираем логарифм
    
    # Восстанавливаем угловую фазу
    angle = angle / 6.0 * 2 * np.pi - np.pi  # Масштабируем из [0, 6] в [-π, π]
    
    # Формируем комплексное представление
    fshift = magnitude * np.exp(1j * angle)
    
    # Обратный сдвиг
    f_ishift = np.fft.ifftshift(fshift)
    
    # Обратное преобразование Фурье
    img_reconstructed = np.fft.ifft2(f_ishift)
    img_reconstructed = np.abs(img_reconstructed)
    
    # Нормализуем изображение для визуализации
    img_reconstructed = cv2.normalize(img_reconstructed, None, 0, 255, cv2.NORM_MINMAX)
    img_reconstructed = img_reconstructed.astype(np.uint8)

    # Формирование имени файла для сохранения
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    output_path = os.path.join(output_dir, f"{name}_dec_inv{ext}")

    # Сохранение изображения
    cv2.imwrite(output_path, img_reconstructed)


input_dir = "task/img"
output_dir = "task/inv_dec_img"

os.makedirs(output_dir, exist_ok=True)

# Перебор всех файлов в папке
for file_name in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file_name)
    decode(file_path, output_dir)
