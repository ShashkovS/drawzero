# Примеры DrawZero

На этой странице собрана галерея из 21 примера, которые поставляются вместе с библиотекой
DrawZero. Каждый блок ниже подтягивает код напрямую из каталога
`src/drawzero/examples`, поэтому вы видите ровно те же исходники, что и при установке
пакета. Используйте галерею как справочник: переходите от иллюстраций к коду, сверяйтесь
с комментариями в исходниках и экспериментируйте у себя в редакторе.

Используйте индекс ниже, чтобы быстро перейти к нужному примеру.

| Файл | Фокус | Ключевые идеи |
| --- | --- | --- |
| [`00_hello_world.py`](#00_hello_worldpy) | Первый рендеринг на холсте | Рисует холст с рамкой, разделяет текст на два языка и запускает цикл `run()`. |
| [`01_grid_and_coordinates.py`](#01_grid_and_coordinatespy) | Обзор системы координат | Рендерит вспомогательную сетку `grid()`, затем аннотирует различные примитивы в известных координатах. |
| [`02_loops_and_rgb_colors.py`](#02_loops_and_rgb_colorspy) | Искусство, управляемое циклом | Использует цикл `for` и случайные кортежи RGB для рисования вертикальных полос различной высоты. |
| [`03_simple_objects.py`](#03_simple_objectspy) | Каталог примитивов | Демонстрирует каждый примитив рисования (линии, круги, повернутые прямоугольники, многоугольники, выравнивание текста). |
| [`04_loops_sin_plot.py`](#04_loops_sin_plotpy) | Построение математических графиков | Строит синусоиду, сшивая короткие отрезки линий вдоль оси X. |
| [`05_points.py`](#05_pointspy) | Помощник [`Pt`](pt.md) как вектор/черепаха | Показывает, как класс `Pt` поддерживает арифметику, движение и вращение в стиле черепахи в циклах. |
| [`06_turtle_style.py`](#06_turtle_stylepy) | Рисование многоугольников с помощью [`Pt`](pt.md) | Вращает экземпляр `Pt` для построения правильных многоугольников для сторон от 3 до 10 с использованием операций черепахи. |
| [`07_animation_circles.py`](#07_animation_circlespy) | Минимальный цикл анимации | Изменяет положение, радиус и цвет круга с течением времени, вызывая `tick()` на каждом кадре. |
| [`08_animation_traffic_light.py`](#08_animation_traffic_lightpy) | Анимация на основе состояний | Повторно использует помощника для рисования светофора и использует `sleep()` для переключения цветов. |
| [`09_animation_rectangles.py`](#09_animation_rectanglespy) | Сложная анимация | Сочетает математику `Pt` с логикой вращения/орбиты, прозрачностью и условными эффектами. |
| [`10_animation_planets.py`](#10_animation_planetspy) | Орбитальное движение | Вычисляет круговое движение для пары планета/луна и перерисовывает каждый кадр. |
| [`11_transparency_and_line_width.py`](#11_transparency_and_line_widthpy) | Альфа-смешивание и толщина обводки | Демонстрирует различные значения альфа-канала и толщины линий на кругах, прямоугольниках, многоугольниках и эллипсах. |
| [`12_images.py`](#12_imagespy) | Рендеринг изображений | Загружает `cat.png` из папки примеров, демонстрирует масштабирование и альфа-канал при выводе изображений. |
| [`13_gradients.py`](#13_gradientspy) | Помощник [Gradient](gradient.md) | Создает несколько шкал `Gradient` и визуализирует их с помощью сложенных прямоугольников. |
| [`14_animation_close_vertex.py`](#14_animation_close_vertexpy) | Анимация графа близости | Перемещает случайные узлы `Pt` с циклическим движением, рисует линии между соседними парами и использует оверлей FPS. |
| [`15_animation_firework.py`](#15_animation_fireworkpy) | Система частиц | Реализует классы `Particle` и `Firework` с обновлениями физики, свечением на основе градиента и логикой очистки. |
| [`16_keyboard_and_mouse.py`](#16_keyboard_and_mousepy) | Обработка ввода | Читает массивы состояний клавиш и очереди событий для перемещения квадрата, отслеживания вводимых символов и следования за мышью. |
| [`17_mouse_tube.py`](#17_mouse_tubepy) | Эффект следа мыши | Захватывает `mouse_pos()` на каждом кадре, выращивает концентрические круги с градиентом по мере их старения. |
| [`18_game_stars.py`](#18_game_starspy) | Мини-игра 3D-звездное поле | Использует датаклассы, случайные звезды и управление WASD/QE для навигации по псевдо-3D полю. |
| [`19_game_colors.py`](#19_game_colorspy) | Игра на реакцию | Отображает слова-цвета в сравнении с фактическими цветами, обрабатывает выбор кнопок мыши со штрафами по времени. |
| [`20_game_racing.py`](#20_game_racingpy) | Многопользовательская мини-игра | Назначает отдельные привязки клавиш для каждой машины, прокручивает предварительно вычисленную дорогу и ведет счет для каждого игрока. |
| [`99_errors.py`](#99_errorspy) | Демонстрация сообщений об ошибках | Принудительно вызывает ошибки проверки в режиме `EJUDGE_MODE`, чтобы продемонстрировать локализованную диагностику, выдаваемую конвертерами. |

## Начало работы

Эти примеры показывают, как вывести первые примитивы на экран и разобраться с базовым
циклом `run()`.

### 00_hello_world.py

![00_hello_world](imgs/ex_00.png)
``` title="00_hello_world.py"
--8<-- "src/drawzero/examples/00_hello_world.py"
```

### 01_grid_and_coordinates.py

![01_grid_and_coordinates](imgs/ex_01.png)
``` title="01_grid_and_coordinates.py"
--8<-- "src/drawzero/examples/01_grid_and_coordinates.py"
```

## Использование циклов и цветов

Используйте циклы и случайные значения, чтобы быстро получать выразительные узоры и
научиться передавать цвета в именованном и RGB-форматах.

### 02_loops_and_rgb_colors.py

![02_loops_and_rgb_colors](imgs/ex_02.png)
``` title="02_loops_and_rgb_colors.py"
--8<-- "src/drawzero/examples/02_loops_and_rgb_colors.py"
```

### 03_simple_objects.py

![03_simple_objects](imgs/ex_03.png)
``` title="03_simple_objects.py"
--8<-- "src/drawzero/examples/03_simple_objects.py"
```

### 04_loops_sin_plot.py

![04_loops_sin_plot](imgs/ex_04.png)
``` title="04_loops_sin_plot.py"
--8<-- "src/drawzero/examples/04_loops_sin_plot.py"
```

## Точки и черепашья графика

Класс `Pt` из публичного API работает и как вектор, и как "черепаха". Эти примеры показывают
арифметику точек и построение фигур через повороты и смещения.

### 05_points.py

![05_points](imgs/ex_05.png)
``` title="05_points.py"
--8<-- "src/drawzero/examples/05_points.py"
```

### 06_turtle_style.py

![06_turtle_style](imgs/ex_06.png)
``` title="06_turtle_style.py"
--8<-- "src/drawzero/examples/06_turtle_style.py"
```

## Анимация

Здесь начинается анимация: цикл `while True`, `tick()`, `clear()` и дополнительные эффекты,
которые встречаются в примерах `07`–`10`.

### 07_animation_circles.py

![07_animation_circles](imgs/ex_07.webp)
``` title="07_animation_circles.py"
--8<-- "src/drawzero/examples/07_animation_circles.py"
```

### 08_animation_traffic_light.py

![08_animation_traffic_light](imgs/ex_08.webp)
``` title="08_animation_traffic_light.py"
--8<-- "src/drawzero/examples/08_animation_traffic_light.py"
```

### 09_animation_rectangles.py

![09_animation_rectangles](imgs/ex_09.webp)
``` title="09_animation_rectangles.py"
--8<-- "src/drawzero/examples/09_animation_rectangles.py"
```

### 10_animation_planets.py

![10_animation_planets](imgs/ex_10.webp)
``` title="10_animation_planets.py"
--8<-- "src/drawzero/examples/10_animation_planets.py"
```

## Продвинутое рисование

Эти скрипты раскрывают дополнительные функции библиотеки: прозрачность, загрузку изображений
и градиенты, на которых основаны многие визуальные эффекты из исходников.

### 11_transparency_and_line_width.py

![11_transparency_and_line_width](imgs/ex_11.png)
``` title="11_transparency_and_line_width.py"
--8<-- "src/drawzero/examples/11_transparency_and_line_width.py"
```

### 12_images.py

![12_images](imgs/ex_12.png)
``` title="12_images.py"
--8<-- "src/drawzero/examples/12_images.py"
```

### 13_gradients.py

![13_gradients](imgs/ex_13.png)
``` title="13_gradients.py"
--8<-- "src/drawzero/examples/13_gradients.py"
```

## Интерактивные примеры

Добавьте управление с клавиатуры и мыши, чтобы рисунки реагировали на пользователя в реальном времени.

### 14_animation_close_vertex.py

![14_animation_close_vertex](imgs/ex_14.webp)
``` title="14_animation_close_vertex.py"
--8<-- "src/drawzero/examples/14_animation_close_vertex.py"
```

### 15_animation_firework.py

![15_animation_firework](imgs/ex_15.webp)
``` title="15_animation_firework.py"
--8<-- "src/drawzero/examples/15_animation_firework.py"
```

### 16_keyboard_and_mouse.py

![16_keyboard_and_mouse](imgs/ex_16.webp)
``` title="16_keyboard_and_mouse.py"
--8<-- "src/drawzero/examples/16_keyboard_and_mouse.py"
```

### 17_mouse_tube.py

![17_mouse_tube](imgs/ex_17.webp)
``` title="17_mouse_tube.py"
--8<-- "src/drawzero/examples/17_mouse_tube.py"
```

## Игры

И, наконец, несколько мини-игр, собранных из примитивов, анимации и обработки ввода.

### 18_game_stars.py

![18_game_stars](imgs/ex_18.webp)
``` title="18_game_stars.py"
--8<-- "src/drawzero/examples/18_game_stars.py"
```

### 19_game_colors.py

![19_game_colors](imgs/ex_19.webp)
``` title="19_game_colors.py"
--8<-- "src/drawzero/examples/19_game_colors.py"
```

### 20_game_racing.py

![20_game_racing](imgs/ex_20.webp)
``` title="20_game_racing.py"
--8<-- "src/drawzero/examples/20_game_racing.py"
```
