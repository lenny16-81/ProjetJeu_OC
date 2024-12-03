import pygame
import random
from pygame.locals import *

pygame.init()
LARGEUR = 600
HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
class Vaisseau(pygame.sprite.Sprite):
   def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("vaisseau.png").convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.x = LARGEUR/2
       self.rect.y = HAUTEUR-70
       self.vitesse = 8
   def bouger_droite(self):
       self.rect.x += self.vitesse
   def bouger_gauche(self):
       self.rect.x -= self.vitesse
class Missile(pygame.sprite.Sprite):
   def __init__(self, x, y):
       super().__init__()
       self.image = pygame.image.load("missile.png").convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.speed = 2
   def update(self):
       self.rect.y -= self.speed
       if self.rect.bottom < 0:
           self.kill()  # Supprime le sprite quand il sort de l'écran
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
           self.kill()  # Supprime le sprite quand il sort de l'écran
missiles = []
nombre = random.randint(1, 100)
ennemis = []
pygame.key.set_repeat(40, 30)
clock = pygame.time.Clock()
vaisseau = Vaisseau()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_sprites.add(vaisseau)
score = 0
police = pygame.font.Font(None, 36)  # Taille de la police: 36, None signifie la police par défaut
texte = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(texte)
pause = False
running = True
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == KEYDOWN:
           if event.key == K_a:
               vaisseau.bouger_gauche()
           if event.key == K_d:
               vaisseau.bouger_droite()
           if event.key == K_SPACE:
               nouveau_missile = Missile(vaisseau.rect.x + 10, vaisseau.rect.y - 10)
               missiles.append(nouveau_missile)
               liste_des_sprites.add(nouveau_missile)
           for missile in missiles:
               missile.update()
           nombre_aleatoire = random.randint(0, 50)
           if nombre_aleatoire == 0 and pause == False:
               position_x_aleatoire = random.randint(0, LARGEUR - 50)
               nouvel_ennemi = Ennemi(position_x_aleatoire, -50)
               liste_des_sprites.add(nouvel_ennemi)
               ennemis.append(nouvel_ennemi)
   if pause == False:
       for ennemi in ennemis:
           ennemi.update()
       for missile in missiles:
           missile.update()
           for ennemi in ennemis:
               if ennemi.rect.colliderect(missile.rect):
                   ennemis.remove(ennemi)
                   missiles.remove(missile)
                   ennemi.kill()
                   missile.kill()
                   score += 1
   if pause == False:
       for ennemi in ennemis:
           if ennemi.rect.colliderect(vaisseau.rect):
               pause = True
               ennemis.remove(ennemi)
               ennemi.kill()
               vaisseau.kill()
               texte.image = police.render(f"GAME OVER. Votre score est de: {score}", 2, (10, 10, 10), (250, 90, 20))
               texte.rect = texte.image.get_rect()
               liste_des_sprites.add(texte)
               pygame.display.flip()
               texte.rect.y = 300
               texte.rect.x = 120
   #if pause == False:
       #for ennemi in ennemis:
        #   if ennemi.rect.y > HAUTEUR:
         #      pause = True
          #     texte.image = police.render(f"GAME OVER. Votre score est de: {score}", 2, (10, 10, 10), (250, 90, 20))
           #    texte.rect = texte.image.get_rect()
            #   liste_des_sprites.add(texte)
            #   pygame.display.flip()
             #  texte.rect.y = 300
              # texte.rect.x = 120



   fenetre.fill((0,0,0))
   liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(100)  # Limite la boucle à 60 images par seconde
pygame.quit()
