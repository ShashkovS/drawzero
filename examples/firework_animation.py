from drawzero import *
import random
import math
from dataclasses import dataclass

START = START_X, START_Y = (500, 200)
G = -2.0
START_SPEED = 20
STICK_WIDTH = 5
TOP = 600
SAFE = 200
GLOW = 15


@dataclass
class Particle:
    vx: float
    vy: float
    cx: float
    cy: float
    color: tuple
    alive: bool
    max_age: int
    age: int = 0

    def __init__(p, move_y):
        random_angle = random.uniform(0, 2 * math.pi)
        random_speed = random.uniform(START_SPEED * 0.5, START_SPEED * 1.5)
        p.vx = math.cos(random_angle) * random_speed
        p.vy = math.sin(random_angle) * random_speed
        p.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        p.cx, p.cy = START_X, START_Y + move_y
        p.max_age = random.randint(5, 13)
        p.alive = True

    def draw(p):
        s = [255, 255, 204]
        f = [230, 230, 0]
        if p.age > GLOW:
            color = f
        else:
            color = [
                s[c] * (GLOW - p.age) / GLOW + f[c] * (p.age) / GLOW
                for c in (0, 1, 2)
            ]
        filled_circle(color, (p.cx, p.cy), 4 - p.age // 6)

    def update(p):
        p.cx += p.vx
        p.cy += p.vy
        p.vy -= G
        p.age += 1
        if p.cy > 1000 or p.age > p.max_age:
            p.alive = False


def draw_particles(particles):
    for p in particles:
        p.draw()


def remove_particles(particles):
    last_good = -1
    for cur in range(len(particles)):
        p = particles[cur]
        if p.alive:
            last_good += 1
            particles[last_good] = p
    del particles[last_good + 1:]


def update_particles(particles):
    for p in particles:
        p.update()


def draw_stick(done):
    border = min(done, TOP - SAFE)
    filled_rect((102, 102, 102), (START_X - STICK_WIDTH / 2 - 2, START_Y), STICK_WIDTH + 4, border)
    filled_rect('white', (START_X - STICK_WIDTH / 2 - 3, START_Y + border), STICK_WIDTH + 6, TOP - border - SAFE)
    filled_rect((64, 64, 64), (START_X - STICK_WIDTH / 2, START_Y + TOP - SAFE), STICK_WIDTH, SAFE)


draw_stick(0)
sleep(1)

particles = []
move_y = 0
while move_y < TOP + 50:
    move_y += 1
    if move_y < TOP - SAFE:
        for __ in range(25):
            particles.append(Particle(move_y=move_y))
    fill('black')
    draw_stick(move_y)
    draw_particles(particles)
    tick()
    update_particles(particles)
    remove_particles(particles)
