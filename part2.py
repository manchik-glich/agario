from pygame import *
from random import randint
from math import hypot
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

sock = socket(AF_INET,SOCK_STREAM)
sock.connect(("localhost",8080))
sock.setblocking(False)



init()

WINDOW_SIZE = 800,600
FPS = 60

running = True
lose = False

screen = display.set_mode(WINDOW_SIZE)
display.set_caption("AGAR.IO")

clk = time.Clock()

class Player:
    def __init__(self,x,y,r,name,color=(255,0,0)):
        self.x = x
        self.y = y
        self.r = r
        self.name = name
        self.color = color

    def move(self): 
        keys = key.get_pressed()
        if keys[K_w]:
            self.y -= 5
        if keys[K_s]:
            self.y += 5
        if keys[K_a]:
            self.x -= 5
        if keys[K_d]:
            self.x += 5
    
    def draw(self,scale): 
        draw.circle(screen, self.color, (400,300), self.r*scale)


class Food:
    def __init__(self):
        self.x = randint(-2000,2000)
        self.y = randint(-2000,2000) 
        self.r = 10
        self.color = (randint(10,255),randint(10,255),randint(10,255))

    def check_collision(self,player):
        dx = self.x - player.x
        dy = self.y - player.y
        return hypot(dx,dy) < self.r + player.r
    
    def draw(self, sx, sy):
        draw.circle(screen, self.color, (sx,sy), self.r)


my_data = list(map(int, sock.recv(64).decode().strip().split(",")))
my_id = my_data[0]
my_Player = Player(my_data[1], my_data[2], my_data[3], "Player")

all_players = []
foods = [Food() for _ in range(300)]


def recieve_data():
    global all_players, running, lose
    while running:
        try:
            data = sock.recv(4096).decode().strip()
            if data == "LOSE":
                lose = True
            elif data:
                parts = data.strip('|').split('|')
                all_players = [list(map(int, p.split(","))) for p in parts if len(p.split(',')) == 4]
        except:
            pass

Thread(target=recieve_data, daemon=True).start()

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    screen.fill((255,255,255))

    scale = max(0.1, min(50, my_Player.r / 80))
    my_Player.move()
    my_Player.draw(scale)

    for p in all_players:
        if p[0] == my_id: continue
        sx= int((p[1] - my_Player.x) * scale + WINDOW_SIZE[0] // 2)
        sy = int((p[2] - my_Player.y) * scale + WINDOW_SIZE[1] // 2)
        draw.circle(screen, (2,255,0),(sx,sy),int(p[3] * scale))
    to_remove = []
    for f in foods:
        if f.check_collision(my_Player):
            my_Player.r += int(f.r * 0.2)
            to_remove.append(f)
        else:
            sx = int((f.x - my_Player.x) * scale + 400)
            sy = int((f.y - my_Player.y) * scale + 300)
            f.draw(sx,sy)

    for f in to_remove: foods.remove(f)

    if lose:
        main_font = font.SysFont("Arial", 50)
        t = main_font.render("You lose", 1 (244,0,0))

    display.update()
    clk.tick(FPS)

    try:
        msg = f"{my_id}, {my_Player.x}, {my_Player.y}, {my_Player.r}"
        sock.send(msg.encode())
    except:
        pass
    