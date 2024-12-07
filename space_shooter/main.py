#Create your own shooter
from pygame import *
from random import *
from time import time as timer
mixer.init()

width= 1000
height= 600
#Bg settings
window=display.set_mode((1000,600))
display.set_caption("The Warrior Clash")
clock= time.Clock()
#Music
mixer.music.load("space.ogg")
mixer.music.play()
fire= mixer.Sound("fire.ogg")
bg= image.load("galaxy.jpg")
score= 0
life= 5
lost= 0
max_lost=7
font.init()
font2=font.Font(None,36)
win_text=font2.render("You Win",True,[0,255,0])
lose_text=font2.render("You Lose",True,[255,0,0])

#Superclass
class Parent(sprite.Sprite):
    def __init__(self,x,y,w,h,speed,img):
        super().__init__()
        self.speed= speed 
        self.image =transform.scale(image.load(img),(w,h))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def reset(self):
        window.blit (self.image,(self.rect.x,self.rect.y))


class Player(Parent):
    def update(self):
        keys =key.get_pressed()
        if keys [K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < 950:
            self.rect.x += self.speed

        if keys [K_UP] and self.rect.y>5:
            self.rect.y -= self.speed
        if keys [K_DOWN] and self.rect.y < 525:
            self.rect.y += self.speed
    def shoot(self):
        bullet= Bullet(self.rect.centerx,self.rect.top,10,20,8,"bullet.png")
        bullets.add(bullet)

class Enemy (Parent):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 600:
            self.rect.x = randint (80,1000-80)
            self.rect.y= 0
            lost += 1

class Rock (Parent):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 600:
            self.rect.x = randint (80,1000-80)
            self.rect.y= 0
            


class Asteriod (Parent):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 600:
            self.rect.x = randint (80,1000-80)
            self.rect.y= 0
            

class Bullet (Parent):
    def update (self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill ()



            
monsters= sprite.Group()
for i in range (1,5):
    monster= Enemy(randint(80,920),-40,80,50, randint (1,2), 'ufo.png')
    monsters.add(monster)  
    

asteroids= sprite.Group()
for i in range (1,5):
    asteroid= Rock(randint(80,920),-40,80,50, randint (1,2), 'asteroid.png')
    asteroids.add(asteroid)

bullets =sprite.Group()


player=Player(500,300,40,75,10,"rocket.png")
    

reload_time= False
num_fire=0    

finish= False
run=True
while run:
    for e in event.get():
        if e.type == QUIT:
            run=False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <=10 and reload_time == False:
                    num_fire += 1 
                    player.shoot()
                    fire.play()
                if num_fire > 10 and reload_time == False:
                    start_time= timer()
                    reload_time= True

    
    if not finish:
        window.blit(bg,(0,0))
        text_missed= font2.render("Missed:"+ str(lost), 1, (255,255,255))
        window.blit(text_missed,(10,60))
        text_score=font2.render("Score:"+str(score),1,(255,255,255))
        window.blit(text_score,(10,20))
        player.reset()
        player.update()
        bullets.update()
        bullets.draw (window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)


        if reload_time:
            end= timer()
            if end - start_time<5:
                reload_text= font2.render("Sorry for the inconvience please donate 500 usd ",True,(255,255,255))
                window.blit(reload_text,(width/2-100, height - 75))
            else:
                num_fire= 0
                reload_time= False

        collision=sprite.groupcollide(bullets,monsters,True,True)
        for c in collision:
            score +=1
            monster= Enemy(randint(80,920),-40,80,50, randint (1,2), 'ufo.png')
            monsters.add(monster)

    

        if sprite.spritecollide(player,asteroids,False) or sprite.spritecollide(player,monsters,False):
            sprite.spritecollide(player,asteroids,True)
            sprite.spritecollide(player,monsters,True)
            life -=1

        if life == 0 or lost > max_lost:
            finish=True
            window.blit(lose_text,(500,300))
            
        
        if score >= 6:
            finish=True
            window.blit(win_text,(500,300))

        life_text=font2.render("Life:"+ str(life),1,(255,255,255)) 
        window.blit (life_text,(1000-150,50))  

        display.update()

    else:
        finish = False
        score= 0
        lost= 0
        num_fire=0
        life= 5
        for m in monsters: 
            m.kill()
        for b in bullets:
            b.kill()
        for a in asteroids:
            a.kill()
        for i in range (1,5):
            monster= Enemy(randint(80,920),-40,80,50, randint (1,2), 'ufo.png')
            monsters.add(monster)  
        for i in range (1,5):
            asteroid= Rock(randint(80,920),-40,80,50, randint (1,2), 'asteroid.png')
            asteroids.add(asteroid)



        

        time.delay(3000)

    
    clock.tick(60)













