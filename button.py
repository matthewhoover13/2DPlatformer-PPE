from pygame import Vector2
import pygame

class Button():
    def __init__(self, text="", selected=False, active=False, pos=Vector2(0,0), width=0, height=0, \
            background_color=[0,0,0], text_color=[255,255,255], selected_color=[0,0,255]):
        self.text = text
        self.selected = selected
        self.active = active
        self.pos = pos
        self.width = width
        self.height = height
        self.background_color = background_color
        self.text_color = text_color
        self.selected_color = selected_color
    
    def draw(self, window, font):
        color = self.text_color
        if self.selected:
            color = self.selected_color
        text = font.render(self.text, True, color)
        if self.width <= 0 and self.height <= 0:
            pygame.draw.polygon(window, self.background_color, [
                [self.pos[0] - text.get_width()/2 - 10, self.pos[1] - text.get_height()/2 - 5],
                [self.pos[0] - text.get_width()/2 - 10, self.pos[1] + text.get_height()/2 + 5],
                [self.pos[0] + text.get_width()/2 + 10, self.pos[1] + text.get_height()/2 + 5],
                [self.pos[0] + text.get_width()/2 + 10, self.pos[1] - text.get_height()/2 - 5],
                ])
        else:
            pygame.draw.polygon(window, self.background_color, [
                [self.pos[0] - self.width/2, self.pos[1] - self.height/2],
                [self.pos[0] + self.width/2, self.pos[1] - self.height/2],
                [self.pos[0] + self.width/2, self.pos[1] + self.height/2],
                [self.pos[0] - self.width/2, self.pos[1] + self.height/2],
                ])
        window.blit(text, [self.pos[0] - text.get_width()/2, self.pos[1] - text.get_height()/2])
