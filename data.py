import copy

import pygame as pg
import math

pg.init()

def foo(value, barrier):
    return value if value > 0 else barrier + value


class Table:
    def __init__(self, size: tuple):
        self.w, self.h = size
        self.objects = [[0 for _ in range(self.w)] for _ in range(self.h)]

    def get(self, i, j):
        try:
            if self.h >= i >= 0 and self.w >= j >= 0:
                return self.objects[int(i)][int(j)]
            raise Exception
        except:
            return -1

    def clear(self):
        self.objects = [[0 for _ in range(self.w)] for _ in range(self.h)]


class Figure:
    def __init__(self, a0: tuple, group, shape):
        self.x, self.y = a0
        self.points = copy.deepcopy(shape)
        self.group = group
        self.color = objects[group]
        self.isdead = False

    def rotate(self, w):
        for el in self.points:
            d0 = math.atan2(el[0], el[1])
            d = math.degrees(d0) + w
            el: list
            l = (el[0] ** 2 + el[1] ** 2) ** 0.5
            el[0] = round(l * math.sin(math.radians(d)), 2)
            el[1] = round(l * math.cos(math.radians(d)), 2)

    def depth(self, i, j):
        if table.get(i, j) or (i, j) in self.object:
            return
        self.object.append((i, j))
        self.depth(i + 1, j)
        self.depth(i, j + 1)
        self.depth(i - 1, j)
        self.depth(i, j - 1)

    def draw(self, screen):
        self.object = []
        for li in range(len(self.points)):
            p1, p2 = self.points[li - 1], self.points[li]
            try:
                k = (p1[0] - p2[0]) / (p1[1] - p2[1])
                for y in range(int(abs(p1[0] - p2[0])) + 1):
                    x1, x2 = y / k, (y + 1) / k
                    if min(x1, x2) < 0:
                        for x in range(int(min(x1, x2)), int(max(x1, x2)) + 1):
                            if 0 <= x + abs(int(p1[1] - p2[1])) <= abs(int(p1[1] - p2[1])) * SIZE:
                                rx = int(((x + abs(int(p1[1] - p2[1])) + min(p1[1], p2[1])) * SIZE + self.x) // SIZE)
                                ry = int(((y + min(p1[0], p2[0])) * SIZE + self.y) // SIZE)
                                if table.get(ry, rx) in (0, -2):
                                    self.object.append((ry, rx))
                                else:
                                    self.isdead = True
                    else:
                        for x in range(int(min(x1, x2)), int(max(x1, x2)) + 1):
                            if 0 <= x <= abs(int(p1[1] - p2[1])):
                                rx = int(((x + min(p1[1], p2[1])) * SIZE + self.x) // SIZE)
                                ry = int(((y + min(p1[0], p2[0])) * SIZE + self.y) // SIZE)
                                if table.get(ry, rx) in (0, -2):
                                    self.object.append((ry, rx))
                                else:
                                    self.isdead = True
            except:
                if p1[1] == p2[1]:
                    for y in range(int(abs(p1[0] - p2[0])) + 1):
                        rx = int(((min(p1[1], p2[1])) * SIZE + self.x) // SIZE)
                        ry = int(((y + min(p1[0], p2[0])) * SIZE + self.y) // SIZE)
                        if table.get(ry, rx) in (0, -2):
                            self.object.append((ry, rx))
                        else:
                            self.isdead = True
                else:
                    for x in range(int(abs(p1[1] - p2[1])) + 1):
                        rx = int(((x + min(p1[1], p2[1])) * SIZE + self.x) // SIZE)
                        ry = int(((min(p1[0], p2[0])) * SIZE + self.y) // SIZE)
                        if table.get(ry, rx) in (0, -2):
                            self.object.append((ry, rx))
                        else:
                            self.isdead = True

        self.depth(int(self.y // SIZE), int(self.x // SIZE))
        for el in self.object:
            pg.draw.rect(screen, self.color, [el[1] * SIZE, el[0] * SIZE, SIZE, SIZE])

        if self.isdead:
            self.dead()

    def dead(self):
        fall.play()
        for el in self.object:
            table.objects[int(el[0])][int(el[1])] = self.group

    def move(self, vx, vy):
        self.x, self.y = self.x + vx, self.y + vy


class Button:
    def __init__(self, a0: tuple, text):
        self.x, self.y = a0
        self.rect = pg.rect.Rect((self.x, self.y, 200, 100))

        font = pg.font.SysFont(None, 50)
        img = font.render(text, True, "white")

        self.surface = pg.Surface((200, 100))
        self.surface.fill("white")
        pg.draw.rect(self.surface, ("black"), [SIZE, SIZE, 200 - SIZE * 2, 100 - SIZE * 2])
        self.surface.blit(img, (SIZE * 6, SIZE * 4))

    def isclicked(self, x, y):
        return self.rect.collidepoint(x, y)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


SIZE_TABLE = (50, 80)
SIZE = 8
table = Table(SIZE_TABLE)
shapes = ([[-4.5, -4.5], [-4.5, 4.5], [4.5, 4.5], [4.5, -4.5]],
          [[-2.5, -7.5], [-2.5, -2.5], [-7.5, -2.5], [-7.5, 2.5], [-2.5, 2.5], [-2.5, 7.5], [2.5, 7.5], [2.5, -7.5]],
          [[-5, -5], [-5, 5], [5, 0]],
          [[-2.5, -12.5], [-2.5, -2.5], [-7.5, -2.5], [-7.5, 2.5], [2.5, 2.5], [2.5, -12.5]],
          [[0, -7.5], [0, -2.5], [-5, -2.5], [-5, 7.5], [0, 7.5], [0, 2.5], [5, 2.5], [5, -7.5]])
objects = {1: (184, 6, 0),
           2: (43, 184, 0),
           3: (0, 5, 161)}
fall = pg.mixer.Sound("sand1.mp3")
dest = pg.mixer.Sound("cloth1.mp3")
btn_restart = Button((SIZE_TABLE[0] * SIZE // 2, SIZE_TABLE[1] * SIZE // 2), "START")
btn_menu = Button((SIZE_TABLE[0] * SIZE // 2, SIZE_TABLE[1] * SIZE // 2 + 120), "MENU")
gameon = False
isdead = False

def foo(value, barrier):
    return value if value >= 0 else barrier + value


def find_connected_blocks(sand_field, x, y, visited, connected_blocks, value):
    if x < 0 or y < 0 or x >= len(sand_field) or y >= len(sand_field[0]) or visited[x][y] or sand_field[x][y] != value:
        return
    visited[x][y] = True
    connected_blocks.append((x, y))
    find_connected_blocks(sand_field, x + 1, y, visited, connected_blocks, value)  # Вправо
    find_connected_blocks(sand_field, x - 1, y, visited, connected_blocks, value)  # Влево
    find_connected_blocks(sand_field, x, y + 1, visited, connected_blocks, value)  # Вниз
    find_connected_blocks(sand_field, x, y - 1, visited, connected_blocks, value)  # Вверх


def find_sand_groups(sand_field):
    rows, cols = len(sand_field), len(sand_field[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    sand_groups = []
    for i in range(rows):
        for j in range(cols):
            if sand_field[i][j] and not visited[i][j]:
                connected_blocks = []
                find_connected_blocks(sand_field, i, j, visited, connected_blocks, sand_field[i][j])
                if connected_blocks:
                    sand_groups.append(connected_blocks)
    return sand_groups