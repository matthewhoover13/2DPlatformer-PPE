from pygame import Vector2

from physics_objects import Wall

class Level():
    def __init__(self, pos=Vector2(0,0), objects_list=[], coins=[], spawn_pos=Vector2(0,0), finish_pos=Vector2(0,0), checkpoints=[], background_color=[255,255,255], enabled=True):
        self.pos = pos
        self.objects = objects_list
        self.coins = coins
        self.local_to_global_space()
        self.spawn_pos = spawn_pos
        self.finish_pos = finish_pos
        self.checkpoints = checkpoints
        self.background_color = background_color
        self.enabled = enabled

    def clear_force(self):
        for obj in self.objects:
            obj.clear_force()

    def draw(self, window):
        if self.enabled:
            for obj in self.objects:
                obj.draw(window)

    def local_to_global_space(self):
        for obj in self.objects:
            if isinstance(obj, Wall):
                obj.point1 += self.pos
                obj.point2 += self.pos
            else:
                obj.pos += self.pos
        for coin in self.coins:
            coin.pos += self.pos
    
    def update(self, dt):
        if self.enabled:
            for obj in self.objects:
                obj.update(dt)
