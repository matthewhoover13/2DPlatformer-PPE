from pygame import Vector2
from level import Level
from physics_objects import Circle, Polygon, Wall

BOUNCE_COLOR = [255,150,0]
BOUNCE_FRICTION = 0
COIN_COLOR = [255,255,0]
COIN_RADIUS = 8
GROUND_COLOR = [255,255,255]
GROUND_FRICTION = 0.9
ICE_COLOR = [0,255,255]
ICE_FRICTION = 0.3
OBSTACLE_COLOR = [255,0,0]
OBSTACLE_FRICTION = 0
WALL_COLOR = [255,255,255]
WALL_FRICTION = 1

class LevelTwo(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_up_level()
        self.local_to_global_space()
    
    def set_up_level(self):
        self.background_color = [100,100,255]
        walls = []
        # ceiling
        walls.append(Polygon(pos=[0,0], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[0,-5],[5000,-5],[5000,5],[0,5]]))
        # right wall
        walls.append(Polygon(pos=[5000,250], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-250],[5,-250],[5,250],[-5,250]]))
        # left wall
        walls.append(Polygon(pos=[0,250], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-250],[5,-250],[5,250],[-5,250]]))
        
        # floors
        floors = []
        floors.append(Polygon(pos=[0,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[500,-5],[500,5],[0,5]]))
        floors.append(Polygon(pos=[500,500], color=ICE_COLOR, friction=ICE_FRICTION, offsets=[[0,-5],[1000,-5],[1000,5],[0,5]]))
        floors.append(Polygon(pos=[1500,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[500,-5],[500,5],[0,5]]))
        floors.append(Polygon(pos=[2000,500], color=ICE_COLOR, friction=ICE_FRICTION, offsets=[[0,-5],[700,-5],[700,5],[0,5]]))
        floors.append(Polygon(pos=[2700,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[300,-5],[300,5],[0,5]]))
        floors.append(Polygon(pos=[3000,500], color=ICE_COLOR, friction=ICE_FRICTION, offsets=[[0,-5],[1100,-5],[1100,5],[0,5]]))
        floors.append(Polygon(pos=[4100,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[900,-5],[900,5],[0,5]]))

        # obstacles
        obstacles = []
        obstacles.append(Polygon(pos=[500,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[800,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[1200,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-80],[5,-80],[5,0]]))
        obstacles.append(Polygon(pos=[1500,400], color=GROUND_COLOR, friction=GROUND_FRICTION, avel=2, offsets=[[-100,-5],[100,-5],[100,5],[-100,5]]))
        obstacles.append(Polygon(pos=[2000,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[2200,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-80],[5,-80],[5,0]]))
        obstacles.append(Polygon(pos=[2500,400], color=GROUND_COLOR, friction=GROUND_FRICTION, avel=-2, offsets=[[-100,-5],[100,-5],[100,5],[-100,5]]))
        obstacles.append(Polygon(pos=[2700,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-80],[5,-80],[5,0]]))
        obstacles.append(Polygon(pos=[3100,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[3300,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-100],[5,-100],[5,0]]))
        obstacles.append(Polygon(pos=[3700,400], color=GROUND_COLOR, friction=GROUND_FRICTION, avel=-2, offsets=[[-100,-5],[100,-5],[100,5],[-100,5]]))
        obstacles.append(Polygon(pos=[3900,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-80],[5,-80],[5,0]]))
        obstacles.append(Polygon(pos=[4100,494], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-100],[5,-100],[5,0]]))
        obstacles.append(Polygon(pos=[4600,400], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=-1, offsets=[[-100,-5],[100,-5],[100,5],[-100,5]]))

        # platforms
        platforms = []
        platforms.append(Polygon(pos=[3500,400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[4400,400], color=ICE_COLOR, friction=ICE_FRICTION, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))

        # add all objects to the main objects list
        self.objects = []
        for wall in walls:
            self.objects.append(wall)
        for floor in floors:
            self.objects.append(floor)
        for obstacle in obstacles:
            self.objects.append(obstacle)
        for platform in platforms:
            self.objects.append(platform)
        
        # coins
        self.coins = []
        self.coins.append(Circle(pos=[1500,350], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[2500,465], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[3550,465], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[4450,365], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))

        # set spawn, checkpoint, and finish positions
        self.checkpoints = []
        self.spawn_pos = Vector2(50,465)
        self.checkpoints.append([50,465])
        self.checkpoints.append([1700,465])
        self.checkpoints.append([2850,465])
        self.finish_pos = Vector2(4950,465)
    