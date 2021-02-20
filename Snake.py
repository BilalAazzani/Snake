# -*- coding: utf-8 -*-

import random
import datetime


class Menu :
    """Class nous permettant de gérer le menu """
    def __init__(self) :

        self.size = 10

        self.name = input(" Enter your name : ")

        print(" Welcome " + self.name + " to the snake game : ")

        self.init_menu()

    
        


    def change_size(self, level):
        """Fonction qui change la taille du board en fonction
        de la difficulté choisi par l'utilisateur """
        if ( level == 1 ) :
                return 5
            
        elif ( level == 2 ) :
                return 10
            
        else :
            return 15




    def start_game(self, name, size) :

        p = Player(name,size)
        g = Game(p,size)
        g.play()

        




    def handle_menu(self, text) :
        """ Gestion des choix de l'utilisateur """ 

        choose = ""
        
        while choose not in [1,2,3] :
            
    
            try :
            
                choose = int(input(text))

                if ( choose not in [1,2,3] ) :
                    print("number not recognize")

            except ValueError: #dans le cas ou il tape autre chose qu'un INT 

                print("you have to choose between 1 , 2 and 3")


        return choose




    def high_score(self) :

        try :

            with open("save_pts.txt", "r") as file :

                list_score = file.readlines()[::-1] #Lis le fichier sous forme de liste et l'inverse


                print("#####  HIGH SCORE !  #####")
                for elem in range (len(list_score[:3])): #On affiche que les 3 meilleurs score
                    
                    elem_split = list_score[elem].split(":")
                    
                    print(str(elem+1) + ") " + elem_split[0] + " with a score of : " + elem_split[1].rstrip() + "\n" )


                
        except FileNotFoundError : #Cas où le fichier contenant les high score n'existe pas encore

            print("you did not played any game yet")



        

                





    def init_menu(self) : 
        """Initilisation du Menu"""
        print(" 1. Choose the difficulty")
        print(" 2. Start the game")
        print(" 3. High Score")

        
        choose = self.handle_menu("Choose action : ")

            
        

        if ( choose == 1 ) :


          choose = self.handle_menu("choose level difficulty (1. low , 2. medium, 3. hard) : ")

          self.start_game(self.name,self.change_size(choose))
            
            

        elif ( choose == 2 ) :

            self.start_game(self.name,self.size)
            


        else :

            self.high_score()
            self.init_menu()
        

        











class Player :
    """Class nous permettant de gérer le Joueur ainsi que ses attributs 
    (name / point/position..) """
    keyboard_key = {'z':(-1,0),
                    'q':(0,-1),
                    's':(1,0),
                    'd':(0,1)}
    
    def __init__(self, name,size, points = 0, start = (0,0)):
        self.name = name
        self.points = points
        self.position = start
        self.size = size
    
    def move (self) :
        
        key = input("Mouvement (z,q,s,d) : ")
        while key not in Player.keyboard_key.keys() :
            key = input("Mouvement (z,q,s,d) : ")
        
        move = Player.keyboard_key[key]

        self.calcul_move(move)


    def calcul_move(self, move) :
        """Fonction nous permettant d'avoir les bonnes coordonées.
        On part du principe que le joueur peut passer à traver les murs """
        if ( self.position[0] == 0) and ( move == (-1,0) )  :

            self.position = (self.position[0] + self.size-1, self.position[1])


        elif ( self.position[1] == 0) and ( move == (0,-1) ) :

            self.position = (self.position[0] , self.position[1] + self.size-1)



        elif ( self.position[1] == self.size-1) and ( move == (0,1) )  :

            self.position = (self.position[0] , 0)



        elif ( self.position[0] == self.size-1) and ( move == (1,0) )  :

            self.position = ( 0 , self.position[1])



        else :

            self.position = (self.position[0] + move[0], self.position[1] + move[1])
            

            

            

        
        

        
        
    

class Game :
    
    def __init__(self, player, size):
        self.player = player
        self.board_size = size
        self.candies = []
        
    # Dessine le plateau
    def draw(self):

        print("score : " + str(self.player.points))
        
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies :
                    print("b",end=" ")
                elif (line,col) == self.player.position :
                    print("P",end=" ")

                    
                else : 
                    print(".",end=" ")
            print()
            
    # Fait apparaitre un bonbon
    def pop_candy(self):
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_candy not in self.candies :
            self.candies.append(new_candy)
            
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies:
            self.player.points += 2
            self.candies.remove(self.player.position)
    
        
        
    # Joue une partie complète
    def play(self):
        print("--- Début de la partie ---")
        self.draw()
        
        end = Game.end_time(0,1)
        now = datetime.datetime.today()
        
        while now < end :
            self.player.move()
            self.check_candy()
            
            if random.randint(1,3) == 1 :
                self.pop_candy()
                
            self.draw()
            
            now = datetime.datetime.today()
        
        
        print("----- Terminé -----")
        print("Vous avez", self.player.points, "points" )
        
        

        self.save_score()


    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end



    def save_score(self) :

        try :

            file = open("save_pts.txt","r")
            lines = file.readlines()
   

            file.close()

            index = self.find_pos(lines)


            if index == len(lines) : 

                print("Congatrulations you have the high score :D")


            lines.insert(index,self.player.name + ":" + str(self.player.points) + "\n")

           

            


            self.write_in_file(lines)
            
            

        except FileNotFoundError : #Cas où le fichier n'existe pas

            file = open("save_pts.txt","w")

            file.write(self.player.name + ":" + str(self.player.points) + "\n")

            file.close()




    def find_pos(self, lines) :
        """Fonction nous permettant de savoir à quel index on doit 
        rajouter le nouveau score du joueur."""

        for i in range (len(lines)):

            if (int(lines[i].split(":")[1]) > self.player.points) :

                return i
            

        return  (len(lines))





    def write_in_file(self, lines) :

        file = open("save_pts.txt","w")

        for line in lines :

            file.write(line.rstrip()+"\n")


        file.close()

            

                

                
                
            
            


        
        



if __name__ == "__main__" :

    Menu() 
   

    
    
    
