import cv2
import numpy as np

# Реализация метода Template Matching
def template_matching(image, template):
    # Выполняем прямое сопоставление шаблона с изображением
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    
    # Находим координаты с максимальным совпадением
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc  # Верхний левый угол области совпадения
    
    # Рассчитываем нижний правый угол области на основе размеров шаблона
    h, w = template.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    return top_left, bottom_right  # Возвращаем координаты прямоугольника

# Реализация метода SIFT Matching
def sift_matching(image, template):
    # Создаем объект SIFT
    sift = cv2.SIFT_create()
    
    # Находим ключевые точки и дескрипторы для шаблона и изображения
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(image, None)
    
    # Используем BFMatcher для сопоставления дескрипторов
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)  # Сортируем по расстоянию
    
    # Получаем координаты совпавших точек
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    # Рассчитываем гомографию для преобразования координат
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    # Преобразуем координаты углов шаблона в координаты на входном изображении
    h, w = template.shape[:2]
    pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    
    return np.int32(dst)  # Возвращаем координаты четырехугольника

# Функция для отображения рамки на изображении
def draw_rectangle(image, points):
    if isinstance(points, tuple):  # Если это прямоугольник (template matching)
        top_left, bottom_right = points
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # Рисуем прямоугольник
    else:  # Если это четырехугольник (SIFT matching)
        cv2.polylines(image, [points], True, (255, 0, 0), 2)  # Рисуем полилинию
    return image


# Применяем Template Matching
def template_method(image, template):
    image, gray_image, gray_template = image_process(image, template)
    rect = template_matching(gray_image, gray_template)
    image_with_rect = draw_rectangle(image.copy(), rect)
    return image_with_rect

# Применяем SIFT Matching
def sift_method(image, template):
    image, gray_image, gray_template = image_process(image, template)
    polygon = sift_matching(gray_image, gray_template)
    image_with_polygon = draw_rectangle(image.copy(), polygon)
    return image_with_polygon


def image_process(image, template):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Преобразуем в градации серого
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # Преобразуем в градации серого
    return image, gray_image, gray_template