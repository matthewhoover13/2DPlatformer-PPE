from pygame import Vector2
from level import Level
from physics_objects import Circle, Polygon, Wall

BOUNCE_COLOR = [255,150,0]
BOUNCE_FRICTION = 0
COIN_COLOR = [255,255,0]
COIN_RADIUS = 8
GROUND_COLOR = [50,50,50]
GROUND_FRICTION = 0.9
ICE_COLOR = [0,255,255]
ICE_FRICTION = 0.3
OBSTACLE_COLOR = [255,0,0]
OBSTACLE_FRICTION = 0
WALL_COLOR = [50,50,50]
WALL_FRICTION = 1

class LevelFour(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_up_level()
        self.local_to_global_space()
    
    def set_up_level(self):
        self.background_color = [120,50,50]
        walls = []
        # ceiling
        walls.append(Polygon(pos=[0,0], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[0,-5],[5000,-5],[5000,5],[0,5]]))
        # right wall
        walls.append(Polygon(pos=[5000,250], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-250],[5,-250],[5,250],[-5,250]]))
        # left wall
        walls.append(Polygon(pos=[0,250], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-250],[5,-250],[5,250],[-5,250]]))
        
        # floors
        floors = []
        floors.append(Polygon(pos=[0,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[2400,-5],[2400,5],[0,5]]))
        floors.append(Polygon(pos=[2400,500], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[0,-5],[200,-5],[200,5],[0,5]]))
        floors.append(Polygon(pos=[2600,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[650,-5],[650,5],[0,5]]))
        floors.append(Polygon(pos=[3250,500], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[0,-5],[150,-5],[150,5],[0,5]]))
        floors.append(Polygon(pos=[3400,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[400,-5],[400,5],[0,5]]))
        floors.append(Polygon(pos=[3800,500], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[0,-5],[1100,-5],[1100,5],[0,5]]))
        floors.append(Polygon(pos=[4900,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[100,-5],[100,5],[0,5]]))

        # obstacles
        obstacles = []
        obstacles.append(Polygon(pos=[506,435], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,59],[-5,-59],[5,-59],[5,59]]))
        obstacles.append(Polygon(pos=[930,370], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=-1, offsets=[[-130,5],[-130,-5],[130,-5],[130,5]]))
        obstacles.append(Polygon(pos=[1400,400], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=-3, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))
        obstacles.append(Polygon(pos=[1800,450], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=3, offsets=[[-50,5],[-50,-5],[50,-5],[50,5]]))
        obstacles.append(Polygon(pos=[2000,400], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=2.5, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))
        obstacles.append(Polygon(pos=[2200,350], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=2, offsets=[[-150,5],[-150,-5],[150,-5],[150,5]]))
        obstacles.append(Polygon(pos=[2800,400], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=-2, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))
        obstacles.append(Polygon(pos=[3500,400], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=-2, offsets=[[-100,5],[-100,-5],[100,-5],[100,5]]))
        obstacles.append(Polygon(pos=[4550,400], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=-2, offsets=[[-40,5],[-40,-5],[40,-5],[40,5]]))

        # platforms
        platforms = []
        platforms.append(Polygon(pos=[500,370], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[300,-5],[300,5]]))
        platforms.append(Polygon(pos=[1200,400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[1800,400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[600,-5],[600,5]]))
        platforms.append(Polygon(pos=[2000,300], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[400,-5],[400,5]]))
        platforms.append(Polygon(pos=[2200,200], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[200,-5],[200,5]]))
        platforms.append(Polygon(pos=[2600,400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[3900,400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[4150,400], color=GROUND_COLOR, friction=GROUND_FRICTION, avel=0.5, offsets=[[-50,5],[-50,-5],[50,-5],[50,5]]))
        platforms.append(Polygon(pos=[4400,400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[4600,400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))

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
        self.coins.append(Circle(pos=[550,465], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[600,465], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[650,465], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[1400,465], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[2650,365], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))

        # set spawn, checkpoint, and finish positions
        self.checkpoints = []
        self.spawn_pos = Vector2(50,465)
        self.checkpoints.append([50,465])
        self.checkpoints.append([1600,465])
        self.checkpoints.append([3000,465])
        self.finish_pos = Vector2(4950,465)
    