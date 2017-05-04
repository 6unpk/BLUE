import pygame

pygame.init()

Blocks1_color = (255,255,255)
Blocks2_color = (255,81,36)
Blocks3_color = (255,177,125)


class Blocks(pygame.sprite.Sprite):
    # Speed Of Notes
    speed = 15

    Sync_time = 0

    def __init__(self, width , height, type, Sync_time_set, speed_set = 15):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])

        if(type == 1):
            color = Blocks1_color
        elif(type == 2):
            color = Blocks2_color
        elif(type == 3):
            color = Blocks3_color

        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 265
        self.speed = speed_set

    def update(self):
        self.rect.x  -= self.speed
        if(self.rect.x < 135):
                self.remove()
                self.rect.x = 1000
                self.alive()



    def get_sync_time(self):
        return self.Sync_time