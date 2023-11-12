from drawzero import *
import random
import math
from typing import List

G = -2.0


class Particle:
    vx: float
    vy: float
    cx: float
    cy: float
    color: tuple
    alive: bool
    max_age: int
    age: int = 0
    GLOW = 20
    START_SPEED = 20
    MAX_SIZE = 4
    SCALE = Gradient([C.yellow, C.red], 0, GLOW)

    def __init__(p, x, y):
        random_angle = random.uniform(0, 2 * math.pi)
        random_speed = random.uniform(p.START_SPEED * 0.5, p.START_SPEED * 1.5)
        p.vx = math.cos(random_angle) * random_speed
        p.vy = math.sin(random_angle) * random_speed
        p.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        p.cx, p.cy = x, y
        p.max_age = random.randint(5, p.GLOW)
        p.alive = True

    def draw(p):
        if p.age < p.GLOW:
            color = p.SCALE(p.age)
            filled_circle(color, (p.cx, p.cy), p.MAX_SIZE * (p.GLOW - p.age) / p.GLOW)

    def update(p):
        p.cx += p.vx
        p.cy += p.vy
        p.vy -= G
        p.age += 1
        if p.cy > 1000 or p.age > p.max_age:
            p.alive = False


class Firework:
    STICK_WIDTH = 5
    HANDLE = 200
    NEW_PARTICLES = 25
    HANDLE_COLOR = (64, 64, 64)
    POWDER_COLOR = (255, 255, 255)
    BURNT_COLOR = (102, 102, 102)

    def __init__(self, x, y, height, sleep=2):
        self.ticks = 0
        self.x = x
        self.y = y
        self.height = height
        self.particles: List[Particle] = []
        self.cur_top = 0
        self.sleep = sleep

    def update(self):
        self.ticks += 1
        if self.ticks < 30 * self.sleep or self.cur_top > self.height:
            return
        self.cur_top += 1
        self.update_particles()
        self.remove_particles()
        self.create_new_particles()

    def draw(self):
        self.draw_stick()
        for p in self.particles:
            p.draw()

    def remove_particles(self):
        last_good = -1
        for cur in range(len(self.particles)):
            p = self.particles[cur]
            if p.alive:
                last_good += 1
                self.particles[last_good] = p
        del self.particles[last_good + 1:]

    def update_particles(self):
        for p in self.particles:
            p.update()

    def create_new_particles(self):
        if self.cur_top < self.height - self.HANDLE:
            for __ in range(self.NEW_PARTICLES):
                self.particles.append(Particle(x=self.x, y=self.y + self.cur_top))

    def draw_stick(self):
        w = self.STICK_WIDTH
        real_top = min(self.cur_top, self.height - self.HANDLE)
        filled_rect(self.HANDLE_COLOR, (self.x - w / 2, self.y), w, self.height)
        filled_rect(self.BURNT_COLOR, (self.x - w / 2 - 2, self.y), w + 4, real_top)
        filled_rect(self.POWDER_COLOR, (self.x - w / 2 - 3, self.y + real_top), w + 6, self.height - self.HANDLE - real_top)

    def is_burnt(self):
        return self.cur_top > 0 and len(self.particles) == 0


firework1 = Firework(x=333, y=200, height=600, sleep=1)
firework2 = Firework(x=666, y=400, height=500, sleep=2)

while not firework1.is_burnt() or not firework2.is_burnt():
    firework1.update()
    firework2.update()
    tick()
    clear()
    firework1.draw()
    firework2.draw()
    fps()

sleep(1)
quit()
