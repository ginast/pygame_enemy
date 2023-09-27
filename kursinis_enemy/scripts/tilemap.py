import pygame
from scripts.enemy import Enemy

class Map:
    def __init__(self):
        self.tile_size = 16 

     
    def load_map(self, path):
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        self.game_map = []
        for row in data:
            self.game_map.append(list(row))

    def get_map(self):
        tiles = []
        for y, row in enumerate(self.game_map):
            for x, tile_type in enumerate(row):
                if tile_type == '1' :  # You can adjust this condition based on your tile data
                    tile_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    tiles.append(tile_rect)
                # if tile_type == '3' :  # Check for the tile type where you want to place an enemy
                #         blob = Enemy(x * 16, y * 16 + 15)  # Adjust the position as needed
                #         self.enemies.add(blob)
        return tiles
