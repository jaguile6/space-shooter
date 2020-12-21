import sys, pygame, random, math
pygame.init()

size = width, height = 1024, 768
black = 0, 0, 0
screen = pygame.display.set_mode(size)


explosion_imgs=[]
shield=100
for i in range(1,7):
    img=pygame.image.load("images/e"+str(i)+".png")
    explosion_imgs.append(img)

imagen=pygame.image.load("images/e1.png")
fuenteLetra=pygame.font.Font('freesansbold.ttf',20)




class ship:
    def __init__(self):
        self.img = pygame.image.load("images/spaceship.png")
        self.rect = self.img.get_rect()
        self.rect.x=20
        self.rect.y=400
        self.speed=[0,0]
        self.shooting=False
        self.reload=0
    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.top < 5:
            self.rect.top=5
        if self.rect.bottom > height-5:
            self.rect.bottom = height-5

class enemy:
    def __init__(self):
        self.img = pygame.image.load("images/enemy.png")
        self.rect = self.img.get_rect()
        self.rect.x=1000+random.randint(0,300)
        self.ybase=random.randint(120,660)
        self.rect.y=self.ybase
        self.speed=[-3,0]
        self.cycle=random.randint(0,300)
    def move(self):
        self.rect = self.rect.move(self.speed)
        self.cycle+=1
        self.rect.y=self.ybase+140*math.cos(-self.cycle/24)
        if self.rect.left < 5:
            global shield
            shield-=10
            enemies.remove(self)
            


    def reset(self):
        self.ybase=random.randint(60,700)
        self.rect.x=1000+random.randint(0,300)
class bullet:
    def __init__(self,inix,iniy):
        self.speed=[20,0]
        self.img = pygame.image.load("images/bullet.png")
        self.rect = self.img.get_rect()
        self.rect.x=inix
        self.rect.y=iniy
    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.x > width:
            bullets.remove(self)        
class explosion:
    def __init__(self,inix,iniy):
        self.cycle=0
        self.speed=[-1,0]
        self.frames=0
        self.img = explosion_imgs[0]
        self.rect = self.img.get_rect()
        self.rect.x=inix
        self.rect.y=iniy
    def move(self):
        self.img = explosion_imgs[self.cycle]
        self.rect = self.rect.move(self.speed)
        self.frames+=1
        if (self.frames>10):
            self.frames=0
            self.cycle+=1
            if self.cycle >= 6:
                explosions.remove(self)

ship = ship()
enemies=[]
SKILL=0
def enemy_burst():
    y=random.randint(120,660)
    for i in range(5):
        temp=enemy()
        temp.rect.x=1000+i*80
        temp.ybase=y
        temp.cycle=-i*4
        enemies.append(temp)

enemy_burst()
bullets=[]
explosions=[]



logo=pygame.image.load("images/logo.png")
logorect=logo.get_rect()
logorect=logorect.move(100,300)

iniciar=0

while (iniciar==0):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit() 
        if (event.type == pygame.KEYDOWN):
            if (event.key== pygame.K_RETURN): 
                iniciar=1
    
    screen.blit(logo, logorect)
    
    text=fuenteLetra.render('Press Enter to START',True,(255,255,255))
    pos=(300,500)
    screen.blit(text,pos)
    pygame.display.flip()
    pygame.time.delay(10)

vivo=1

while (vivo==1):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit() 
        if (event.type == pygame.KEYDOWN):
            if (event.key== pygame.K_UP): 
                ship.speed=[0,-20]
            if (event.key== pygame.K_DOWN):
                ship.speed=[0,20]
            if (event.key== pygame.K_SPACE):
                ship.shooting=True
            if (event.key== pygame.K_RIGHT):
                enemy_burst()
        if (event.type == pygame.KEYUP):
            if (event.key== pygame.K_UP or event.key== pygame.K_DOWN):
                ship.speed=[0,0]
            if (event.key== pygame.K_SPACE):
                ship.shooting=False
    if(random.randint(0,200)<1):
        enemy_burst()
    ship.move()
    for e in enemies:
        e.move()
        for b in bullets:
            if e.rect.colliderect(b):
                enemies.remove(e)
                bullets.remove(b)
                explosions.append(explosion(e.rect.x,e.rect.y))
                SKILL+=1
                
    
    for b in bullets:
        b.move()
    for ex in explosions:
        ex.move()
    if(ship.shooting):
        if(ship.reload<=0 and len(bullets)<500):
            bullets.append(bullet(ship.rect.x+55,ship.rect.y+45))
            ship.reload=4
        else:
            ship.reload-=1
    
    screen.fill(black)
    for b in bullets:
        screen.blit(b.img, b.rect)
    
    for e in enemies:
        screen.blit(e.img, e.rect)

    for ex in explosions:
        screen.blit(ex.img, ex.rect)
    if shield==0:
        vivo=0
    screen.blit(ship.img, ship.rect)
    letras=fuenteLetra.render('Punts= %s' %(SKILL),True,(255,255,255))
    posTexto=(300,25)
    screen.blit(letras,posTexto)
    letras2=fuenteLetra.render('Shield= %s' %(shield),True,(255,255,255))
    posTexto2=(100,25)
    screen.blit(letras2,posTexto2)
    pygame.display.flip()
    pygame.time.delay(10)



gameover=pygame.image.load("images/gameover.png")
gameoverrect=gameover.get_rect()
gameoverrect=gameoverrect.move(100,300)

finalizar=0

while (finalizar==0):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit() 
        if (event.type == pygame.KEYDOWN):
            if (event.key== pygame.K_RETURN): 
                finalizar=1
    screen.fill(black)
    screen.blit(gameover, gameoverrect)
    
    text=fuenteLetra.render('Press Enter to EXIT',True,(255,255,255))
    pos=(300,500)
    
    screen.blit(text,pos)
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
sys.exit()
