self.eSize = 64
        self.eImg = pygame.image.load('virus.png')
        self.ex = 50
        self.ey = 0
        self.eyChange = 1  # enemy speed
        self.exList = []  # x position of enemy
        self.eyList = []  # y position of enemy
        self.eyChangeList = []
        self.allEnemy = 3  # จำนวน enemy