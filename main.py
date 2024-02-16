import pygame as pg
import random
import time
from data import *
import csv
import datetime

pg.init()
main = pg.display.set_mode((SIZE_TABLE[0] * SIZE + 200, SIZE_TABLE[1] * SIZE - 100))
screen = pg.Surface((SIZE_TABLE[0] * SIZE, SIZE_TABLE[1] * SIZE))
clock = pg.time.Clock()
score = 0
font = pg.font.SysFont(None, 50)
q = [(random.choice(list(objects.keys())), random.choice(shapes)), (random.choice(list(objects.keys())), random.choice(shapes))]
next_fig = pg.surface.Surface((100, 100))
fig = Figure((200, 100), q[0][0], q[0][1])

for i in range(len(q[1][1])):
    pg.draw.line(next_fig, objects[q[1][0]], (q[1][1][i - 1][1] * 3 + 50, q[1][1][i - 1][0] * 3 + 50), (q[1][1][i][1] * 3 + 50, q[1][1][i][0] * 3 + 50), 8)

running = True

while running:
    main.fill((92, 92, 92))
    keys = pg.key.get_pressed()
    clicked = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            clicked = True
    if gameon:
        screen.fill("black")

        for i in range(table.h - 1, -1, -1):
            for j in range(table.w):
                if table.objects[i][j] > 0:
                    ni, nj = i, j
                    if not table.get(i + 1, j):
                        ni, nj = i + 1, j
                    elif not table.get(i + 1, j - 1):
                        ni, nj = i + 1, j - 1
                    elif not table.get(i + 1, j + 1):
                        ni, nj = i + 1, j + 1
                    table.objects[i][j], table.objects[ni][nj] = table.objects[ni][nj], table.objects[i][j]
                    pg.draw.rect(screen, objects[table.objects[ni][nj]], (nj * SIZE, ni * SIZE, SIZE, SIZE))

        groups = find_sand_groups(table.objects)
        for group in groups:
            if max(group, key=lambda x: x[1])[1] == table.w - 1 and min(group, key=lambda x: x[1])[1] == 0:
                for el in group:
                    pg.draw.rect(screen, "white", (el[1] * SIZE, el[0] * SIZE, SIZE, SIZE))
                dest.play()
                while group:
                    main.fill((92, 92, 92))
                    img = font.render(str(score), True, "white")
                    main.blit(img, (20, 20))
                    for i in range(50):
                        try:
                            el = random.choice(group)
                            group.remove(el)
                            table.objects[el[0]][el[1]] = 0
                            score += 5
                            pg.draw.rect(screen, "black", (el[1] * SIZE, el[0] * SIZE, SIZE, SIZE))
                        except:
                            break
                    if not fig.isdead:
                        fig.draw(screen)
                    main.blit(screen, (200, -100))
                    pg.display.flip()
                    time.sleep(0.05)

        if not fig.isdead:
            fig.draw(screen)
            fig.move((keys[pg.K_d] - keys[pg.K_a]) * 8, 8 + (keys[pg.K_s]) * 8)
            fig.rotate((keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * 5)
        else:
            q.pop(0)
            q.append((random.choice(list(objects.keys())), random.choice(shapes)))
            fig = Figure((200, 100), q[0][0], q[0][1])
            next_fig.fill("black")
            for i in range(len(q[1][1])):
                pg.draw.line(next_fig, objects[q[1][0]], (q[1][1][i - 1][1] * 3 + 50, q[1][1][i - 1][0] * 3 + 50), (q[1][1][i][1] * 3 + 50, q[1][1][i][0] * 3 + 50), 8)

        if table.objects[100 // SIZE].count(0) != table.w:
            with open("records.csv", mode="a", newline="") as csvfile:
                writer = csv.writer(csvfile, quotechar=",", delimiter=";")
                writer.writerow([datetime.datetime.today(), score])
            gameon = False
            isdead = True

        main.blit(next_fig, (20, 100))
        main.blit(img, (20, 20))
        pg.draw.line(screen, "red", [0, 100], [table.w * SIZE, 100], 8)
        pg.draw.line(main, (77, 77, 77), [200, 0], [200, table.h * SIZE], 25)
        main.blit(screen, (200, -100))

        clock.tick(20)
    elif isdead:
        img = font.render(f"Your score is: {score}", True, "white")
        main.blit(screen, (200, -100))
        main.blit(img, (200, 200))
        pg.draw.line(main, (77, 77, 77), [200, 0], [200, table.h * SIZE], 25)
        x, y = pg.mouse.get_pos()
        btn_restart.draw(main)
        btn_menu.draw(main)
        if btn_restart.isclicked(x, y):
            if clicked:
                table.clear()
                isdead, gameon, score = False, True, 0
                img = font.render("0", True, "white")
        elif clicked and btn_menu.isclicked(x, y):
            isdead = False
    else:
        main.fill("black")
        btn_restart.draw(main)
        x, y = pg.mouse.get_pos()
        if clicked and btn_restart.isclicked(x, y):
            table.clear()
            isdead, gameon, score = False, True, 0
            img = font.render("0", True, "white")
    pg.display.flip()