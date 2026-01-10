# Ввод с клавиатуры и мыши

Эта страница объясняет, как считывать ввод с клавиатуры и мыши при создании
интерактивного рисунка с помощью DrawZero.

## Цикл событий и tick

Программы реального времени должны проверять ввод много раз в секунду. В
DrawZero это делает `tick()`: он опрашивает очередь событий pygame, обновляет
состояние клавиш и мыши и переводит координаты мыши в виртуальный холст
1000x1000. Вызывайте `tick()` один раз за кадр (обычно в конце цикла).

```python
from drawzero import *

while True:
    # читаем ввод, собранный последним tick()
    # обновляем состояние + рисуем
    tick()  # обрабатывает события и держит ~30 FPS
```

Если перестать вызывать `tick()`, окно зависнет, а ввод перестанет обновляться.

## Функции состояния

### `get_keys_pressed()`

Возвращает объект `KeysPressed` (обертка над `pygame.key.get_pressed()`). Он
ведет себя как список булевых значений и принимает коды клавиш или их имена.

```python
from drawzero import *

keys = get_keys_pressed()
if keys[K.LEFT] or keys[K.a]:
    player_x -= 5
if keys["SPACE"]:
    player_jump()
```

Используйте константы `K`/`KEY` для надежных названий (например, `K.LEFT`,
`K.SPACE`, `K.a`).

### `keys_mods_pressed()`

Возвращает **битовую маску** активных модификаторов (как
`pygame.key.get_mods()`). Проверяйте ее через `&` и константы `K.MOD_*`.

```python
from drawzero import *

mods = keys_mods_pressed()
if mods & K.MOD_CTRL and get_keys_pressed()[K.s]:
    save_project()
if mods & K.MOD_SHIFT:
    speed *= 2
```

### `get_mouse_pressed()`

Возвращает кортеж булевых значений `(left, middle, right)` — какие кнопки мыши
удерживаются.

```python
from drawzero import *

left, middle, right = get_mouse_pressed()
if left:
    draw_circle(mouse_pos(), radius=10)
```

### `mouse_pos()`

Возвращает текущее положение мыши в **виртуальных координатах холста**.

## Очереди событий

Очереди событий — это **списки**, которые очищаются при каждом `tick()`. Они
содержат объекты событий `pygame`, пришедшие с предыдущего тика, в порядке
поступления.

### `keysdown` / `keysup`

Списки событий нажатия и отпускания клавиш. Используйте `event.key` для
сравнения с константами `K`, а `event.unicode` — для введенного символа.

```python
from drawzero import *

for event in keysdown:
    if event.key == K.SPACE:
        spawn_bullet()
    if event.unicode:
        typed_text += event.unicode
```

`event.mod` содержит битовую маску модификаторов, если это нужно.

Если нужен не текст, а только конкретные клавиши (стрелки, пробел, escape),
сравнивайте `event.key` напрямую:

```python
from drawzero import *

for event in keysdown:
    if event.key == K.SPACE:
        print("space")
    elif event.key == K.LEFT:
        print("left")
```

### `mousemotions`

Список событий движения мыши. У каждого события есть:

- `event.pos` — текущая позиция курсора (виртуальные координаты)
- `event.rel` — смещение с прошлого события
- `event.buttons` — кортеж удерживаемых кнопок мыши

```python
from drawzero import *

for event in mousemotions:
    trail.add_point(event.pos)
```

### `mousebuttonsdown` / `mousebuttonsup`

Списки событий нажатия и отпускания кнопок мыши. У каждого события есть:

- `event.button` — номер кнопки (`1` левая, `2` средняя, `3` правая, `4/5` колесо)
- `event.pos` — позиция клика (виртуальные координаты)

```python
from drawzero import *

for event in mousebuttonsdown:
    if event.button == 1:
        start_drag(event.pos)
```

Можно сразу читать координаты клика и номер кнопки:

```python
from drawzero import *

for event in mousebuttonsdown:
    x, y = event.pos
    print(f"button={event.button} pos=({x:.1f}, {y:.1f})")
```

## Собираем все вместе

```python
from drawzero import *

while True:
    keys = get_keys_pressed()
    if keys[K.LEFT]:
        player.move(-5, 0)
    if keys[K.RIGHT]:
        player.move(5, 0)

    for event in keysdown:
        if event.key == K.SPACE:
            player.jump()

    for event in mousebuttonsdown:
        if event.button == 1:
            player.shoot(event.pos)

    # обновите холст здесь
    tick()
```

Сравните этот шаблон с примером `16_keyboard_and_mouse.py` в
[Примерах](examples.md).

## Советы по плавному взаимодействию

- Регулярно вызывайте `tick()`, чтобы ввод был актуальным.
- Избегайте длительного блокирующего кода (например, `time.sleep(5)`) внутри цикла.
- Используйте `keys_mods_pressed()` вместе с `K.MOD_*` для сочетаний клавиш.
- Если нужно только последнее положение мыши, вызывайте `mouse_pos()`.
- Печатайте события во время разработки, чтобы увидеть реальные значения.

## Где узнать больше

- [Основы анимации](animation.md) объясняет, как `tick()` вписывается в
  конвейер рисования.
- [Примеры](examples.md) указывают на готовые скрипты, которые вы
  можете запускать и изменять.
