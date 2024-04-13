# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:31:04 2024

@author: bluet
""" 
    Coin sound: https://opengameart.org/content/plingy-coin
    Car: https://opengameart.org/content/lap-rusher-assets
    background: https://opengameart.org/content/2d-top-down-highway-background
    Coin image: https://opengameart.org/content/coin-icon
    Car Crash: https://opengameart.org/content/stop
"""
import pygame, simpleGE, random
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("background-1.png")
        self.sndCoin = simpleGE.Sound("coin.wav")
        self.sndCrash = simpleGE.Sound("Car Crash.flac")
        
        self.score = 0
        self.lblScore = LblScore()
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 20
        self.lblTime = LblTime()
        
        self.racer = Racer(self)
        self.obstacles = []
        self.coin = []
        self.sprites = [self.racer, self.obstacles, self.coin,self.lblTime, self.lblScore]
        
        for obstacle in range(3):
            self.obstacles.append(Obstacles(self))
        for coin in range(2):
            self.coin.append(Coin(self))
        
    def process(self):
        for obstacle in self.obstacles:
            if obstacle.collidesWith(self.racer):
                self.sndCrash.play()
                obstacle.reset()
                self.score -= 5
                self.lblScore.text = f"Score: {self.score}"
        for coin in self.coin:
            if coin.collidesWith(self.racer):
                self.sndCoin.play()
                coin.reset()
                self.score += 20
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"score: {self.score}")
            self.stop()
            
        if self.racer.x <= 115:
            self.racer.x = 125
        if self.racer.x >= 535:
            self.racer.x = 525
class Racer(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("TopDownCar.png")
        self.setSize(80,40)
        self.moveSpeed = 10
        self.position = (200,400)
        self.imageAngle = 90
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
class Obstacles(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("TopDownCar.png")
        self.setSize(80,40)
        self.minSpeed = 6
        self.maxSpeed = 12
        self.imageAngle = -90
        self.reset()
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
    def reset(self):
        self.y = 10
        self.x = random.randint(125,525)
        self.dy - random.randint(self.minSpeed, self.maxSpeed)
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Coin.png")
        self.setSize(40,40)
        self.minSpeed = 3
        self.maxSpeed = 6
        self.imageAngle = -90
        self.reset()
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
    def reset(self):
        self.y = 10
        self.x = random.randint(125,525)
        self.dy - random.randint(self.minSpeed, self.maxSpeed)
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 20"
        self.center = (120,100)
     
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (500,100)
        
class Instructions(simpleGE.Scene):
    def __init__(self,prevScore):
        super().__init__()
        
        self.prevScore = prevScore
        
        self.setImage("background-1.png")
        self.response = "Quit"
       
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "Your a Highway racer",
        "Use the left and right arrow key to catch",
        "coins and avoid in coming cars.",
        "Get as many points as possible"]
        
        self.directions.center = (320, 200)
        self.directions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100,400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540,400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320,400)

        self.lblScore.text = f"Last score: {self.prevScore}"
        
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
        
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
            
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        
        
def main():
   
    keepGoing = True
    lastScore = 0
    
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
            
        else:
            keepGoing = False
    
if __name__ == "__main__":
    main()
