# main.py
import pygame
import math
import random
import csv


class MainClass(object):
    def __init__(self):
        super().__init__()
        # initial pygame
        pygame.init()
        self.settings()
        self.initial()
        self.GameLoop()

    def settings(self):
        print('settings')
        # ===== Screen =====
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Covid-19 Fighter')  # set Title
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        self.background = pygame.image.load('background.jpg')

        # ===== Player =====
        self.pSize = 128
        self.pImg = pygame.image.load('boy.png')
        self.px = 100  # start Point x
        self.py = self.HEIGHT-self.pSize  # start Point y
        self.pxChange = 0

        # ===== Enemy =====
        self.eSize = 64
        self.eImg = pygame.image.load('virus.png')
        self.ex = 50
        self.ey = 0
        self.eyChange = 1  # enemy speed
        self.exList = []  # x position of enemy
        self.eyList = []  # y position of enemy
        self.eyChangeList = []
        self.allEnemy = 3  # จำนวน enemy

        # ===== Apple =====
        self.aSize = 64
        self.aImg = pygame.image.load('apple.png')
        self.ax = 50
        self.ay = 0
        self.ayChange = 2  # apple speed
        self.axList = []  # x position of apple
        self.ayList = []  # y position of apple
        self.ayChangeList = []
        self.allApple = 1  # จำนวน apple
        self.aState = 'ready'

        # ===== Mask Bullet =====
        self.mSize = 32
        self.mImg = pygame.image.load('mask.png')
        self.mx = 100
        self.my = self.HEIGHT-self.pSize
        self.myChange = 20  # Mask speed
        self.mState = 'ready'

        # ===== Sound =====
        pygame.mixer.music.load('music.wav') #https://freesound.org/people/Mativve/sounds/416778/
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.backgroundSound = pygame.mixer.Sound('virus_alert.wav')
        self.overSound = pygame.mixer.Sound('over.wav') #https://freesound.org/people/dersuperanton/sounds/434465/
        self.laserSound = pygame.mixer.Sound('laser.wav') #https://freesound.org/people/bubaproducer/sounds/151022/
        self.brokenSound = pygame.mixer.Sound('broken.aiff') # https://freesound.org/people/bareform/sounds/218721/

        # ===== Font =====
        self.fontOver = pygame.font.Font('ANGSA.ttf', 120)
        self.fontOver2 = pygame.font.Font('ANGSA.ttf', 80)
        self.overText = self.fontOver.render('Game Over', True, (255, 0, 0))
        self.overText2 = self.fontOver2.render(
            'Press [N] New Game', True, (255, 255, 255))
        self.fontScore = pygame.font.Font('ANGSA.ttf', 50)
        self.fontHighScore = pygame.font.Font('ANGSA.ttf', 50)
        self.fontHealth = pygame.font.Font('ANGSA.ttf', 55)
        self.fontSpeed = pygame.font.Font('ANGSA.ttf', 55)

    def initial(self):
        print('initial')
        for i in range(self.allEnemy):
            self.exList.append(random.randint(0, self.WIDTH-self.eSize))
            self.eyList.append(random.randint(0, 100))
            # eyChangeList.append(random.randint(1, 3))  # random enemy speed
            # กำหนดความเร็วเป็น 1 ก่อน แล้วค่อยเพิ่มหลังจากยิงโดน
            self.eyChangeList.append(1)
        
        for i in range(self.allApple):
            self.axList.append(random.randint(0, self.WIDTH-self.aSize))
            self.ayList.append(random.randint(0, 100))
            self.ayChangeList.append(1)

        # ===== score =====
        self.allScore = 0
        self.highScore = self.readHighScore()

        # ===== Health =====
        self.allHealth = 3
        
        # ===== state ====='
        self.playSound = False
        self.gameOver = False
        self.running = True

        # ===== other =====
        self.backgroundSound.play()
        self.pSpeed = 10

    def Player(self, x, y):
        self.screen.blit(self.pImg, (x, y))  # วางภาพในหน้าจอ

    def Enemy(self, x, y):
        self.screen.blit(self.eImg, (x, y))
    def Apple(self, x, y):
        self.aState = 'fire'
        self.screen.blit(self.aImg, (x, y))

    def fire_mask(self, x, y):
        self.mState = 'fire'
        self.screen.blit(self.mImg, (x, y))

    def isCollision(self, ecx, ecy, mcx, mcy):  # เช็คชนกัน
        distance = math.sqrt(math.pow(ecx-mcx, 2)+math.pow(ecy-mcy, 2))
        # print(distance)
        if distance < (self.eSize/2+self.mSize/2):  # (eSize/2+mSize/2) = ระยะที่ชนกัน
            return True
        else:
            return False
    
    def isCollisionApple(self, acx, acy, pcx, pcy):  # เช็คชนกัน
        distance = math.sqrt(math.pow(acx-pcx, 2)+math.pow(acy-pcy, 2))
        # print(distance)
        if distance < (self.aSize/2+self.pSize/2):  # (eSize/2+mSize/2) = ระยะที่ชนกัน
            return True
        else:
            return False

    def showScore(self):
        score = self.fontScore.render(f'Score: {self.allScore} คะแนน', True, (255, 255, 255))
        self.screen.blit(score, (30, 30))

    def readHighScore(self):
        with open('high-score.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                highscore = int(row[0])
            return highscore

    def writeHighScore(self):
        with open('high-score.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f'{self.allScore}'])

    def showHighscore(self):
        score = self.fontHighScore.render(f'High Score: {self.highScore} คะแนน', True, (255, 255, 255))
        self.screen.blit(score, (30, 65))
    
    def showhealth(self):
        health = self.fontHealth.render(f'Health: {self.allHealth}',True, (255,255,255))
        self.screen.blit(health,(30,100))

    def showSpeed(self):
        speed = self.fontSpeed.render(f'Speed: {self.pSpeed}',True, (255,255,255))
        self.screen.blit(speed,(30,135))

    def GameOver(self):
        self.screen.blit(self.overText, (300, 300))
        self.screen.blit(self.overText2, (250, 400))
        if self.playSound == False:
            self.overSound.play()
            self.playSound = True

    def GameLoop(self):
        print('GameLoop')
        # ===== Game Loop =====
        clock = pygame.time.Clock()
        FPS = 60  # set frame per second
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pxChange = -self.pSpeed  # set speed player
                    if event.key == pygame.K_RIGHT:
                        self.pxChange = self.pSpeed  # set speed player
                        # ถ้า player ได้ apple เพิ่มความเร็ว
                    if event.key == pygame.K_SPACE:
                        if self.mState == 'ready':
                            self.laserSound.play()
                            self.mx = self.px + 50  # ขยับออกมาด้านขวา
                            self.fire_mask(self.mx, self.my)
                    if event.key == pygame.K_n and self.gameOver == True:
                        self.settings()
                        self.initial()
                        for i in range(self.allEnemy):
                            self.eyList[i] = random.randint(0, 100)
                            self.exList[i] = random.randint(
                                50, self.WIDTH-self.eSize)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.pxChange = 0

                    # print(event)

            # ===== Run player =====
            self.Player(self.px, self.py)  # start px,py
            if self.px <= 0:
                self.px = 0
                self.px = self.px + self.pxChange
            elif self.px >= self.WIDTH - self.pSize:
                self.px = self.WIDTH - self.pSize
                self.px = self.px + self.pxChange
            else:
                self.px = self.px + self.pxChange

            # ===== Run single-enemy =====
            # Enemy(ex, ey)
            # ey = ey + eyChange
            # ===== collision for single-enemy =====
            # collision = isCollision(ex, ey, mx, my)
            # if collision:
            #     my = HEIGHT - pSize
            #     mState = 'ready'
            #     ey = 0
            #     ex = random.randint(0, WIDTH-eSize)  # random new virus position
            #     allScore = allScore + 1

            # ===== Run single-apple =====
            self.Apple(self.ax, self.ay)
            self.ay = self.ay + self.ayChange
            # ===== collision for single-apple =====
            self.collision = self.isCollisionApple(self.ax, self.ay, self.px, self.py)
            if self.collision:
                self.pSpeed = self.pSpeed + 10 # เพิ่มความเร็ว 10
                self.ay = 0
                self.ax = random.randint(0, self.WIDTH-self.aSize)  # random new virus position
            # ===== Run muti-enemy =====
            for i in range(self.allEnemy):
                # increase enemy speed
                if self.eyList[i] > self.HEIGHT-self.eSize and self.allHealth > 0:
                    self.allHealth = self.allHealth -1 
                    self.eyList[i] = 0
                    self.exList[i] = random.randint(50, self.WIDTH-self.eSize)
                    print('health-1')
                elif self.allHealth == 0:
                    for i in range(self.allEnemy):
                        self.eyList[i] = 1000
                    # for i in range(self.allApple):
                    #     self.ayList[i] = 1000
                    self.ay = 1000
                    if self.allScore > self.highScore and self.gameOver == False:
                        print('write new high score')
                        self.writeHighScore()
                    print('over loop')
                    self.gameOver = True
                    self.GameOver()
                # ===== collision for multi-enemy =====
                self.eyList[i] = self.eyList[i] + self.eyChangeList[i]
                self.collisionMulti = self.isCollision(
                    self.exList[i], self.eyList[i], self.mx, self.my)
                if self.collisionMulti:
                    self.my = self.HEIGHT - self.pSize
                    self.mState = 'ready'
                    self.eyList[i] = 0
                    self.exList[i] = random.randint(50, self.WIDTH-self.eSize)
                    self.allScore = self.allScore + 1  # ตัวละกี่คะแนน
                    # ทำความเร็วเพิ่ม 1 step
                    self.eyChangeList[i] = self.eyChangeList[i] + 0.5

                    self.brokenSound.play()

                self.Enemy(self.exList[i], self.eyList[i])  # enemy respawn

            # ===== fire mask =====
            if self.mState == 'fire':
                self.fire_mask(self.mx, self.my)
                self.my = self.my-self.myChange
            if self.my <= 0:  # check mask is top, if True set to 'ready' state
                self.my = self.HEIGHT - self.pSize
                self.mState = 'ready'

            # ===== apple respawn =====
            if self.ay > self.HEIGHT and self.ay != 1000:  # check mask is top, if True set to 'ready' state
                self.ay = 0
                self.ax = random.randint(0, self.WIDTH-self.aSize)

            self.showScore()  # ปรับ score
            self.showHighscore()
            self.showhealth()
            self.showSpeed()
            # print(self.px, self.pxChange)
            pygame.display.update()
            clock.tick(FPS)
            self.screen.fill((0, 0, 0))  # clear blit image
            self.screen.blit(self.background, (0, 0))
            # pygame.display.flip()


if __name__ == "__main__":
    app = MainClass()
