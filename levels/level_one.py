from pygame import Vector2
from level import Level
from physics_objects import Circle, Polygon, Wall

BOUNCE_COLOR = [255,150,0]
BOUNCE_FRICTION = 0
COIN_COLOR = [255,255,0]
COIN_RADIUS = 8
GROUND_COLOR = [100,255,100]
GROUND_FRICTION = 0.8
ICE_COLOR = [0,255,255]
ICE_FRICTION = 0.3
OBSTACLE_COLOR = [255,0,0]
OBSTACLE_FRICTION = 0
WALL_COLOR = [100,255,100]
WALL_FRICTION = 1

class LevelOne(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_up_level()
        self.local_to_global_space()
    
    def set_up_level(self):
        self.background_color = [100,100,255]
        walls = []
        # ceiling
        walls.append(Polygon(pos=[0,0], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[0,-5],[4000,-5],[4000,5],[0,5]]))
        # right wall
        walls.append(Polygon(pos=[4000,500], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-500],[5,-500],[5,500],[-5,500]]))
        # left wall
        walls.append(Polygon(pos=[0,500], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-500],[5,-500],[5,500],[-5,500]]))
        
        # floors
        floors = []
        floors.append(Polygon(pos=[0,1000], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[4000,-5],[4000,5],[0,5]]))

        # obstacles
        obstacles = []
        obstacles.append(Polygon(pos=[400,994], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[700,994], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[1100,994], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-80],[5,-80],[5,0]]))
        obstacles.append(Polygon(pos=[1550,800], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,100],[-5,-100],[5,-100],[5,100]]))
        obstacles.append(Polygon(pos=[1700,994], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-80],[5,-80],[5,0]]))
        obstacles.append(Polygon(pos=[2000,994], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-100],[5,-100],[5,0]]))
        obstacles.append(Polygon(pos=[2400,994], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-100],[5,-100],[5,0]]))
        obstacles.append(Polygon(pos=[2850,800], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,100],[-5,-100],[5,-100],[5,100]]))
        obstacles.append(Polygon(pos=[3200,994], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-130],[5,-130],[5,0]]))

        # platforms
        platforms = []
        platforms.append(Polygon(pos=[1350,900], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[2650,900], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))

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
        self.coins.append(Circle(pos=[1400,865], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[2700,965], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))

        # set spawn, checkpoint, and finish positions
        self.checkpoints = []
        self.spawn_pos = Vector2(50,965)
        self.checkpoints.append([50,965])
        self.checkpoints.append([1600,965])
        self.finish_pos = Vector2(3800,965)
    