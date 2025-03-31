import pygame
from random import randint
import sys
pygame.init()
window = pygame.display.set_mode((800,600)) # okienko
pygame.display.set_caption("Snake")

class Snake:
    def __init__(self):
        self.i = 0
        self.x_cord = 350
        self.y_cord = 250
        self.cords_x = []
        self.cords_y = []
        self.width = 73
        self.height = 73
        self.direction = None
        self.start = True
        self.images = {
            "up": pygame.image.load("snakeU.png"),
            "down": pygame.image.load("snakeD.png"),
            "left": pygame.image.load("snakeL.png"),
            "right": pygame.image.load("snakeH.png")
        }
        self.image1 = pygame.image.load("corp.png")
        self.start_png = pygame.image.load("start_png.png")
        self.image = self.images["right"]  # początkowy obraz węża
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.body = 0 # lista elementów węża

    def tick(self, keys):
        if keys[pygame.K_UP] and self.direction != "down":
            self.direction = "up"
            self.start = False
        if keys[pygame.K_DOWN] and self.direction != "up":
            self.direction = "down"
            self.start = False
        if keys[pygame.K_LEFT] and self.direction != "right":
            self.direction = "left"
            self.start = False
        if keys[pygame.K_RIGHT] and self.direction != "left":
            self.direction = "right"
            self.start = False
        if self.direction == "up":
            self.y_cord -= 2
            self.image = self.images["up"]
        elif self.direction == "down":
            self.y_cord += 2
            self.image = self.images["down"]
        elif self.direction == "left":
            self.x_cord -= 2
            self.image = self.images["left"]
        elif self.direction == "right":
            self.x_cord += 2
            self.image = self.images["right"]
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        
    def draw(self):
        j = 0
        while self.body>j:
            j+=1
            window.blit(self.image1,(self.cords_x[self.i-j*20],self.cords_y[self.i-j*20]))
            if self.body>1:
                if j>3:
                    if self.hitbox.colliderect(self.cords_x[self.i-j*20],self.cords_y[self.i-j*20],2,2):
                        game_over()
        window.blit(self.image, (self.x_cord, self.y_cord))     
        
    def reset(self):
        self.__init__()

class Apple:
    def __init__(self):
        self.x_cord = randint(0,760)
        self.y_cord = randint(0,580)
        self.width = 74
        self.height = 74
        self.image = pygame.image.load('apple.png')
        self.hitbox = pygame.Rect(self.x_cord,self.y_cord,self.width,self.height)
    def tick(self):
        self.hitbox = pygame.Rect(self.x_cord,self.y_cord,self.width,self.height)
    def draw(self):
        window.blit(self.image,(self.x_cord,self.y_cord))

def game_over():
    global score, clock1, apple1, timer1, text, timer
    
    skull = pygame.image.load('skull.png')
    background = pygame.image.load('back.png')
    
    # obrazki
    apple_img = pygame.image.load('apple1.png')
    timer_img = pygame.image.load('timer.png')
    font = pygame.font.SysFont("modern", 40)
    score_text = font.render(f'Punkty: {score}', True, (0, 0, 0))
    time_text = font.render(f'Czas: {round(clock1, 2):.2f}', True, (0, 0, 0))
    
    font_large = pygame.font.SysFont("arial", 60)
    game_over_text = font_large.render("Koniec gry", True, (255, 0, 0))
    options_text = font.render("R - Restart, Q - Wyjście", True, (0, 0, 0))
    
    waiting = True
    while waiting:
        window.blit(background, (0, 0))
        window.blit(skull, (350, 180))
        
        # Wyświetlanie statystyk
        window.blit(apple_img, (315, 355))
        window.blit(timer_img, (315, 392))
        window.blit(score_text, (330, 350))
        window.blit(time_text, (330, 387))
        
        # Wyświetlanie tekstów
        window.blit(game_over_text, (400 - game_over_text.get_width()//2, 260))
        window.blit(options_text, (400 - options_text.get_width()//2, 424))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restart gry
                    waiting = False
                    main()
                    return
                if event.key == pygame.K_q:  # wyjscie z gry
                    pygame.quit()
                    sys.exit()

def main():
    global clock1, text, timer, apple1, timer1, score
    
    run = True #petla trwania gry
    player = Snake()
    clock = 0
    clock1 = 0
    score = 0
    apples = []
    apples.append(Apple())
    apple1 = pygame.image.load('apple1.png')
    timer1 = pygame.image.load('timer.png')
    background = pygame.image.load('back.png')
    
    while run:
        if player.x_cord < 0 or player.x_cord + player.width > 800 or player.y_cord < 0 or player.y_cord + player.height > 600:
            game_over()
            
        clock += pygame.time.Clock().tick(200)/350
        if player.start == False:
            clock1 += pygame.time.Clock().tick(250)/300
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # wyjscie z okienka
                run = False
                
        keys = pygame.key.get_pressed()
        player.tick(keys)
        
        for apple in apples:
            apple.tick()
            
        for apple in apples:
            if player.hitbox.colliderect(apple.hitbox):
                apples.remove(apple)
                score +=1
                apples.append(Apple())
                player.body+=1
                
        text = pygame.font.Font.render(pygame.font.SysFont("modern",40),'Punkty: '+ str(score),True,(0,0,0))
        timer = pygame.font.Font.render(pygame.font.SysFont("modern",40),'Czas: '+ str(f"{round(clock1, 2):.2f}"),True,(0,0,0))       
        
        window.blit(background,(0,0)) # kolor tla
        player.draw() # wyswietlanie 'snake' na ekranie
        
        for apple in apples:
            apple.draw()
            
        window.blit(apple1,(2,3))
        window.blit(timer1,(2,31))
        window.blit(text,(17,0))
        window.blit(timer,(17,27))
        
        if player.start == True:
            window.blit(background,(0,0))
            window.blit(player.start_png,(45,100))
            
        player.cords_x.insert(player.i,player.x_cord)
        player.cords_y.insert(player.i,player.y_cord)
        player.i+=1
        pygame.display.update()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
