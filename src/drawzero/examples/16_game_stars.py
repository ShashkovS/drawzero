from drawzero import *
from random import randint
from dataclasses import dataclass

from time import perf_counter
NUM_STARS = 300


@dataclass
class Star:
    x: float
    y: float
    z: float
    r: int
    color: tuple


def gen_star():
    '''Создать звезду'''
    x = randint(-1000000 // 2, 1000000 // 2)
    y = randint(1, 1000)
    z = randint(-1000000 // 2, 1000000 // 2)
    r = randint(10, 3000)
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    return Star(x, y, z, r, color)


def create_stars():
    '''Создать массив звёзд'''
    stars = []
    for i in range(NUM_STARS):
        stars.append(gen_star())
    return stars


def move_stars(stars, speed):
    '''Сдвинуть все звёзды
    Если звезда перестала попадать на экран, то заменяем её на новую'''
    Vx, Vy, Vz = speed
    for i, star in enumerate(stars):
        star.x += Vx
        star.y += Vy
        star.z += Vz
        if (
                not (1 < star.y < 1000)
                or not (-500 < star.x / star.y < 500)
                or not (-500 < star.x / star.y < 500)
        ):
            # Вообще это — так себе решение. Но частично работает
            stars[i] = gen_star()


def draw_stars(stars):
    '''Отрисовать все звёзды'''
    # Сортируем звёзды, чтобы те, которые ближе к экрану, отрисовывались позже
    stars.sort(key=lambda star: -star.y)
    for star in stars:
        y = star.y
        screen_x = 500 + star.x / y
        screen_y = 500 + star.z / y
        screen_r = star.r / y
        filled_circle(star.color, (screen_x, screen_y), screen_r)
    text('white', 'Press WASD or QE to move', (500, 5), 48, '.^')


def process_keys(pressed_keys, speed):
    '''Обрабатываем нажатия клавиш
    Используем WASD для вверх/вниз/влево/вправо и QE для вперёд/назад'''
    if pressed_keys[K.UP] or pressed_keys[K.w]:
        speed[2] += 100
    if pressed_keys[K.DOWN] or pressed_keys[K.s]:
        speed[2] -= 100
    if pressed_keys[K.LEFT] or pressed_keys[K.a]:
        speed[0] += 100
    if pressed_keys[K.RIGHT] or pressed_keys[K.d]:
        speed[0] -= 100
    if pressed_keys[K.q]:
        speed[1] -= 1
    if pressed_keys[K.e]:
        speed[1] += 1


# Здесь ставим размер экрана
stars = create_stars()
# Текущая скорость, стартуем с 0
speed = [0, 0, 0]
while True:
    # Заливаем всё чёрным
    fill((0, 0, 0))
    # Обрабатываем нажатия клавиш
    process_keys(get_keys_pressed(), speed)
    # Двигаем звёзды
    move_stars(stars, speed)
    # Рисуем звёзды
    draw_stars(stars)
    # Ждём 1/60 секунды
    tick()
