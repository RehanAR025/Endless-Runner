import pygame
import random
import os
import sys

pygame.init()

#Global Constant
pygame.display.set_caption("Endless Runner")
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [
    pygame.image.load(os.path.join("Assets/Avatar", "Lari1.png")),
    pygame.image.load(os.path.join("Assets/Avatar", "Lari2.png")),
    pygame.image.load(os.path.join("Assets/Avatar", "Lari3.png")),
    pygame.image.load(os.path.join("Assets/Avatar", "Lari2.png")),]

JUMPING = pygame.image.load(os.path.join("Assets/Avatar", "Jump.png"))

DUCKING = [
    pygame.image.load(os.path.join("Assets/Avatar", "Slide1.png")),
    pygame.image.load(os.path.join("Assets/Avatar", "Slide2.png"))]

STANDING = pygame.image.load(os.path.join("Assets/Avatar", "idle.png"))

SMALL_OBSTACLE = [
    pygame.image.load(os.path.join("Assets/Obstacle", "Small1.png")),
    pygame.image.load(os.path.join("Assets/Obstacle", "Small2.png"))]

LARGE_OBSTACLE = [    
    pygame.image.load(os.path.join("Assets/Obstacle", "Large1.png")),
    pygame.image.load(os.path.join("Assets/Obstacle", "Large2.png"))]

AIR_OBSTACLE = [
    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),]

BG = [
    pygame.image.load(os.path.join("Assets/Other", "BG1.png")),
    pygame.image.load(os.path.join("Assets/Other", "BG2.png")),
    pygame.image.load(os.path.join("Assets/Other", "BG3.png"))]

GROUND = pygame.image.load(os.path.join("Assets/Other", "Ground.png"))


class Avatar:
    X_POS = 80
    Y_POS = 360
    Y_POS_DUCK = 390
    JUMP_VEL = 10

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.avatar_duck = False 
        self.avatar_run = True
        self.avatar_jump = False

        self.step_index = 0
        self.duckstep_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.avatar_rect = self.image.get_rect()
        self.avatar_rect.x = self.X_POS
        self.avatar_rect.y = self.Y_POS

    def update(self, userInput):
        if self.avatar_duck:
            self.duck()
        if self.avatar_run:
            self.run()
        if self.avatar_jump:
            self.jump()

        if self.step_index >= 12: #angkanya diedit seperlunya (note u/ post asset drawing)
            self.step_index = 0
        if self.duckstep_index >= 8:
            self.duckstep_index = 0
        
        if (userInput [pygame.K_UP] and not self.avatar_jump) or userInput [pygame.K_DOWN] and userInput [pygame.K_UP]:
            self.avatar_duck = False
            self.avatar_run = False
            self.avatar_jump = True
        elif userInput [pygame.K_DOWN] and not self.avatar_jump:
            self.avatar_duck = True
            self.avatar_run = False
            self.avatar_jump = False
        elif not (self.avatar_jump or userInput[pygame.K_DOWN]):
            self.avatar_duck = False
            self.avatar_run = True
            self.avatar_jump = False
        elif userInput [pygame.K_DOWN] and self.avatar_jump: #midair drop
            self.jump_vel -= 2

    def run(self):
        self.image = self.run_img[self.step_index // 3]
        self.avatar_rect = self.image.get_rect()
        self.avatar_rect.x = self.X_POS
        self.avatar_rect.y = self.Y_POS
        self.step_index += 1                #increment step_index

    def duck(self):
        self.image = self.duck_img[self.duckstep_index // 4]
        self.avatar_rect = self.image.get_rect()
        self.avatar_rect.x = self.X_POS
        self.avatar_rect.y = self.Y_POS_DUCK
        self.duckstep_index += 1            #increment duckstep_index
        

    def jump(self):
        self.image = self.jump_img
        if self.avatar_jump:
            self.avatar_rect.y -= self.jump_vel * 3.2
            self.jump_vel -= 1

        if self.jump_vel < -self.JUMP_VEL: #pas velocity dari JUMP_VEL nya -10(liat var global atas) dia bakal stop 
            self.avatar_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.avatar_rect.x, self.avatar_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < self.rect.width - 300:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Small_Obstacle(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 375

class Large_Obstacle(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 350

class Air_Obstacle(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 300
        self.index = 0
    
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1                #increment index

def main():
    global userInput, x_pos_bg, y_pos_bg, points, game_speed, obstacles, RUN, run
    RUN = True
    font = pygame.font.Font("freesansbold.ttf", 20)
    death_count = 0
    scroll = 0 #scroll background
    points = 0
    x_pos_bg = 0
    y_pos_bg = 10
    game_speed = 20
    obstacles = []
    bg_width = BG[0].get_width()
    clock = pygame.time.Clock()
    player = Avatar() #di video Dinosaur()   

    def Score():
        global points, game_speed, highscore_read
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render(str(points), True, (0,0,100))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

        #highscore stuff
        highscore_file = open("highscore.txt", "r+")
        highscore_read = highscore_file.readline()

        highscore = font.render(f"Highest: {str(highscore_read)}", True, (0,0,100))
        highscoreRect = highscore.get_rect()
        highscoreRect.center = (1000,60)

        highscore_file.close() 

        SCREEN.blit(highscore, highscoreRect)


    def Track():
        global x_pos_bg, y_pos_bg
        image_width = GROUND.get_width()
        SCREEN.blit(GROUND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(GROUND, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(GROUND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while RUN:
        
        clock.tick(64)

        for event in pygame.event.get(): #buat exit aman
            if event.type == pygame.QUIT:
                RUN = False
                run = False
                pygame.quit()
                quit()
                sys.exit()
        
        SCREEN.fill((251, 185, 158)) #warna background putih
        userInput = pygame.key.get_pressed()
        
        #drawing scrolling bg

        for x in range(4):
            speed = 1
            for i in BG:
                SCREEN.blit(i , ((x * bg_width + scroll * speed), 0))
                speed += 1

        #scroll background 
        scroll -= 4
        
        #reset scroll
        if abs(scroll) > bg_width:
            scroll = 0

        Track()
        
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0: #randomizer jenis obstacle
            if random.randint(0, 2) == 0:
                obstacles.append(Small_Obstacle(SMALL_OBSTACLE))
            elif random.randint(0, 2) == 1:
                obstacles.append(Large_Obstacle(LARGE_OBSTACLE))
            elif random.randint(0, 2) == 2:
                obstacles.append(Air_Obstacle(AIR_OBSTACLE))
        
        for obstacle in obstacles: #nampilkan obstacle
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.avatar_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                death_count += 1
                menu(death_count)

        Score()

        pygame.display.update()

def menu(death_count):
    global points, RUN, run
    run = True

    while run:
        SCREEN.fill((251, 185, 158))
        font = pygame.font.Font("freesansbold.ttf", 20)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0,0,0))
        elif death_count > 0:
            text = font.render("Press any key to Restart", True, (0,0,0))
            score = font.render(f"Your score: {str(points)}", True, (0,0,0))

            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_WIDTH // 2 - 250)

            SCREEN.blit(score, scoreRect)

            highscore_txt = open("highscore.txt", "r+")

            try:
                points > int(highscore_read)
            except ValueError:
                highscore_file = open("highscore.txt", "r+")
                highscore_txt.truncate(0)
                highscore_file.write(str(points))
                highscore_file.close() 
            else:
                if points > int(highscore_read):
                    highscore_txt.truncate(0)
                    highscore_txt.write(str(points))
                else:
                    pass
            highscore_txt.close()

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
        SCREEN.blit(text, textRect)

        SCREEN.blit (STANDING, (SCREEN_WIDTH // 2 -40, SCREEN_WIDTH // 2 -140))
        pygame.display.update()

        for event in pygame.event.get(): #buat exit aman
            if event.type == pygame.QUIT:
                run = False
                RUN = False
                pygame.quit()
                quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                main()

menu(death_count = 0)
