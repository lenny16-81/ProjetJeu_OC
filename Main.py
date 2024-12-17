from pickle import FALSE

import pygame
import random
from pygame.locals import *

class Voiture(pygame.sprite.Sprite):
   def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("Voiture_Rouge.png").convert_alpha()

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
       self.image = pygame.image.load(voiture_image).convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.speed = 2
   def update(self):
       self.rect.y += self.speed
       if self.rect.top > HAUTEUR:
           self.kill()

pygame.init()
LARGEUR = 600
HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()

fond = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(fond)
fond.image = pygame.image.load("Route.png").convert()
fond.rect = fond.image.get_rect()
# Coordonnées de l’image
fond.rect.x = 0
fond.rect.y = 0
positions_x = [150, 280, 405]  # Positions fixes sur l'axe x

voiture = Voiture()

liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_sprites.add(fond)
liste_des_sprites.add(voiture)
gameover = False
police = pygame.font.Font(None, 36)
texte1 = pygame.sprite.Sprite()
texte2 = pygame.sprite.Sprite()
lescore = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(texte1)
pygame.sprite.Sprite.__init__(texte2)
pygame.sprite.Sprite.__init__(lescore)

ennemis = []
score = 0
ennemi_manque = 0
nombre = random.randint(1, 100)
running = True
game = True
pygame.key.set_repeat(400, 300)
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == KEYDOWN:
           if voiture.rect.x > 150:
               if event.key == K_a:
                   voiture.bouger_gauche()
           if voiture.rect.x < 400:
               if event.key == K_d:
                   voiture.bouger_droite()
           if game == False:
               if event.key == K_r:
                   voiture.rect.x = LARGEUR/2
                   voiture.rect.y = HAUTEUR-70
                   liste_des_sprites.add(voiture)
                   liste_des_sprites.draw(fenetre)
                   ennemi_manque = 0
                   score = 0
                   game = True
   nombre_aleatoire = random.randint(0, 100)
   if game:
       liste_des_sprites.remove(texte1)
       liste_des_sprites.remove(texte2)
       if nombre_aleatoire == 0:
           position_x_aleatoire = random.choice(positions_x)  # Choisir une des 3 positions
           nouvel_ennemi = Ennemi(position_x_aleatoire, -50)
           liste_des_sprites.add(nouvel_ennemi)
           ennemis.append(nouvel_ennemi)
       lescore.image = police.render(f"Score: {score}", 1, (250, 250, 250), (0, 0, 0))
       lescore.rect = lescore.image.get_rect()
       lescore.rect.x = 10
       lescore.rect.y = 10
       liste_des_sprites.add(lescore)
   for ennemi in ennemis:
       ennemi.update()
       for ennemi in ennemis:
           if ennemi.rect.y > 850 :
               ennemis.remove(ennemi)
               ennemi.kill()
               ennemi_manque += 1
               score += 10
   for ennemi in ennemis:
       if ennemi.rect.colliderect(voiture.rect):
           ennemis.remove(ennemi)
           ennemi.kill()
           voiture.kill()
           voiture.rect.x = 8000
           voiture.rect.y = 8000
           texte1.image = police.render(f"Game Over \n Votre score: {score} \n Ennemis ésquivés: {ennemi_manque} !", 1, (10, 10, 10),(150, 150, 150))
           texte1.rect = texte1.image.get_rect()
           texte1.rect.centerx = fenetre.get_rect().centerx
           texte1.rect.centery = fenetre.get_rect().centery
           texte2.image = police.render(f"Appuyez sur R pour recommencer", 1, (10, 10, 10), (150, 150, 150))
           texte2.rect = texte2.image.get_rect()
           texte2.rect.centerx = fenetre.get_rect().centerx
           texte2.rect.centery = fenetre.get_rect().centery + 50
           liste_des_sprites.add(texte1)
           liste_des_sprites.add(texte2)
           pygame.display.flip()
           game = False
   if game == False:
       liste_des_sprites.remove(lescore)
       liste_des_sprites.remove(ennemis)
   fenetre.fill((0,0,0))
   liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(180)
pygame.quit()

