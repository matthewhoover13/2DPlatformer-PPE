from pygame import Vector2
from level import Level
from physics_objects import Circle, Polygon, Wall

GROUND_COLOR = [100,255,100]
GROUND_FRICTION = 0.8
WALL_COLOR = [100,255,100]
WALL_FRICTION = 1

class LevelSelect(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_up_level()
        self.local_to_global_space()
    
    def set_up_level(self):
        self.background_color = [100,100,255]

        walls = []
        # ceiling
        walls.append(Polygon(pos=[0,-400], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-100,-5],[900,-5],[900,5],[-100,5]]))
        # right wall
        walls.append(Polygon(pos=[900,0], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,0],[-5,-400],[5,-400],[5,0]]))
        # left wall
        walls.append(Polygon(pos=[-100,0], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,0],[-5,-400],[5,-400],[5,0]]))
        
        # floors
        floor = Polygon(pos=[0,0], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-100,-5],[900,-5],[900,5],[-100,5]])

        # add all objects to the main objects list
        self.objects = []
        for wall in walls:
            self.objects.append(wall)
        self.objects.append(floor)
        
        # set spawn, checkpoint, and finish positions
        self.spawn_pos = [0,-35]
        self.checkpoints = []
        self.checkpoints.append([0,-35])
        self.finish_pos = [0,500]
    