from drawzero import *
import random
from time import time

COLORS = [('жёлтый', 'yellow'), ('зелёный', 'green'), ('голубой', '#42aaff'), ('синий', '#0000ff'), ('фиолетовый', 'purple'), ('красный', 'red'),
          ('оранжевый', 'orange'), ('коричневый', 'brown'), ('серый', 'gray'), ('белый', 'white'), ]


def gen_new():
    cur_word, color = random.choice(COLORS)
    corr = True
    if random.random() < 0.5:
        corr = False
        new_color = color
        while new_color == color:
            __, color = random.choice(COLORS)
    return cur_word, color, corr


score = 0
cur_timelimit = 4
cur_word, color, corr = gen_new()
cur_status = None
round_start = last_status_ts = time()
while True:
    cur_ts = time()
    time_left = round_start + cur_timelimit - cur_ts
    if time_left < 0:
        score -= 1
        cur_timelimit *= 1.02
        cur_word, color, corr = gen_new()
        round_start = last_status_ts = cur_ts
        cur_status = None
        time_left = cur_timelimit
    clear()
    text('white', f'Ваши очки: {score}', (500, 50), 48)
    text('white', f'Дважды кликните левой кнопкой мыши,', (500, 100), 32)
    text('white', f'если совпадает слово и цвет, иначе — правой', (500, 142), 32)
    text('white', f'{time_left:0.2f}с...', (500, 600), 48)
    text(color, cur_word, (500, 500), 120)
    if cur_status == 1:
        text('green', 'Совпадают?', (500, 700), 48)
    elif cur_status == 3:
        text('red', 'Различаются?', (500, 800), 48)
    # Половина секунды после смены цвета игнорируем нажатия
    for ev in mousebuttonsdown:
        if cur_ts - last_status_ts > 0.3:
            if ev.button == cur_status:
                # Пользователь подтвердил
                if (corr and cur_status == 1) or (not corr and cur_status == 3):
                    score += 1
                    cur_timelimit *= 0.95
                else:
                    score -= 1
                    cur_timelimit *= 1.02
                cur_word, color, corr = gen_new()
                round_start = last_status_ts = cur_ts
                cur_status = None
            elif ev.button in (1, 3):
                cur_status = ev.button
                last_status_ts = cur_ts
    tick()
