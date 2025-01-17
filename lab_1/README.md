# Лабораторная работа №1
## Цель
Научиться реализовывать один из простых алгоритмов обработки изображений.

## Задание 
1. Реализовать программу согласно варианту задания. Базовый алгоритм, используемый в программе, необходимо реализовать в 2 вариантах: с 
использованием встроенных функций какой-либо библиотеки (OpenCV, PIL и др.) и нативно на Python или C++. 
2. Сравнить быстродействие реализованных вариантов. 
3. Сделать отчёт в виде readme на GitHub, там же должен быть выложен исходный код.

## Вариант
Дилатация, примитив размера 3 на 3, бинаризацию можно не реализовывать вручную.

## Реализация

### Теоретическая база
Дилатация (расширение) — это морфологическая операция, используемая в обработке изображений для расширения белых областей изображения (объектов) за счет черных областей (фона). Операция заключается в применении структурного элемента (ядра) ко всем пикселям изображения, при этом в каждой области, охваченной ядром, пикселю присваивается максимальное значение из этой области.

Операция дилатации может быть полезна для заполнения пробелов внутри объектов или увеличения видимого размера объектов на изображении. Она применяется, например, при подготовке изображений для распознавания и выделения объектов.

<table align="center">
  <tr>
    <td align="center">
      <img src="src/origin.png" alt="Оригинальное изображение" width="250">
      <p>Оригинальное изображение</p>
    </td>
    <td align="center">
      <img src="src/dilation.png" alt="Результат дилатации" width="250">
      <p>Результат дилатации</p>
    </td>
  </tr>
</table>


#### Алгоритмы и принципы работы
**OpenCV реализация**: использует встроенную функцию `cv2.dilate`, которая применяет ядро ко всем пикселям изображения и выполняет операцию дилатации на основе оптимизированных функций библиотеки.
  
**Нативная реализация**: создается копия изображения с дополнительными пикселями по краям для обработки границ, после чего выполняется проход по каждому пикселю изображения. На каждом шаге применяется ядро 3x3, и пикселю присваивается максимальное значение в соответствующей области.

### Код нативной реализации
```python
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
```

## Результаты работы и тестирования

### Скриншоты и изображения
Ниже приведены результаты работы алгоритмов.

**Маленькое изображение**

<table align="center">
  <tr>
    <td align="center">
      <img src="src/image_1.png" alt="Оригинальное изображение" width="">
      <p>Оригинальное изображение</p>
    </td>
    <td align="center">
      <img src="src/dilated_image_cv_1.png" alt="Результат дилатации" width="">
      <p>OpenCV</p>
    </td>
    <td align="center">
      <img src="src/dilated_image_native_1.png" alt="Результат дилатации" width="">
      <p>Нативная реализация</p>
    </td>
  </tr>
</table>

**Большое изображение**

<table align="center">
  <tr>
    <td align="center">
      <img src="src/image_bin.jpg" alt="Оригинальное изображение" width="300">
      <p>Оригинальное изображение</p>
    </td>
    <td align="center">
      <img src="src/dilated_image_cv.png" alt="Результат дилатации" width="300">
      <p>OpenCV</p>
    </td>
    <td align="center">
      <img src="src/dilated_image_native.png" alt="Результат дилатации" width="300">
      <p>Нативная реализация</p>
    </td>
  </tr>
</table>


### Временные затраты

*Среднее время выполнения алгоритмов за 100 итераций*

Для оценки производительности каждого метода алгоритмы прогоняются по 100 раз. Вычисляется среднее время выполнения:

![Avg Time](src/results_time.png)

### Сравнение изображений

Выполняется побайтовое сравнение двух изображений (результатов OpenCV и нативного метода). Подсчитывается процент совпадения пикселей, что позволяет оценить точность реализации нативного алгоритма.

![Comp](src/results_comp.png)

## Выводы
Был реализован алгоритм делатации c ядром 3*3. Также было произведено сравнение с реализацией алгоритма из библиотеки OpenCV. Обе реализации успешно выполняют операцию дилатации, однако нативная реализация на Python значительно уступает по скорости функции из библиотеки OpenCV. Это связано с оптимизациями, реализованными в OpenCV, которые снижают временные затраты на обработку изображения.

## Использованные источники
[Документация OpenCV](https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html) 

[Erosion and Dilation of images using OpenCV in python](https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html)