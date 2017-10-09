import pygame
from src.skeleton import Skeleton

if __name__ == '__main__':
    def loop():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

    bones = Skeleton()
    loop()