# import pygame
# class Coin(pygame.sprite.Sprite):
# 	def __init__(self, x, y,):
# 		pygame.sprite.Sprite.__init__(self)
# 		img = pygame.image.load('coin.png')
# 		self.image = pygame.transform.scale(img,(11,11))
# 		self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

# 	def update(self, scroll):
#         # Update the position of the Coin sprite based on the scroll
#         self.rect.x -= scroll[0]
#         self.rect.y -= scroll[1]