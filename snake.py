import pygame
import threading
import random
import tkinter as tk

class snakegame():
    
    # infinite loop - gets input right,left and update the screen per ( 0.2 second = 200ms ) gameplay
    def run(self):
        self.create_game()
        while self.running:
            pygame.time.delay(200)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # pencereyi kapata basarsa error verme programi kapat
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.goRight()
                    if event.key == pygame.K_LEFT:
                        self.goLeft()


            self.checkCollision()   # if its out of bounds check the cordinates func.                        
                
            if not self.gameOver:
                
                self.update_position()  # change the cordinates and clear the previous image
                
                if self.isFoodGone():     
                    self.increase_score()
                    self.generate_food()
                
                pygame.draw.rect(self.win, (255, 0, 0), (self.cordinate_X, self.cordinate_Y, self.width, self.height))
                pygame.draw.rect(self.win, (0, 255, 0), (self.food_X, self.food_Y, self.width, self.height))
                pygame.display.update()
                print("SCORE :", self.score)
                print("check RIGHT:", self.isRightEmpty(), "check LEFT:", self.isLeftEmpty(), "check MOVE:", self.isMoveOk())
                print("Which side Food :", self.whichSideFood())
                self.movement += 1
            else:
                self.finishGame()
        
        
    def create_game(self):
        print("code is in the game")
        pygame.init()
        self.win = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Snake Game")   
        # create the object size or position here
        self.cordinate_X = 180
        self.cordinate_Y = 180
        self.width = 30
        self.height = 30
        self.score = 0
        self.direction = 2  #  I set it 3 = right for deafult move.    1=up , 2=right , 3=down , 0=left      
        # bool value for game contuinue = true or false change later
        self.running = True   # bool for while loop in the run function
        self.move = 30
        self.gameOver = False
        self.food_X = random.randint(0,19) * 30
        self.food_Y = random.randint(0,19) * 30
        
        self.label = tk.Label(None, text= "", font=('Times', '18'),fg='blue')
        self.label.pack()

        
    def __init__(self):
        print("code is in the INIT")
        
        
    def main(self):
        print("code is in the MAIN")
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()       
        
    
    # generate new food position
    def generate_food(self):
        temp_food_x = random.randint(0,19) * 30
        temp_food_y = random.randint(0,19) * 30
        # above lines for when food is behind the snake then AI confusing so this lines temporary fix
        if temp_food_x == self.cordinate_X:
            while temp_food_x == self.cordinate_X:
                temp_food_x = random.randint(0,19) * 30
        if temp_food_y == self.cordinate_Y:
            while temp_food_y == self.cordinate_Y:
                temp_food_y = random.randint(0,19) * 30
        self.food_X = temp_food_x
        self.food_Y = temp_food_y
    
    # add score when snake eat the food
    def increase_score(self):
        self.score += 1
    
    # check the food is eaten or not
    def isFoodGone(self):
        if self.food_X == self.cordinate_X and self.food_Y == self.cordinate_Y:
            return True
        return False
    
    # snake direction=1 (up) , direction=2 (right) , ...etc
    def change_direction(self, dr):
        if dr == 2:
            self.direction = (self.direction + 1)%4     # it goes like 1, 2, 3, 0, 1, 2, 3, 0, .. always turn right
        if dr == 0:
            self.direction = (self.direction - 1)%4     # it goes like 2, 1, 0, 3, 2, 1, 0, 3, .. always turn left
    
    # this function constantly change the position of snake head for movement
    def update_position(self):
        self.win.fill((0, 0, 0))    # clear the previous position display
        
        if self.direction == 1:     # move to up
            self.cordinate_Y -= self.move
            print("/// up ///")
            
        if self.direction == 2:     # move to right
            self.cordinate_X += self.move
            print("/// right ///")
            
        if self.direction == 3:     # move to down
            self.cordinate_Y += self.move
            print("/// down ///")
            
        if self.direction == 0:     # move to left
            self.cordinate_X -= self.move
            print("/// left ///")
            
        scor = str(self.score)
        b = "Score : "
        kelime = b + scor
        self.label.config(text= kelime)
        self.label.update()
            
            
    def startGame(self):
        self.resetValues()
        self.gameOver = False
    
    def finishGame(self):
        # self.running = False
        print("******** GAME OVER *******")

    # reset game values like positions, score,         
    def resetValues(self):
        # change the moving side if u like
        self.score = 0
        self.direction = random.randint(0,3)
        self.cordinate_X = random.randint(2,17) * 30
        self.cordinate_Y = random.randint(2,17) * 30
        
        
    
            
    # if snake is out of the bounds gameOver
    def checkCollision(self):
        if (self.cordinate_X > 570) or (self.cordinate_X < 0):
            self.gameOver = True
        if (self.cordinate_Y > 570) or (self.cordinate_Y < 0):
            self.gameOver = True
    
    def stop(self):
        self.running = False
    
    def get_Score(self):      
        return self.score
    
    # number of each move like increase şn every 0.4 ms
    def set_movement(self):
        self.movement = 0
        
    def get_movement(self):
        return self.movement
    
    
    
    # ************************************
    # ************************************
    
    def goLeft(self):
        self.change_direction(0)
        print("sol")
        
    def goRight(self):
        self.change_direction(2)
        print("sag")
        
    # is snake have bounds on the left side
    def isLeftEmpty(self):
        if self.direction == 1 and self.cordinate_X == 0:
            return 1
        elif self.direction == 2 and self.cordinate_Y == 0:
            return 1
        elif self.direction == 3 and self.cordinate_X == 570:
            return 1
        elif self.direction == 0 and self.cordinate_Y == 570:
            return 1
        return 0
    
    # is snake have bounds on the right side
    def isRightEmpty(self):
        if self.direction == 1 and self.cordinate_X == 570:
            return 1
        elif self.direction == 2 and self.cordinate_Y == 570:
            return 1
        elif self.direction == 3 and self.cordinate_X == 0:
            return 1
        elif self.direction == 0 and self.cordinate_Y == 0:
            return 1
        return 0
    
    # is snake have bounds on the front side
    def isMoveOk(self):
        if self.direction == 1 and self.cordinate_Y == 0:
            return 1
        elif self.direction == 2 and self.cordinate_X == 570:
            return 1
        elif self.direction == 3 and self.cordinate_Y == 570:
            return 1
        elif self.direction == 0 and self.cordinate_X == 0:
            return 1
        return 0
            
    
    # this method gives you a distance number to food for check the snake is going to close food or not
    def distanceToFood(self):
        vertical = abs(self.food_X - self.cordinate_X)
        horizantal = abs(self.food_Y - self.cordinate_Y)
        return horizantal+vertical
    
    
    # which side is food at ( left or right )
    def whichSideFood(self):
        if self.direction == 1:
            if self.cordinate_X > self.food_X:
                return 1
            elif self.cordinate_X == self.food_X:
                return 0
            
        if self.direction == 2:
            if self.cordinate_Y >self.food_Y:
                return 1
            elif self.cordinate_Y == self.food_Y:
                return 0
            
        if self.direction == 3:
            if self.cordinate_X <self.food_X:
                return 1
            elif self.cordinate_X == self.food_X:
                return 0
            
        if self.direction == 0:
            if self.cordinate_Y<self.food_Y:
                return 1
            elif self.cordinate_Y == self.food_Y:
                return 0
        return -1
        
    # ************************************
    # ************************************
    
pygame.quit()