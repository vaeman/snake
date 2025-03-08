import pygame 
import random
import speedtest
import threading
import time

running = True
def get_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  
    return download_speed

def update_speed():
    global internet_speed
    while running: 
        internet_speed = get_speed()
        print(f"Updated Internet Speed: {internet_speed:.2f} Mbps")
        time.sleep(5)

def randPos():
    pos = random.randint(0,7)
    return pos*100

internet_speed = 10
print(f"Internet Speed: {internet_speed:.2f} Mbps")
threading.Thread(target=update_speed, daemon=True).start()

min_speed = 10   
max_speed = 100  
min_delay = 200  
max_delay = 50   

pygame.init()
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
div = 16
count = WIDTH/div
count = int(count)
xpos = WIDTH/2
ypos = HEIGHT/2
ltime = pygame.time.get_ticks()
dx, dy =0,0
randx = randPos()
randy = randPos()
prevx,prevy =0,0
slen = 1

font = pygame.font.Font(None,64)


pos = [[xpos,ypos]]

while running:
    # internet
    snake_speed = max_delay + (min_delay - max_delay) * (max_speed - min(internet_speed, max_speed)) / (max_speed - min_speed)
    snake_speed = max(min_delay, min(snake_speed, max_delay)) 


    # font
    scoreText = f"Score: {slen}"
    score = font.render(scoreText,True,"#babbf1",None)
    scoreRect = score.get_rect()

    # drawing snake
    def drawSnake():
        for x,y in pos:
            pygame.draw.rect(screen,"#e5c890",[x,y,count,count])
        
    ctime = pygame.time.get_ticks()

    # controls

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -count
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, count
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -count, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = count, 0
     
    # move snake

    for i in range(slen - 1, 0, -1):
        pos[i] = pos[i - 1].copy()
    pos[0][0] +=dx
    pos[0][1] +=dy
    ltime = ctime

    # food eaten 

    if pos[0][0] == randx and pos[0][1] == randy:
        slen+=1
        pos.append(pos[-1].copy())
        while [randx, randy] in pos: 
            randx = randPos()
            randy = randPos()  

    # border collision
    if pos[0][1] > HEIGHT -50:
        pos[0][1] = HEIGHT -50
        running = False
    elif pos[0][1] < 0:
        pos[0][1] = 0
        running = False
    elif pos[0][0] < 0:
        pos[0][0] = 0
        running = False
    elif pos[0][0] > WIDTH-50:
        pos[0][0] = WIDTH -50
        running = False
        
    # snake collision with itself
    if pos[0] in pos[2:]: 
        running = False  


    # draw area

    screen.fill("#232634")
    
    pygame.draw.rect(screen, "#e78284", [randx,randy,count, count])

    drawSnake()

    for i in range(0,WIDTH,count):
        for j in range(0,HEIGHT,count):
            pygame.draw.rect(screen, "#292c3c", [i, j, count, count],1)

    screen.blit(score,scoreRect)

    pygame.display.flip()
    clock.tick(int(internet_speed))

pygame.quit()

