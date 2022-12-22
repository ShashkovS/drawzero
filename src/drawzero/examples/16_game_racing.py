from drawzero import *

cars_y = [540, 500, 460]
cars_x = [100, 100, 100]
ups = [K.w, K.i, K.UP]
downs = [K.s, K.k, K.DOWN]
lefts = [K.a, K.j, K.LEFT]
rights = [K.d, K.l, K.RIGHT]
colors = ['green', 'blue', 'yellow']
scores = [1000, 1000, 1000]

road = [500] * 30 + list(range(500, 700, 3)) + list(range(700, 900, 6)) + list(range(900, 100, -4)) + list(
    range(100, 500, 8))
road.extend(road)
road.extend(road)
WIDTH2 = 80
road_pos = 0
for i in 3, 2, 1:
    clear()
    text('green', 'READY? ' + str(i), (300, 400), 128)
    sleep(1)

while True:
    keys = get_keys_pressed()
    for i in range(len(cars_y)):
        if keys[ups[i]]:
            cars_y[i] -= 5
        if keys[downs[i]]:
            cars_y[i] += 5
        if keys[lefts[i]]:
            cars_x[i] -= 5
        if keys[rights[i]]:
            cars_x[i] += 5
    clear()
    for i in range(len(cars_y)):
        filled_rect(colors[i], (cars_x[i], cars_y[i] - 20), 80, 40, alpha=70)
    for i in range(100):
        line('red', i * 10, road[i + road_pos] - WIDTH2, i * 10 + 10, road[i + 1 + road_pos] - WIDTH2)
        line('red', i * 10, road[i + road_pos] + WIDTH2, i * 10 + 10, road[i + 1 + road_pos] + WIDTH2)
    for i in range(len(cars_y)):
        if cars_y[i] - 20 < road[cars_x[i] // 10 + road_pos] - WIDTH2:
            text(colors[i], 'Boom!', (300 + 200 * i, 10), 72)
            cars_y[i] = road[cars_x[i] // 10 + road_pos] - WIDTH2 + 20
            scores[i] -= 1
        elif cars_y[i] + 20 > road[cars_x[i] // 10 + road_pos] + WIDTH2:
            text(colors[i], 'Boom!', (300 + 200 * i, 10), 72)
            cars_y[i] = road[cars_x[i] // 10 + road_pos] + WIDTH2 - 20
            scores[i] -= 1
        text(colors[i], str(scores[i]), (300 + 200 * i, 100), 72)

    tick()
    road_pos += 1
    if road_pos > 1000:
        i = scores.index(max(scores))
        text('white', f'{colors[i]} is winner!', (150, 900), 128)
        tick()
        break
