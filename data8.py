import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
import snake
import random


class NN():
    
    # create X input and Y output
    def __init__(self):
        print("NN - Init function")
        self.X = [[0,0,0,0,0]]
        self.Y = [[0]]
        self.gameNumber = 0
        self.sn = snake.snakegame()
        self.prev_movement = 0
        self.sayac = 0
        
        self.build_model()
        
        self.last_left = 0
        self.last_front = 0
        self.last_right = 0
        self.last_food = 0
        self.last_suggested = 0
        self.prev_food_dis = 0
        self.last_scored = 0


    # create model
    def build_model(self):
        print("NN - build_model function")
        network = input_data(shape=[None, 5], name='input')
        network = fully_connected(network, 25, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=0.0001, loss='mean_square', name='target')    # u can change the lr rate for speeding the things up
        self.model = tflearn.DNN(network)
    
    
    # start game and count the played gameNumber
    def startGame(self):
        print("NN - startGame")
        if self.gameNumber == 0:
            self.sn.main()
            self.sn.set_movement()
            self.gameUpdate()
        else:
            self.sn.startGame()
            self.sn.set_movement()
            self.gameUpdate()
        self.gameNumber += 1
        
    # guess the direction with model prediction
    def PredictDirection(self, guessDirection):
        self.X=[[self.sn.isLeftEmpty(), self.sn.isMoveOk(), self.sn.isRightEmpty(), self.sn.whichSideFood(), guessDirection]]
        
        guess_result = self.model.predict(self.X)
        
        if guess_result > 0.8:
            print(" 0.5 ten buyukse :", guess_result)
            return 1
        elif guess_result < 0.8 and guess_result > -0.5:
            print(" 0.5 ten kucuk -0.1 den buyuk :", guess_result)
            return 0
        elif guess_result < -0.5:
            print(" -0.1 den kucukse :", guess_result)
            return -1
        
        
    # first data needs to be snake direciton or can be random but then others gonna be model predictions
    def SuggestDirection(self):
        self.sayac += 1
        
        # if its gonna 
        if self.sayac == 1:
            i = random.randint(0,2)-1
            print("random git :", i)
            return i
        
        l = self.PredictDirection(-1)
        f = self.PredictDirection(0)
        r = self.PredictDirection(1)
        
        total = 0
        if l==1:
            total +=3
        if f==1:
            total +=4
        if r==1:
            total +=5
        
        if total == 7:
            print("sol veya duz git")
            i = random.randint(0,1)-1
            print("random git :", i)
            return i
        
        if total == 8:
            print("sol veya sag git")
            i = random.randint(0,1)-1
            if i==0:    # go right
                i=1
            print("random git :", i)
            return i
        
        if total == 9:
            print("duz veya sag git")
            i = random.randint(0,1)
            return i
        
        if total == 3:
            print("sola git")
            return -1
        
        if total == 4:
            print("duz git")
            return 0
        
        if total == 5:
            print("sag git")
            return 1
        
            
        # its couldnt predict to correct directiopn then do random
        number = random.randint(0,2)-1
        print("couldnt! trying random:",number)
        return number
            
        
            
        
    
    # when snake.py done with the moving
    # update for game changes
    def gameUpdate(self):
        while True:
            if self.sn.get_movement() != self.prev_movement:
                self.sn.checkCollision()
                print("New Movement :", self.sn.get_movement()," - ",self.sn.gameOver)
                self.prev_movement = self.sn.get_movement()
                print("***********************************")
                print("***********************************")
                
                if self.prev_movement > 1:
                    self.X = [[self.last_left, self.last_front, self.last_right, self.last_food, self.last_suggested]]                
                    if self.sn.gameOver == False: # if snake was alive since the last move
                        print("+-+-+-+-+- Distance food +-+-+-+-+")
                        print("+-+-+- prev:",self.prev_food_dis, "- Now:", self.sn.distanceToFood())
                        if self.prev_food_dis > self.sn.distanceToFood() or self.last_scored < self.sn.get_Score():   # if snake alive but it went far from the food (wrong direction = 0)
                            self.Y=[[1]]     # if snake alive and getting closer to food
                        else:
                            self.Y=[[0]]   
                    else:   # if snake died
                        self.Y=[[-1]]                   
                    print("++++++++++++++++++++++++++++")
                    print("++++++ Print X and Y +++++++")
                    print("X :",self.X)
                    print("Y :",self.Y)                
                    self.model.fit(self.X,self.Y)     # feed the model
                    
                       
                self.last_scored = self.sn.get_Score()
                self.prev_food_dis = self.sn.distanceToFood()
                self.last_left = self.sn.isLeftEmpty()
                self.last_front = self.sn.isMoveOk()
                self.last_right = self.sn.isRightEmpty()
                self.last_food = self.sn.whichSideFood()
                snakeGoTo = self.SuggestDirection()
                self.last_suggested = snakeGoTo
                
                
                # change the snake direction in the game ( press key left or right job)
                if snakeGoTo == 1:
                    self.sn.goRight()
                elif snakeGoTo == -1:
                    self.sn.goLeft()
                
                
            if self.prev_movement > 0:
                if self.sn.gameOver == True:
                    print("--- GAME STARTING AGAIN ---")
                    # reset game count number at this and snake
                    self.prev_movement = 0
                    self.sn.set_movement() #  = 0
                    self.sn.startGame()



        
        

        