from pickle import FALSE

import pygame
import random
from pygame.locals import *

class Voiture(pygame.sprite.Sprite):
   def __init__(self, vie):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("Voiture_Rouge.png").convert_alpha()
       self.vie = 1
       self.rect = self.image.get_rect()
       self.rect.x = LARGEUR/4
       self.rect.y = HAUTEUR-70
       self.vitesse = 130
   def bouger_droite(self):
        self.rect.x += self.vitesse
   def bouger_gauche(self):
        self.rect.x -= self.vitesse

class Ennemi(pygame.sprite.Sprite):
   def __init__(self, x, y):
       super().__init__()
       couleurs_voitures = ["Voiture_Blanche.png", "Voiture_Orange.png", "Voiture_Bleue.png"]
       voiture_image = random.choice(couleurs_voitures)
       vitesse_ennemi = [2, 2.5, 3, 3.5, 4]
       self.image = pygame.image.load(voiture_image).convert_alpha()
       self.image = pygame.transform.flip(self.image, False, True)
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.speed = random.choice(vitesse_ennemi)
   def update(self):
       self.rect.y += self.speed
       if self.rect.top > HAUTEUR:
           self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Bouclier.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(positions_x)
        self.rect.y = y
        self.speed = 1
        self.actif = False
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HAUTEUR:
            self.kill()

class Tuyeau(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Tuyeau.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

pygame.init()
LARGEUR = 600
HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()

t1 = Tuyeau(145, 0)
t2 = Tuyeau(275, 0)
t3 = Tuyeau(400, 0)

positions_x = [145, 275, 400]  # Positions fixes sur l'axe x
fond = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(fond)
fond.image = pygame.image.load("Route.png").convert()
fond.rect = fond.image.get_rect()
# Coordonnées de l’image
fond.rect.x = 0
fond.rect.y = 0

voiture = Voiture(1)

gameover = False
bouclier = False
police = pygame.font.Font(None, 25)
police2 = pygame.font.Font(None, 30)
police3 = pygame.font.Font(None, 80)

titre = True

for event in pygame.event.get():
    if event.type == KEYDOWN:
        if event.key == K_SPACE:
            titre = False

titre1 = pygame.sprite.Sprite()
titre2 = pygame.sprite.Sprite()
titre3 = pygame.sprite.Sprite()
logo_jeu = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(titre1)
pygame.sprite.Sprite.__init__(titre2)
pygame.sprite.Sprite.__init__(titre3)
pygame.sprite.Sprite.__init__(logo_jeu)

titre1.image = police.render("Par Arnaud et Lenny ©", 1, (100, 100, 100), (0, 0, 0))
titre1.rect = titre1.image.get_rect()
titre1.rect.x = 400
titre1.rect.y = 770

titre2.image = police2.render("Appuyez sur [ESPACE] pour commencer à jouer", 1, (250, 250, 250), (0, 0, 0))
titre2.rect = titre1.image.get_rect()
titre2.rect.x = 60
titre2.rect.y = 560

titre3.image = police2.render("Utilisez les touches [A] et [D] pour vous déplacer", 1, (250, 250, 250), (0, 0, 0))
titre3.rect = titre1.image.get_rect()
titre3.rect.x = 60
titre3.rect.y = 500

logo_jeu.image = pygame.image.load("Logo.png").convert_alpha()
logo_jeu.rect = logo_jeu.image.get_rect()
logo_jeu.rect.x = 40
logo_jeu.rect.y = -20

liste_des_sprites = pygame.sprite.LayeredUpdates()
if not titre:
    liste_des_sprites.add(fond, layer=0)
    liste_des_sprites.add(voiture, layer=2)
    liste_des_sprites.add(t1, layer=3)
    liste_des_sprites.add(t2, layer=3)
    liste_des_sprites.add(t3, layer=3)
if titre:
    liste_des_sprites.add(titre1, layer=2)
    liste_des_sprites.add(titre2, layer=2)
    liste_des_sprites.add(titre3, layer=2)
    liste_des_sprites.add(logo_jeu, layer=2)


texte1 = pygame.sprite.Sprite()
texte2 = pygame.sprite.Sprite()
texte3 = pygame.sprite.Sprite()
lescore = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(texte1)
pygame.sprite.Sprite.__init__(texte2)
pygame.sprite.Sprite.__init__(texte3)
pygame.sprite.Sprite.__init__(lescore)

ennemis = []
powerups = []
score = 0
ennemi_manque = 0
nombre = random.randint(1, 100)

running = True
game = True
pygame.key.set_repeat(400, 300)
while running:
   if titre:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           if event.type == KEYDOWN:
               if event.key == K_SPACE:
                   titre = False
   if not titre:
       liste_des_sprites.remove(titre1)
       liste_des_sprites.remove(titre2)
       liste_des_sprites.remove(titre3)
       liste_des_sprites.remove(logo_jeu)
       liste_des_sprites.add(fond, layer=0)
       liste_des_sprites.add(voiture, layer=2)
       liste_des_sprites.add(t1, layer=3)
       liste_des_sprites.add(t2, layer=3)
       liste_des_sprites.add(t3, layer=3)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           if event.type == KEYDOWN:
               if voiture.rect.x > 150:
                   if event.key == K_a:
                       voiture.bouger_gauche()
                       if bouclier == True:
                           powerup.rect.x -= 130
               if voiture.rect.x < 400:
                   if event.key == K_d:
                       voiture.bouger_droite()
                       if bouclier == True:
                           powerup.rect.x += 130
               if game == False:
                   if event.key == K_r:
                       voiture.rect.x = LARGEUR/4
                       voiture.rect.y = HAUTEUR-70
                       liste_des_sprites.add(voiture)
                       ennemi_manque = 0
                       score = 0
                       voiture.vie += 1
                       game = True
       nombre_aleatoire = random.randint(0, 100)
       nombre_aleatoireII = random.randint(0,10000)
       if game:
           liste_des_sprites.remove(texte1)
           liste_des_sprites.remove(texte2)
           liste_des_sprites.remove(texte3)
           if nombre_aleatoire == 0:
               i = random.randint(0,2)  # Choisir une des 3 positions
               if i == 0:
                   autre_pos1 = positions_x[1]
                   autre_pos2 = positions_x[2]
                   pos_ok_1 = True
                   pos_ok_2 = True
                   for ennemi in ennemis:
                       if ennemi.rect.x == autre_pos1:
                           if ennemi.rect.y < 100:
                               pos_ok_1 = False
                       elif ennemi.rect.x == autre_pos2:
                           if ennemi.rect.y < 100:
                               pos_ok_2 = False

                   if not pos_ok_1 and not pos_ok_2:
                       i = random.choice([1,2])

               elif i == 1:
                   autre_pos1 = positions_x[0]
                   autre_pos2 = positions_x[2]
                   pos_ok_1 = True
                   pos_ok_2 = True
                   for ennemi in ennemis:
                       if ennemi.rect.x == autre_pos1:
                           if ennemi.rect.y < 100:
                               pos_ok_1 = False
                       elif ennemi.rect.x == autre_pos2:
                           if ennemi.rect.y < 100:
                               pos_ok_2 = False

                   if not pos_ok_1 and not pos_ok_2:
                       i = random.choice([0, 2])

               elif i == 2:
                   autre_pos1 = positions_x[0]
                   autre_pos2 = positions_x[1]
                   pos_ok_1 = True
                   pos_ok_2 = True
                   for ennemi in ennemis:
                       if ennemi.rect.x == autre_pos1:
                           if ennemi.rect.y < 100:
                               pos_ok_1 = False
                       elif ennemi.rect.x == autre_pos2:
                           if ennemi.rect.y < 100:
                               pos_ok_2 = False

                   if not pos_ok_1 and not pos_ok_2:
                       i = random.choice([0, 1])

               position_x_aleatoire = positions_x[i]

               nouvel_ennemi = Ennemi(position_x_aleatoire, -50)
               liste_des_sprites.add(nouvel_ennemi, layer=2)
               ennemis.append(nouvel_ennemi)
           if nombre_aleatoireII == 0:
               position_x_aleatoireII = random.choice(positions_x)
               nouveau_powerup = Powerup(position_x_aleatoireII, -50)
               liste_des_sprites.add(nouveau_powerup, layer=2)
               powerups.append(nouveau_powerup)

           lescore.image = police.render(f"Score: {score}", 1, (250, 250, 250), (0, 0, 0))
           lescore.rect = lescore.image.get_rect()
           lescore.rect.x = 10
           lescore.rect.y = 10
           liste_des_sprites.add(lescore)

       for powerup in powerups:
           if powerup.rect.y > 850:
               powerups.remove(powerup)
               powerup.kill()
               liste_des_sprites.remove(powerup)
       for powerup in powerups:
           if powerup.actif:
               powerup.rect.x = voiture.rect.x - 15
               powerup.rect.y = voiture.rect.y - 10
           else:
               powerup.update()

           if powerup.rect.colliderect(voiture.rect):
               powerup.actif = True
       for powerup in powerups:
           if not powerup.actif:
               continue
           for ennemi in ennemis:
               if powerup.rect.colliderect(ennemi.rect):
                   ennemis.remove(ennemi)
                   liste_des_sprites.remove(ennemi)
                   powerups.remove(powerup)
                   liste_des_sprites.remove(powerup)
                   powerup.actif = False
                   ennemi.kill()
                   powerup.kill()
                   score += 100

       for ennemi in ennemis:
           ennemi.update()
           for ennemi in ennemis:
               if ennemi.rect.y > 850 :
                   ennemis.remove(ennemi)
                   ennemi.kill()
                   ennemi_manque += 1
                   score += 10
       for ennemi in ennemis:
           if bouclier == False:
               if ennemi.rect.colliderect(voiture.rect):
                   ennemis.remove(ennemi)
                   ennemi.kill()
                   voiture.vie -= 1

       if voiture.vie == 0:
           game = False
           voiture.kill()
           voiture.rect.x = 8000
           voiture.rect.y = 8000
           texte1.image = police.render(f"\n Votre score: {score} \n Ennemis ésquivés: {ennemi_manque} ! \n", 1, (10, 10, 10), (150, 150, 150))
           texte1.rect = texte1.image.get_rect()
           texte1.rect.centerx = fenetre.get_rect().centerx
           texte1.rect.centery = fenetre.get_rect().centery
           texte2.image = police.render(f"Appuyez sur R pour recommencer", 1, (10, 10, 10), (150, 150, 150))
           texte2.rect = texte2.image.get_rect()
           texte2.rect.centerx = fenetre.get_rect().centerx
           texte2.rect.centery = fenetre.get_rect().centery + 50
           texte3.image = police3.render("GAME OVER", 1, (250, 0, 0), (150, 150, 150))
           texte3.rect = texte3.image.get_rect()
           texte3.rect.centerx = fenetre.get_rect().centerx
           texte3.rect.centery = fenetre.get_rect().centery - 100
           liste_des_sprites.add(texte1)
           liste_des_sprites.add(texte2)
           liste_des_sprites.add(texte3)
           pygame.display.flip()


       if game == False:
           liste_des_sprites.empty()
           liste_des_sprites.add(fond)
           liste_des_sprites.add(texte1)
           liste_des_sprites.add(texte2)
           liste_des_sprites.add(texte3)
           liste_des_sprites.add(t1, layer=3)
           liste_des_sprites.add(t2, layer=3)
           liste_des_sprites.add(t3, layer=3)
           powerups = []
           ennemis = []

       fenetre.fill((0,0,0))
       liste_des_sprites.draw(fenetre)
       pygame.display.flip()
       clock.tick(180)
   else:
       fenetre.fill((0,0,0))
       liste_des_sprites.draw(fenetre)
       pygame.display.flip()
       clock.tick(180)
pygame.quit()