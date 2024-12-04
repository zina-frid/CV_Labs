import cv2
import time
import numpy as np
from dilation import dilate_native

# Загрузка изображения
image = cv2.imread('src/image.jpg', 0)
if image is None:
    raise FileNotFoundError("Image file not found. Check the file path.")

# Создание ядра
kernel = np.ones((3, 3), np.uint8)

print("----- Single Execution -----")

# OpenCV
dilated_image_cv = cv2.dilate(image, kernel)
cv2.imwrite('src/dilated_image_cv.png', dilated_image_cv)

# Нативная реализация
dilated_image_native = dilate_native(image, kernel)
cv2.imwrite('src/dilated_image_native.png', dilated_image_native)

print('Done.')

print("----- Average time -----")

# Функция для измерения времени
def measure_time(func, *args, iterations=100):
    times = []
    for _ in range(iterations):
        start_time = time.time()
        func(*args)
        times.append(time.time() - start_time)
    return np.mean(times)

# Среднее время OpenCV
opencv_time = measure_time(cv2.dilate, image, kernel)
print(f"Average OpenCV dilation time: {opencv_time:.6f} seconds")

# Среднее время нативной реализации
native_time = measure_time(dilate_native, image, kernel)
print(f"Average Native Python dilation time: {native_time:.6f} seconds")


print("----- Comparison -----")

# Загрузка сохранённых изображений
image1 = cv2.imread('src/dilated_image_cv.png', 0)
image2 = cv2.imread('src/dilated_image_native.png', 0)

# Попиксельное сравнение
total_pixels = image1.size
identical_pixels = np.sum(image1 == image2)
similarity = (identical_pixels / total_pixels) * 100

print(f"Images are {similarity:.2f}% identical.")