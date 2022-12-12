import pygame
from blur import blurSurf
from random import randint
from PIL import Image, ImageFilter
import button 

# Initialisation de pygame
pygame.init()
surf = pygame.display.set_mode((900,900))
surf.fill((255,255,255))
clock = pygame.time.Clock()
police = pygame.font.SysFont("monospace" ,100)

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

        # Détecter les bandes verticales
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
        
        # Détecter les bandes diagonales
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

    def victoire(self,joueur):
        """Vérifie si un des joueur a gagné. Si oui trace une ligne rouge sur la bande gagnante et renvoie un booléen."""
        # Bandes horizontales
        for i in range(3):
            if self.grille[i]==[joueur,joueur,joueur]:
                pygame.draw.line(surf, (250, 70, 70), (10, 150*(i+1) + 150*i), (890, 150*(i+1) + 150*i), 10)
                return True
        # Bandes verticales
        liste_bande_verticale = [[self.grille[0][a],self.grille[1][a],self.grille[2][a]] for a in range(3)]
        for i in range(3):  
            if liste_bande_verticale[i] == [joueur,joueur, joueur]:
                pygame.draw.line(surf, (250, 70, 70), (150*(i+1) + 150*i, 10), (150*(i+1) + 150*i, 890), 10)
                return True

        # Bande diagonale en partant de la gauche
        if [self.grille[0][0],self.grille[1][1],self.grille[2][2]] == [joueur,joueur, joueur]:
            pygame.draw.line(surf, (250, 70, 70), (10, 10), (890, 890), 10)
            return True
        # Bande diagonale en partant de la droite
        if [self.grille[0][2],self.grille[1][1],self.grille[2][0]] == [joueur,joueur, joueur]:
            pygame.draw.line(surf, (250, 70, 70), (890, 10), (10, 890), 10)
            return True
        return False
                
def afficher_grille(grille,surf,img_o,img_x): 
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
    run=True
    coup_debut=randint(0,1)
    nb_coups=coup_debut
    grille=Grille()
    while run:
        clock.tick(30) # 30 fps
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    pos = pygame.mouse.get_pos()
                    y=pos[0]//300
                    x=pos[1]//300
                    if grille.set_case(x,y,nb_coups%2+1):
                        afficher_grille(grille,surf, img_o,img_x)
                        if grille.victoire(nb_coups%2+1): # Ecran de victoire de l'humain si dif = 1 ou 2 / Ecran de victoire d'un des deux joueurs si dif = 0
                            surf.blit(blurSurf(surf,5),(0,0)) # Remplace la surface actuelle par une surface floutée
                            pygame.time.wait(100) # Pour éviter d'appuyer sur le bouton sans s'en rendre compte
                            while run:
                                for event in pygame.event.get():
                                    if event.type==pygame.QUIT:
                                        run=False
                                replay_img = pygame.image.load('replay.png').convert_alpha()
                                replay_button = button.Button(300, 200, replay_img, 0.2)
                                image_texte1 = police.render ("Victoire", 1 , (255,0,0))
                                image_texte2 = police.render ("du", 1 , (255,0,0))
                                image_texte3 = police.render ("joueur %s"%(str(nb_coups%2+1),), 1 , (255,0,0))
                                surf.blit(image_texte1, (210,300))  
                                surf.blit(image_texte2, (390,400))
                                surf.blit(image_texte3, (210,500))
                                pygame.display.flip()
                                
                                if replay_button.draw(surf): # Si click sur bouton replay 
                                    surf.fill((255,255,255))
                                    partie(dif) # Relance une partie
                        nb_coups+=1
            
        if niveau_ia>=1 and nb_coups%2==0 and nb_coups-coup_debut<9:
            tour_ia(niveau_ia, grille)
            if grille.victoire(1):
                afficher_grille(grille,surf, img_o,img_x)
                if grille.victoire(nb_coups%2+1): # Ecran de victoire de l'IA (quasiment le même que celui d'au dessus donc répétitif et pas très optimisé)
                    surf.blit(blurSurf(surf,5),(0,0)) # Remplace la surface actuelle par une surface floutée
                    pygame.time.wait(100) # Pour éviter d'appuyer sur le bouton sans s'en rendre compte
                    while run:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                run=False
                        replay_img = pygame.image.load('replay.png').convert_alpha()
                        replay_button = button.Button(300, 200, replay_img, 0.2)
                        image_texte1 = police.render ("Victoire", 1 , (255,0,0))
                        image_texte2 = police.render ("du", 1 , (255,0,0))
                        image_texte3 = police.render ("robot", 1, (255,0,0))
                        surf.blit(image_texte1, (210,300))
                        surf.blit(image_texte2, (390,400))
                        surf.blit(image_texte3, (300,500))
                        pygame.display.flip()
                        if replay_button.draw(surf):  # Si click sur bouton replay
                            surf.fill((255,255,255))
                            partie(dif) # Relance une partie
            nb_coups+=1
        if nb_coups-coup_debut>=9:  # Ecran de fin si aucun gagnant
            afficher_grille(grille,surf, img_o,img_x)
            surf.blit(blurSurf(surf,5),(0,0)) # Remplace la surface actuelle par une surface floutée
            pygame.time.wait(100) # Pour éviter d'appuyer sur le bouton sans s'en rendre compte
            while run:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        run=False
                replay_img = pygame.image.load('replay.png').convert_alpha()
                replay_button = button.Button(300, 200, replay_img, 0.2)
                image_texte1 = police.render ("Aucun", 1 , (255,0,0))
                image_texte2 = police.render ("gagnant", 1 , (255,0,0))
                surf.blit(image_texte1, (300,300))
                surf.blit(image_texte2, (240,400))
                pygame.display.flip()
                if replay_button.draw(surf):  # Si click sur bouton replay
                    surf.fill((255,255,255))
                    partie(dif) # Relance une partie


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
dif = 0 # Niveau de difficulté
partie(dif)

