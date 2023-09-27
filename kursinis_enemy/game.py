import pygame
import sys
import math
from pygame.locals import *
from scripts.tilemap import Map 
from scripts.enemy import Enemy 
# from scripts.coin import Coin

BLACK = (0, 0, 0)



class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Pygame Platformer')

        self.WINDOW_SIZE = (640, 480)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.game_over = 0

       



        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0

        self.true_scroll = [0, 0]

        self.map = Map()
        self.map.load_map('map')

        self.grass_img = pygame.image.load('grass.png')
        self.dirt_img = pygame.image.load('dirt.png')
        self.enemy_img = pygame.image.load('enemy.png')
        self.coin_img = pygame.image.load('coin.png')

        self.player_img = pygame.image.load('player.png').convert()
        self.player_img.set_colorkey((0, 0, 0))

        self.player_rect = pygame.Rect(100, 100, 5, 13)

        self.enemies = pygame.sprite.Group()
        # self.coin_group = pygame.sprite.Group()

    

    def collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types
    


    def run(self):
        while True:  # game loop
            self.display.fill((146, 244, 255))  # clear screen by filling it with blue

            for enemy in self.enemies:
                enemy.update(self.true_scroll)
                if self.player_rect.colliderect(enemy.rect):
                # Handle collision with enemy (e.g., player loses a life, game over, etc.)
                    print(self.enemies)
                    pass
            
            
            # for coin in self.coin_group:
            #     coin.update(self.true_scroll)
            #     self.display.blit(coin.image, coin.rect.topleft)
            #     if self.player_rect.colliderect(coin.rect):
            #         self.coin_group.remove(coin)


            

            
            self.enemies.update(self.player_rect)  # Update enemy behavior
            self.enemies.draw(self.display)  # Draw the enemies on the display surface

            self.true_scroll[0] += (self.player_rect.x - self.true_scroll[0] - 152) / 20
            self.true_scroll[1] += (self.player_rect.y - self.true_scroll[1] - 106) / 20
            scroll = self.true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            tile_rects = []
            y = 0
            for layer in self.map.game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        self.display.blit(self.dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    elif tile == '2':
                        self.display.blit(self.grass_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    # elif tile == '4':
                    #     coin = Coin(x * 16, y * 16, scroll[0], scroll[1])
                    #     self.coin_group.add(coin)

                    elif tile == '3': 
                        enemy = Enemy(x * 16, y * 16, scroll[0], scroll[1])
                        self.enemies.add(enemy)

                    if tile != '0':
                        tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                        
                    x += 1
                y += 1

            player_movement = [0, 0]
            if self.moving_right:
                player_movement[0] += 2
            if self.moving_left:
                player_movement[0] -= 2
            player_movement[1] += self.vertical_momentum
            self.vertical_momentum += 0.2
            if self.vertical_momentum > 3:
                self.vertical_momentum = 3

            self.player_rect, collisions = self.move(self.player_rect, player_movement, tile_rects)

            if collisions['bottom']:
                self.air_timer = 0
                self.vertical_momentum = 0
            else:
                self.air_timer += 1

            self.display.blit(self.player_img, (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
            
                

            for event in pygame.event.get():  # event loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.moving_right = True
                    if event.key == K_LEFT:
                        self.moving_left = True
                    if event.key == K_UP:
                        if self.air_timer < 6:
                            self.vertical_momentum = -5
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        self.moving_right = False
                    if event.key == K_LEFT:
                        self.moving_left = False

            self.screen.blit(pygame.transform.scale(self.display, self.WINDOW_SIZE), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
