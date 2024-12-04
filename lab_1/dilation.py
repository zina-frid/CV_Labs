import numpy as np

# Нативная реализация дилатации
def dilate_native(image, kernel):
    # Создаем изображение с отступом в 1 пиксель (для обработки границ)
    # Используем нулевые значения (черный цвет) для заполнения отступа
    padded_image = np.pad(image, 1, mode='constant', constant_values=0)

    # Пустое изображение для сохранения результата
    dilated_image = np.zeros_like(image)

    # Проходим по каждому пикселю исходного изображения
    for i in range(1, image.shape[0] + 1):
        for j in range(1, image.shape[1] + 1):
            # Применяем ядро, используя максимум значений в области
            dilated_image[i-1, j-1] = np.max(padded_image[i-1:i+2, j-1:j+2] * kernel)

    return dilated_image