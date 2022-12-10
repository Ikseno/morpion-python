import pygame
from random import randint

class Grille:
    """Grille 3x3 de morpion sous forme de liste de liste basée sur un système de coordonnée comme ceci :
[[00,01,02],
 [10,11,12],
 [20,21,22]]

sous la forme xy

Dans les cases, les 0 représentent des cases vides, les 1 représentent des X et les 2 des O"""

    def __init__(self):
        """Constructeur"""
        self.grille=[[0,0,0],[0,0,0],[0,0,0]]
        
    def get_case(self,x,y):
        """Récupère le contenu de la case de coordonnée xy"""
        return self.grille[x][y]

    def set_case(self,x,y,valeur):
        """vérifie que la case de coordonnée xy est vide et remplace le contenu par valeur (1 ou 2)
        renvoie True si la modification a été effectuée"""
        if self.get_case(x,y)==0:
            self.grille[x][y]=valeur
            return True
        return False
    def peut_gagner(self,joueur):
        """Vérifie si un joueur peut gagner. Le joueur est représenté par un 1 ou un 2.
        Renvoie les coordonnées de la case à choisir pour gagner (ou pour contrer une victoire)"""

        # Détecter kes bandes verticales
        for x in range(3):
            for deux_y in [0,1],[0,2],[1,2]:
                if self.get_case(x,deux_y[0])==joueur and self.get_case(x,deux_y[1])==joueur:
                    y_solution=[0,1,2]
                    y_solution.remove(deux_y[0])
                    y_solution.remove(deux_y[1])
                    if self.get_case(x,y_solution[0])==0:
                        return (x,y_solution[0])

        # Détecter les bandes horizontales
        for y in range(3):
            for deux_x in [0,1],[0,2],[1,2]:
                if self.get_case(deux_x[0],y)==joueur and self.get_case(deux_x[1],y)==joueur:
                    x_solution=[0,1,2]
                    x_solution.remove(deux_x[0])
                    x_solution.remove(deux_x[1])
                    if self.get_case(x_solution[0],y)==0:
                        return (x_solution[0],y)

        liste_case1=[]
        liste_case2=[]
        for i in range(3):
            liste_case1.append(self.get_case(i,i))
            liste_case2.append(self.get_case(i,2-i))
            
        if liste_case1==[joueur,joueur,0]:
            return(2,2)
        if liste_case1==[joueur,0,joueur]:
            return(1,1)
        if liste_case1==[0,joueur,joueur]:
            return(0,0)
        if liste_case2==[joueur,joueur,0]:
            return(2,0)
        if liste_case2==[joueur,0,joueur]:
            return(1,1)
        if liste_case2==[0,joueur,joueur]:
            return(0,2)
        return (None,None)
                
def afficher_grille(grille,surf,img_o,img_x):
    surf.fill((255,255,255))
    for posY in range(300,901,300):
        pygame.draw.line(surf,(0,0,0),(0,posY),(900,posY),2)
    for posX in range(300,901,300):
        pygame.draw.line(surf,(0,0,0),(posX,0),(posX,900),2)
    for x in range(3):
        for y in range(3):
            case=grille.get_case(x,y)
            if case==1:
                surf.blit(img_o,(300*y+10,300*x+10))
            elif case==2:
                surf.blit(img_x,(300*y+10,300*x+10))
    pygame.display.flip()

def partie(niveau_ia):
    img_o=pygame.transform.scale(pygame.image.load("o.png"),(280,280))
    img_x=pygame.transform.scale(pygame.image.load("x.png"),(280,280))
    surf =pygame.display.set_mode((900,900))
    surf.fill((255,255,255))
    run=True
    coup_debut=randint(0,1)
    nb_coups=coup_debut
    grille=Grille()
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    pos = pygame.mouse.get_pos()
                    y=pos[0]//300
                    x=pos[1]//300
                    if grille.set_case(x,y,nb_coups%2+1):
                        nb_coups+=1
        if niveau_ia>=1 and nb_coups%2==0 and nb_coups-coup_debut<9:
            tour_ia(niveau_ia, grille)
            nb_coups+=1
        
        afficher_grille(grille,surf, img_o,img_x)
    pygame.quit()

def tour_ia(niveau_ia, grille):
    if niveau_ia==1:
        while True:
            x=randint(0,2)
            y=randint(0,2)
            if grille.get_case(x,y)==0:
                grille.set_case(x,y,1)
                return
    if niveau_ia==2:
        x,y=grille.peut_gagner(1)
        if x!=None:
            grille.set_case(x,y,1)
        else:
            x,y=grille.peut_gagner(2)
            if x!=None:
                grille.set_case(x,y,1)
            else:
                tour_ia(1,grille)
        return

partie(2)
