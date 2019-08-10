import arcade
from neupy.layers import *
from neupy import layers
from neupy import algorithms
from neupy import storage
import numpy as np
import math
from random import randint
import os
import re
import sys

np.random.seed(42)

CODINOME = 'QT'

amostra = 1

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

SPRITE_SCALING_CONE = 0.05
SPRITE_SCALING_CAR = 0.5
SPRITE_SCALING_BAR = 1.0
SPRITE_SCALING_DOT = 1.0  

TOP_SPEED = 10#aceleracao
TOP_SPEED_TURNING = 10
MIN_SPEED = 4
SCALE = 70
SENS_SCALE = 195

CONE_TIMER = 300
SAVE_SPAN = 5

fundo_size = 150

esqYpos = 300+(fundo_size/2)-5
dirYpos = 300-(fundo_size/2)+5

nn = layers.join(
    layers.Input(4),        
    layers.Softmax(3),
)

#out-> [0]-acelerar [1]-esquerda [2]-direita
otimizador = algorithms.Momentum(nn)

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.time_elapsed = 0.0
        self.distance_map = 0.0
        self.distance_car = 0.0
        self.maxDistance = 0.0
        self.last_checkUpX = 0.0
        self.resetCount=1
        self.spdX_=0
        self.spdY_esq=0
        self.spdY_dir=0        
        self.save = SAVE_SPAN
        self.coneTimer = 0      
        self.trained=False
        self.trigger=False
        self.entrada=None        

        #self.physics_engine = None
        self.car=None    

        self.car_list = arcade.SpriteList()
        self.cone_list = arcade.SpriteList()        
        self.barreira_list = arcade.SpriteList()        

        #self.check = None
        self.sensorD = None
        self.sensorE = None        

        arcade.set_background_color(arcade.color.GRAY)
    #def on_mouse_motion(self, x, y, dx, dy):
    #    """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
    #    self.car.center_x = x
    #    self.car.center_y = y

    def setup(self):
        # Set up your game here        
        self.car_list = arcade.SpriteList()
        self.cone_list = arcade.SpriteList()        
        self.barreira_list = arcade.SpriteList()              

        self.car = arcade.Sprite("car.png", SPRITE_SCALING_CAR)
        self.car.center_x = 80 # Starting position
        self.car.center_y = 300
        self.car_list.append(self.car)
        #self.physics_engine = arcade.PhysicsEngineSimple(self.car,self.barreira_list)           
                
        fundo = arcade.Sprite("lateral.png", 1.0)
        fundo.center_x = 492
        fundo.center_y = esqYpos        
        self.barreira_list.append(fundo)

        fundo = arcade.Sprite("lateral.png", 1.0)
        fundo.center_x = 492
        fundo.center_y = dirYpos    
        self.barreira_list.append(fundo)
    
        fundo = arcade.Sprite("fundo.png", 1.0)
        fundo.center_x = 20
        fundo.center_y = 300        
        self.barreira_list.append(fundo)   

        
        self.sensorE = arcade.Sprite("ponto.png",SPRITE_SCALING_DOT)
        self.sensorE.center_x = 274
        self.sensorE.center_y = 315
        
        self.sensorD = arcade.Sprite("ponto.png",SPRITE_SCALING_DOT)
        self.sensorD.center_x = 274
        self.sensorD.center_y = 285              
        
        '''
        self.check = arcade.Sprite("cone.png",0.03) 
        self.check.center_x = 600
        self.check.center_y = 370
        '''
        

        #fundo = arcade.Sprite("fundo.png", 1.0)
        #fundo.center_x = 800
        #fundo.center_y = 300        
        #self.barreira_list.append(fundo)  
        
        #Importar rede antiga        
        for filename in os.listdir('Saves/Rede1_4-3/'):
            if filename.startswith('SavedDriver_+'+CODINOME+'_'):                
                dados = re.findall('\d+',filename)
                self.resetCount = int(dados[0])
                print(dados[1])
                self.maxDistance = float(dados[1])
                print(dados[2])
                save = "Saves/Rede1_4-3/"+filename
                storage.load(nn, filepath=save)

        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        cone = arcade.Sprite("cone.png",SPRITE_SCALING_CONE)
        cone.center_x = x
        cone.center_y = y
        self.cone_list.append(cone)   

    def reset_log(self):                
        F = open("Logs/Rede1_4-3/R1_"+str(amostra)+".txt","a")               
        F.write(str(int(self.distance_car))+"\n")
        if(self.resetCount>=120):
            #storage.save(nn, filepath=f"Saves/Rede1_4-3/motorista{amostra}_{CODINOME}_g{self.save}_d{self.maxDistance:.0f}.hdf5")
            sys.exit()
        
        

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
                    
        self.car_list.draw()
        self.barreira_list.draw()
        self.cone_list.draw()

        self.sensorD.draw()
        self.sensorE.draw()

        #self.check.draw()        
        

        #arcade.draw_text(f"Tempo decorrido: {self.time_elapsed:7.1f}",10, 580, arcade.color.WHITE, 14)
        arcade.draw_text(f"Distancia atual: {self.distance_car:7.1f}",10,560,arcade.color.WHITE,14)
        arcade.draw_text(f"Distancia Recorde: {self.maxDistance:7.1f}",10,540,arcade.color.WHITE,14)
        arcade.draw_text(f"Geração: {self.resetCount}",10,520,arcade.color.WHITE,14)
        #speedY = (self.spdY_esq-self.spdY_dir)
        #speedX = self.spdX_

        #speedY*=100
        #speedX*=100

        #if(speedY>0):
        #    arcade.draw_text(f"Velocidade Y (volante): {speedY:.2f}% (Esquerda)",10,500,arcade.color.WHITE,14)
        #else:
        #    arcade.draw_text(f"Velocidade Y (volante): {speedY:.2f}% (Direita)",10,500,arcade.color.WHITE,14)

        #arcade.draw_text(f"Velocidade X (aceleração): {speedX:.2f}%",10,480,arcade.color.WHITE,14)
        

        
    

    def update(self, delta_time):
        self.time_elapsed += delta_time
       
        
        #movimento       
        esquerda = abs(self.car.position[1]-esqYpos)
        if(esquerda>SCALE):
            esquerda=SCALE   
        #print(esquerda)     

        direita = abs(self.car.position[1]-dirYpos)
        if(direita>SCALE):
            direita=SCALE
        sensE=SENS_SCALE
        sensD=SENS_SCALE

        for cone in self.cone_list:
            if(cone.position[0]>self.car.position[0]-55):
                if(cone.position[1]>self.car.position[1]):
                    #print("cone a esquerda")   
                    sensE_ = math.sqrt((self.car.position[0]-cone.position[0])**2+(self.car.position[1]-cone.position[1])**2)
                    if(sensE_<sensE):
                        sensE=sensE_            
                else:
                    #print("cone a direita")                   
                    sensD_ = math.sqrt((self.car.position[0]-cone.position[0])**2+(self.car.position[1]-cone.position[1])**2)
                    if(sensD_<sensD):
                        sensD=sensD_


        '''
        senHit = arcade.check_for_collision_with_list(self.sensorE, self.cone_list)
        if senHit:
            for cone in senHit:            
                if(cone.position[1]>self.car.position[1]):                    
                    print("cone a esquerda")                   
                    sensE_ = math.sqrt((self.car.position[0]-cone.position[0])**2+(self.car.position[1]-cone.position[1])**2)
                    if(sensE_<sensE):
                        sensE=sensE_

        senHit = arcade.check_for_collision_with_list(self.sensorD, self.cone_list)
        if senHit:
            for cone in senHit:       
                if(cone.position[1]<self.car.position[1]): 
                    print("cone a direita")                   
                    sensD_ = math.sqrt((self.car.position[0]-cone.position[0])**2+(self.car.position[1]-cone.position[1])**2)
                    if(sensD_<sensD):
                        sensD=sensD_
        '''
        
        direita/=SCALE
        esquerda/=SCALE        
            
        self.entrada=[[esquerda,direita,sensE/SENS_SCALE,sensD/SENS_SCALE]]    

        saida = otimizador.predict(self.entrada)
        self.spdX_ = saida[0][0]
        self.spdY_esq = saida[0][1]
        self.spdY_dir = saida[0][2]
        #print("testando")
        
        speedX = TOP_SPEED*self.spdX_        

        self.car.center_x = self.car.position[0]+speedX   
        self.sensorD.center_x = self.sensorD.position[0]+speedX
        self.sensorE.center_x = self.sensorE.position[0]+speedX         

        self.distance_car+=speedX

        if(self.car.position[0]>500):
            self.car.center_x = self.car.position[0]-speedX
            self.sensorD.center_x = self.sensorD.position[0]-speedX
            self.sensorE.center_x = self.sensorE.position[0]-speedX  
            self.distance_map+speedX
            for cone in self.cone_list:
                cone.center_x = cone.position[0]-speedX
                if(cone.center_x<=20):
                    cone.kill()

        speedY = TOP_SPEED_TURNING*(self.spdY_esq-self.spdY_dir)

        self.car.center_y = self.car.position[1]+speedY
        self.sensorD.center_y = self.sensorD.position[1]+speedY
        self.sensorE.center_y = self.sensorE.position[1]+speedY

        hit = arcade.check_for_collision_with_list(self.car, self.barreira_list)
        
        #colidiu com parede/fundo
        if hit:            
            print("colidiu")
            self.reset_log()
            #learn
            y_dir = self.spdY_dir
            y_esq = self.spdY_esq
            x_ = self.spdX_
            
            for fundo in hit:
                if(fundo.center_y==esqYpos):#esquerda
                    print("esquerda")
                    y_esq = 0
                    y_dir = 1
                elif(fundo.center_y==dirYpos):#direita
                    print("direita")
                    y_esq = 1
                    y_dir = 0
                elif(fundo.center_y==300):#fundo
                    print("fundo")
                    x_ = 0.7
                    y_esq=self.spdY_esq
                    y_dir=self.spdY_dir
                    #print(f"{self.spdX_} {self.spdY_esq-self.spdY_dir}")
            if(x_<0.01):
                x_=0.7            
            #print(x_)
            y_esperado = [[x_,y_esq,y_dir]]
            
            print(f"{self.entrada} {y_esperado}")

            otimizador.train(self.entrada,y_esperado)

            #reset position
            self.resetCount+=1
            self.car.center_x = 80
            self.car.center_y = 300   
            self.sensorD.center_x = 160
            self.sensorD.center_y = 285
            self.sensorE.center_x = 160
            self.sensorE.center_y = 315
            self.distance_car=0     
            self.trained = True
            for cone in self.cone_list:
                cone.kill()
        

        hit = arcade.check_for_collision_with_list(self.car, self.cone_list)
        if hit:#colidiu com cone
            print("colidiu")
            self.reset_log()
            #learn
            y_dir = self.spdY_dir
            y_esq = self.spdY_esq
            x_ = self.spdX_
        
            for cone in hit:
                if(cone.center_y>=self.car.position[1]):#esquerda
                    print("cone - esquerda")
                    #if() #se estava no canto direito
                    y_esq = 0.0
                    y_dir = 1
                    #x_ = 0.5
                elif(cone.center_y<self.car.position[1]):#direita
                    print("cone - direita")
                    #if(esquerda<40): #se estava no canto esquerdo
                    y_esq = 1
                    y_dir = 0.0
                    #x_ = 0.5
            if(x_<0.05):
                x_=0.7
                            
            y_esperado = [[x_,y_esq,y_dir]]
            
            #print("{self.entrada} {y_esperado}")

            otimizador.train(self.entrada,y_esperado)

            #reset position
            self.resetCount+=1
            self.car.center_x = 80
            self.car.center_y = 300   
            self.distance_car=0     
            self.trained = True
            self.sensorD.center_x = 160
            self.sensorD.center_y = 285
            self.sensorE.center_x = 160
            self.sensorE.center_y = 315
            for cone in self.cone_list:
                cone.kill()
        '''
        #trigger de 1.5s
        if(self.time_elapsed>self.last):
            self.trigger=True        
            self.last+=1.5            
        '''
        #se nao treinou e ativou o trigger
        #if(self.trigger==True and self.trained==False):
        #if(self.trigger==True):            
        if(abs(self.distance_car-self.last_checkUpX)<MIN_SPEED and (sensE>=SENS_SCALE or sensD>= SENS_SCALE)):#checa se "parou"
            print("parou")
            self.reset_log()
            #learn
            x_ = 0.8
            y_esq = self.spdY_esq
            y_dir = self.spdY_dir
            y_esperado = [[x_,y_esq,y_dir]]
            
            #print("{self.entrada} {y_esperado}")
            otimizador.train(self.entrada,y_esperado)
            #reset position
            self.car.center_x = 80
            self.car.center_y = 300
            self.sensorD.center_x = 160
            self.sensorD.center_y = 285
            self.sensorE.center_x = 160
            self.sensorE.center_y = 315 
            self.resetCount+=1      
            self.distance_car=0    
            for cone in self.cone_list:
                cone.kill()                                      
        else:
            self.last_checkUpX = self.distance_car
        #self.trained = False
        #self.trigger=False
        '''
        if(self.resetCount>=self.save):                    
            storage.save(nn, filepath=f"Saves/Rede1_4-3/motorista{amostra}_{CODINOME}_g{self.save}_d{self.maxDistance:.0f}.hdf5")
            self.save+= SAVE_SPAN
        '''
        if(self.coneTimer>=CONE_TIMER and self.car.position[0]>400):
            cone = arcade.Sprite("cone.png",SPRITE_SCALING_CONE)
            cone.center_x = 900            
            cone.center_y = randint(int(self.car.position[1]-50),int(self.car.position[1]+50)) 
            if(len(self.cone_list)<5):
                self.cone_list.append(cone)  
            self.coneTimer=0
        else:
            self.coneTimer+=1


        if(self.distance_car>self.maxDistance):
            self.maxDistance = self.distance_car
        
        if(self.car.position[0]<400):
            for cone in self.cone_list:
                cone.kill()

        #self.car.center_x = x
        #self.car.center_y = y
        #self.car.center_x = self.car.position[0]+distX
        #self.car.center_y = self.car.position[1]+distY
        #self.car.change_x = 10

        #self.physics_engine.update()
        """ All the logic to move, and the game logic goes here. """
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()