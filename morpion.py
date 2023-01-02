import pygame
from blur import blurSurf
from random import randint
from PIL import Image, ImageFilter
from time import sleep
import button 

# Initialisation de pygame
pygame.init()
surf = pygame.display.set_mode((750,750))
surf.fill((255,255,255))
clock = pygame.time.Clock()

# définition de la police
police = pygame.font.SysFont("monospace" ,100)
police2 = pygame.font.SysFont("monospace" ,30)
police3 = pygame.font.SysFont("monospace" , 50)


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
    
    def ligne_gagnante(self,joueur,numero_ligne):
        """Vérifie si la ligne 'numero_ligne' est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return self.grille[numero_ligne]==[joueur,joueur,joueur]

    def colonne_gagnante(self,joueur,numero_colonne):
        """Vérifie si la colonne 'numero_colonne' est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return [self.grille[j][numero_colonne] for j in range(3)]==[joueur,joueur,joueur]

    def diagonale_bas_droite_gagnante(self, joueur):
        """Vérifie si la diagonale \ est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return [self.grille[j][j] for j in range(3)]==[joueur,joueur,joueur]

    def diagonale_haut_droite_gagnante(self, joueur):
        """Vérifie si la diagonale / est gagnante pour le joueur 'joueur' et renvoie True si oui (non sinon)"""
        return [self.grille[2-j][j] for j in range(3)]==[joueur,joueur,joueur]
        
    def victoire(self,joueur,x,y,surf):
        """Vérifie si le joueur 'joueur' a gagné à partir de ce qu'il vient de jouer (coordonnées x, y).
        Si oui trace une ligne rouge sur la bande gagnante et renvoie un booléen."""
        
        # Bandes horizontales
        if self.ligne_gagnante(joueur,x):
            pygame.draw.line(surf, (250, 70, 70), (10, 125*(x+1) + 125*x), (740, 125*(x+1) + 125*x), 10)
            return True
            
        # Bandes verticales  
        if self.colonne_gagnante(joueur,y):
            pygame.draw.line(surf, (250, 70, 70), (125*(y+1) + 125*y, 10), (125*(y+1) + 125*y, 740), 10)
            return True

        # Bande diagonale en partant de la gauche
        if self.diagonale_bas_droite_gagnante(joueur):
            pygame.draw.line(surf, (250, 70, 70), (10, 10), (740, 740), width=10)
            return True
        
        # Bande diagonale en partant de la droite
        if self.diagonale_haut_droite_gagnante(joueur):
            pygame.draw.line(surf, (250, 70, 70), (740, 10), (10, 740), width=10)
            return True

        return False
    
    def peut_gagner(self,joueur):
        """Vérifie si un joueur peut gagner. Le joueur est représenté par un 1 ou un 2.
        Renvoie les coordonnées de la case à choisir pour gagner (ou pour contrer une victoire)"""

        for x in range(3):
            for y in range(3):
                if self.get_case(x,y)==0:
                    copie_self=Grille()
                    for a in range(3):
                        for b in range(3):
                            copie_self.set_case(a,b,self.get_case(a,b))
                    if copie_self.set_case(x,y,joueur):
                        if (copie_self.ligne_gagnante(joueur,x) or
                            copie_self.colonne_gagnante(joueur,y) or
                            copie_self.diagonale_bas_droite_gagnante(joueur) or
                            copie_self.diagonale_haut_droite_gagnante(joueur)):

                            return (x,y)
        return (None,None)
                        
                
def afficher_grille(grille,surf,img_o,img_x): 
    for posY in range(250,751,250):
        pygame.draw.line(surf,(0,0,0),(0,posY),(750,posY),2)
    for posX in range(250,751,250):
        pygame.draw.line(surf,(0,0,0),(posX,0),(posX,750),2)
    for x in range(3):
        for y in range(3):
            case=grille.get_case(x,y)
            if case==1:
                surf.blit(img_o,(250*y+10,250*x+10))
            elif case==2:
                surf.blit(img_x,(250*y+10,250*x+10))
    pygame.display.flip()

def partie(dif):
    pygame.display.set_caption("Partie") 
    img_o=pygame.transform.scale(pygame.image.load("./images/o.png"),(230,230))
    img_x=pygame.transform.scale(pygame.image.load("./images/x.png"),(230,230))
    run=True
    joueur_debut=randint(0,1)
    nb_coups=0
    grille=Grille()
    while run:
        afficher_grille(grille,surf, img_o,img_x)
        clock.tick(30) # 30 fps
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    pos = pygame.mouse.get_pos()
                    y=pos[0]//250
                    x=pos[1]//250
                    if grille.set_case(x,y,(nb_coups+joueur_debut)%2+1):
                        afficher_grille(grille,surf, img_o,img_x)
                        if grille.victoire((nb_coups+joueur_debut)%2+1,x,y,surf): # Ecran de victoire de l'humain si dif = 1 ou 2 / Ecran de victoire d'un des deux joueurs si dif = 0
                            pygame.display.flip()
                            sleep(0.4)
                            run=message_victoire("joueur %s"%(str((nb_coups+joueur_debut)%2+1),),grille,dif,surf,img_o,img_x)

                        nb_coups+=1
        
        if run and dif>=1 and nb_coups%2==joueur_debut and nb_coups<9:
            coord=tour_ia(dif, grille, nb_coups)
            afficher_grille(grille,surf, img_o,img_x)
            if grille.victoire(1,coord[0],coord[1],surf):
                run = message_victoire("Robot",grille,dif,surf,img_o,img_x)
                    
            nb_coups+=1
        if run and nb_coups>=9:  # Ecran de fin si aucun gagnant
            run = message_victoire("Personne",grille,dif,surf,img_o,img_x)
    pygame.quit()

def tour_ia(dif, grille, tour):
    if dif==1:
        while True:
            x=randint(0,2)
            y=randint(0,2)
            if grille.get_case(x,y)==0:
                grille.set_case(x,y,1)
                return (x,y)
    if dif==2:
        x,y=grille.peut_gagner(1)
        if x!=None:
            grille.set_case(x,y,1)
        else:
            x,y=grille.peut_gagner(2)
            if x!=None:
                grille.set_case(x,y,1)
            else:
                return tour_ia(1,grille,tour)
        return (x,y)
    
    if dif==3:
        x,y=grille.peut_gagner(1)
        if x!=None:
            grille.set_case(x,y,1)
        else:
            x,y=grille.peut_gagner(2)
            if x!=None:
                grille.set_case(x,y,1)
            else:
                return tour_ia_3(grille, tour)
        return (x,y)

def tour_ia_3(grille, tour):
    if tour==0:
        grille.set_case(0,0,1)
        return (0,0)
    elif tour==2:
        if grille.get_case(1,1)==2:
            grille.set_case(2,2,1)
            return (2,2)
        elif grille.get_case(2,0)==0 and grille.get_case(1,0)==0:
            grille.set_case(2,0,1)
            return (2,0)
        else:
            grille.set_case(0,2,1)
            return (0,2)
    elif tour==4:
        if grille.get_case(2,0)==1:
            if grille.get_case(0,1)==2 or grille.get_case(0,2)==2:
                grille.set_case(2,2,1)
                return (2,2)
            else:
                grille.set_case(0,2,1)
                return (0,2)
        else:
            if grille.get_case(1,0)==2 or grille.get_case(2,0)==2:
                grille.set_case(2,2,1)
                return (2,2)
            else:
                grille.set_case(2,0,1)
                return (2,0)
    elif tour==1:
        if grille.get_case(0,0)==2 or grille.get_case(2,0)==2 or grille.get_case(0,2)==2 or grille.get_case(2,2)==2:
            grille.set_case(1,1,1)
            return(1,1)
        else:
            grille.set_case(0,0,1)
            return(0,0)
    return tour_ia(1,grille,tour)
            

def message_victoire(gagnant,grille,dif,surf,img_o,img_x):
    sleep(.2)  # Pour éviter d'appuyer sur le bouton sans s'en rendre compte
    rect = pygame.Rect(130,0,490,750)
    sub = surf.subsurface(rect)
    surf.blit(blurSurf(sub,5),(130,0)) # Remplace la surface actuelle par une surface floutée
    pygame.draw.line(surf, (36, 36, 36), (130, 0), (130, 750))
    pygame.draw.line(surf, (36, 36, 36), (620, 0), (620, 750))
    run=True
    while run:
        if run:
            replay_img = pygame.image.load("./images/New_game_Button.png").convert_alpha()
            replay_button = button.Button(258, 400, replay_img, 0.4)
            menu_img = pygame.image.load("./images/Menu_Button.png").convert_alpha()
            menu_button = button.Button(258, 500, menu_img, 0.4)
            if gagnant=="Personne":
                image_texte1 = police.render ("Aucun", 1 , (222, 109, 44))
                image_texte2 = police.render ("gagnant", 1 , (222, 109, 44))
                surf.blit(image_texte1, (225,125))
                surf.blit(image_texte2, (170,208))

            else:
                image_texte1 = police.render ("Victoire", 1 , (42, 201, 71))
                image_texte2 = police.render ("du", 1 , (42, 201, 71))
                image_texte3 = police.render (gagnant, 1, (42, 201, 71))
                surf.blit(image_texte1, (135,100))
                surf.blit(image_texte2, (325,183))
                if gagnant=="Robot":
                    surf.blit(image_texte3, (225,266))
                else:
                    surf.blit(image_texte3, (135,266)) 
            pygame.display.flip()

            
            
            if replay_button.draw(surf):  # Un appui sur le bouton replay (affiché à l'écran) relance une partie
                surf.fill((255,255,255))
                partie(dif) # Relance une partie
            
            
            
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Un appui sur la touche "Entrée" relance une partie
                        surf.fill((255,255,255))
                        partie(dif)
                if event.type==pygame.QUIT:
                    run = False
                    exit()
            
            if menu_button.draw(surf):
                run = False
                sleep(0.2)
                menu.main_menu()
                
                

    return run 
class Menu():
    def __init__(self, niveau=0):
        self.niveau = niveau
    def main_menu(self):  
        pygame.display.set_caption("Main Menu") 
        run = True
        # load text
        titre_txt = police.render ("Morpion", 1 , (0))
        # load button images
        play_img = pygame.image.load("./images/Play_Button.png").convert_alpha()
        options_img = pygame.image.load("./images/Options_Button.png").convert_alpha()
        credits_img = pygame.image.load("./images/bouton_credits.png").convert_alpha()
        # creation des boutons
        play_button = button.Button(258, 275, play_img, 0.4)
        options_button = button.Button(258, 400, options_img, 0.4)
        credits_button = button.Button(258, 525, credits_img, 0.4)
        while run:
            surf.fill((112, 112, 112))
            surf.blit(titre_txt, (165,80))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run = False
                    exit()
            if play_button.draw(surf):  # Un appui sur le bouton replay (affiché à l'écran) relance une partie
                surf.fill((255,255,255))
                partie(self.niveau) 
            if options_button.draw(surf):
                run = False
                menu.options()
            if credits_button.draw(surf):
                run = False
                menu.credits()
            pygame.display.flip()
    def options(self):
        pygame.display.set_caption("Options") 
        run = True
        # load text
        titre_txt = police.render ("Difficulté", 1 , (0))
        joueur_txt = police2.render ("joueur", 1 , (0))
        contre_txt = police2.render ("VS", 1 , (250,0,0)) 
        ia_txt = police2.render ("IA", 1 , (0))
        simple_txt = police2.render ("simple", 1 , (50, 168, 82))
        moyenne_txt = police2.render ("moyenne", 1 , (232, 155, 23))
        difficile_txt = police2.render ("difficile", 1 , (250,0,0))
        # load button images
        dif0g_img = pygame.image.load("./images/dif0(grey).png").convert_alpha()
        dif1g_img = pygame.image.load("./images/dif1(grey).png").convert_alpha()
        dif2g_img = pygame.image.load("./images/dif2(grey).png").convert_alpha()
        dif3g_img = pygame.image.load("./images/dif3(grey).png").convert_alpha()
        actif_img = pygame.image.load("./images/dif_actif.png").convert_alpha()
        back_img = pygame.image.load("./images/Back_Button.png").convert_alpha()
        # creation des boutons
        dif0_button = button.Button(100, 200, dif0g_img, 0.4)
        dif1_button = button.Button(260, 200, dif1g_img, 0.4)
        dif2_button = button.Button(420, 200, dif2g_img, 0.4)
        dif3_button = button.Button(580, 200, dif3g_img, 0.4)
        back_button = button.Button(258, 600, back_img, 0.4)
        # liste des boutons
        l_button = [(dif0_button,0),(dif1_button,1),(dif2_button,2),(dif3_button,3)]
        while run:
            surf.fill((112, 112, 112))
            # affiche le texte
            surf.blit(titre_txt, (75,50))
            surf.blit(joueur_txt, (85,300)) # 0
            surf.blit(joueur_txt, (245,300)) # 1
            surf.blit(joueur_txt, (405,300)) # 2
            surf.blit(joueur_txt, (570,300)) # 3
            surf.blit(contre_txt, (115,330)) # 0
            surf.blit(contre_txt, (275,330)) # 1
            surf.blit(contre_txt, (435,330)) # 2
            surf.blit(contre_txt, (600,330)) # 3
            surf.blit(joueur_txt, (85,360)) # 0
            surf.blit(ia_txt, (275,360)) # 1
            surf.blit(ia_txt, (435,360)) # 2
            surf.blit(ia_txt, (600,360)) # 3
            surf.blit(simple_txt, (245,390)) # 1
            surf.blit(moyenne_txt, (395,390)) # 2
            surf.blit(difficile_txt, (545,390)) # 3

            if self.niveau == 0:
                l = list(l_button)
                l.pop(0) # retire le bouton actif de la liste des boutons
                for element in l: # affiche les 3 autres boutons et gère le click
                    if element[0].draw(surf):
                        self.niveau = element[1]
                actif_button= button.Button(100, 200, actif_img, 0.4) 
                actif_button.draw(surf) # affiche bouton actif
            
            if self.niveau == 1:
                l = list(l_button)
                l.pop(1) # retire le bouton actif de la liste des boutons
                for element in l: # affiche les 3 autres boutons et gère le click
                    if element[0].draw(surf):
                        self.niveau = element[1]
                actif_button= button.Button(260, 200, actif_img, 0.4)
                actif_button.draw(surf) # affiche bouton actif

            if self.niveau == 2:
                l = list(l_button)
                l.pop(2) # retire le bouton actif de la liste des boutons
                for element in l: # affiche les 3 autres boutons et gère le click
                    if element[0].draw(surf):
                        self.niveau = element[1]
                actif_button= button.Button(420, 200, actif_img, 0.4)
                actif_button.draw(surf) # affiche bouton actif
        
            if self.niveau == 3: 
                l = list(l_button)
                l.pop(3) # retire le bouton actif de la liste des boutons
                for element in l: # affiche les 3 autres boutons et gère le click
                    if element[0].draw(surf):
                        self.niveau = element[1]
                actif_button= button.Button(580, 200, actif_img, 0.4)
                actif_button.draw(surf) # affiche bouton actif
            
            if back_button.draw(surf):
                run = False
                menu.main_menu()
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run = False
                    exit()   
            pygame.display.flip()
    
    def credits(self):
        pygame.display.set_caption("Crédits")
        run = True
        # load button img
        back_img = pygame.image.load("./images/Back_Button.png").convert_alpha()
        # création du bouton
        back_button = button.Button(258, 600, back_img, 0.4)
        # load text
        titre_txt = police.render ("Crédits", 1 , (0))
        realise_txt = police3.render("Réalisé par :", 1, (0))
        raphael_txt  = police3.render("Raphaël FISCHER", 1, (50, 168, 82))
        dorian_txt  = police3.render("Dorian COURCELLE", 1, (50, 168, 82))
        while run:
            surf.fill((112, 112, 112))
            surf.blit(titre_txt, (165,80))
            surf.blit(realise_txt, (180,220))
            surf.blit(raphael_txt, (150,290))
            surf.blit(dorian_txt, (140,360))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run = False
                    exit()
            if back_button.draw(surf):
                run = False
                menu.main_menu()
            
            pygame.display.flip()
menu = Menu() # Niveau de difficulté
menu.main_menu()
