from pickle import FALSE

import pygame
import random
from pygame.locals import *

class Voiture(pygame.sprite.Sprite):
   def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("Voiture_Rouge.png").convert_alpha()

       self.rect = self.image.get_rect()
       self.rect.x = LARGEUR/2
       self.rect.y = HAUTEUR-70
       self.vitesse = 20
   def bouger_droite(self):
        self.rect.x += self.vitesse
   def bouger_gauche(self):
        self.rect.x -= self.vitesse

class Ennemi(pygame.sprite.Sprite):
   def __init__(self, x, y):
       super().__init__()
       self.image = pygame.image.load("ennemi1.png").convert_alpha()
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
voiture = Voiture()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_sprites.add(fond)
liste_des_sprites.add(voiture)
gameover = False
police = pygame.font.Font(None, 36)
texte = pygame.sprite.Sprite()
lescore = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(texte)
pygame.sprite.Sprite.__init__(lescore)

ennemis = []
score = 0
ennemi_manque = 0
nombre = random.randint(1, 100)
running = True
game = True
pygame.key.set_repeat(40, 30)
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == KEYDOWN:
           if event.key == K_a:
               voiture.bouger_gauche()
           if event.key == K_d:
               voiture.bouger_droite()
   nombre_aleatoire = random.randint(0, 100)
   if game:
       if nombre_aleatoire == 0:
           position_x_aleatoire = random.randint(0, LARGEUR - 50)
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
   for ennemi in ennemis:
       if ennemi.rect.colliderect(voiture.rect):
           ennemis.remove(ennemi)
           ennemi.kill()
           voiture.kill()
           voiture.rect.x = 8000
           voiture.rect.y = 8000
           texte.image = police.render(f"Game Over \n Votre score: {score} \n Ennemis ésquivés: {ennemi_manque} !", 1, (10, 10, 10),(150, 150, 150))
           texte.rect = texte.image.get_rect()
           texte.rect.centerx = fenetre.get_rect().centerx
           texte.rect.centery = fenetre.get_rect().centery
           liste_des_sprites.add(texte)
           pygame.display.flip()
           game = False
   if game == False:
       liste_des_sprites.remove(lescore)
   fenetre.fill((0,0,0))
   liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(180)
pygame.quit()

