from pygame import Vector2
from level import Level
from physics_objects import Circle, Polygon, Wall

BOUNCE_COLOR = [255,150,0]
BOUNCE_FRICTION = 0
COIN_COLOR = [255,255,0]
COIN_RADIUS = 8
GROUND_COLOR = [200,200,200]
GROUND_FRICTION = 0.7
ICE_COLOR = [0,255,255]
ICE_FRICTION = 0.3
OBSTACLE_COLOR = [255,0,0]
OBSTACLE_FRICTION = 0
WALL_COLOR = [200,200,200]
WALL_FRICTION = 1

class LevelThree(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_up_level()
        self.local_to_global_space()
    
    def set_up_level(self):
        self.background_color = [100,100,255]
        walls = []
        # ceiling
        walls.append(Polygon(pos=[0,0], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[0,-5],[1000,-5],[1000,5],[0,5]]))
        # right wall
        walls.append(Polygon(pos=[1000,1500], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-1500],[5,-1500],[5,1500],[-5,1500]]))
        # left wall
        walls.append(Polygon(pos=[0,1500], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-1500],[5,-1500],[5,1500],[-5,1500]]))
        
        # floors
        floors = []
        floors.append(Polygon(pos=[500,3000], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=800, offsets=[[-500,-5],[-400,-5],[-400,5],[-500,5]]))
        floors.append(Polygon(pos=[500,3000], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-400,-5],[500,-5],[500,5],[-400,5]]))
        floors.append(Polygon(pos=[500,2800], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-380,-5],[300,-5],[300,5],[-380,5]]))
        floors.append(Polygon(pos=[500,2550], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-350,-5],[500,-5],[500,5],[-350,5]]))
        floors.append(Polygon(pos=[500,1700], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-300,-5],[500,-5],[500,5],[-300,5]]))

        # obstacles
        obstacles = []
        obstacles.append(Polygon(pos=[300,2994], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[700,2794], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[400,2794], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-60],[5,-60],[5,0]]))
        obstacles.append(Polygon(pos=[500,1300], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, avel=-0.4, offsets=[[-350,5],[-350,-5],[350,-5],[350,5]]))

        # platforms
        platforms = []
        platforms.append(Polygon(pos=[1000,2900], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-100,5],[-100,-5],[0,-5],[0,5]]))
        platforms.append(Polygon(pos=[0,2665], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[200,-5],[200,5]]))
        platforms.append(Polygon(pos=[500,2450], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[700,2400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[400,2300], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[925,2275], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[200,2200], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[500,2150], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=800, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[800,2050], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[200,1900], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[0,1800], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[350,1600], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[650,1600], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[250,1500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[750,1500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[0,1400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[1000,1400], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-100,5],[-100,-5],[0,-5],[0,5]]))
        platforms.append(Polygon(pos=[250,1300], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[750,1300], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[350,1200], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[650,1200], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[500,1100], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[200,1050], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[0,950], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,5],[0,-5],[100,-5],[100,5]]))
        platforms.append(Polygon(pos=[250,820], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[500,700], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=800, offsets=[[-75,5],[-75,-5],[75,-5],[75,5]]))
        platforms.append(Polygon(pos=[1000,600], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-250,5],[-250,-5],[0,-5],[0,5]]))

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
        self.coins.append(Circle(pos=[80,2965], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[950,2865], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[150,2765], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[925,2240], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[800,2015], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[50,1365], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))
        self.coins.append(Circle(pos=[500,1065], color=COIN_COLOR, radius=COIN_RADIUS, collision=False))

        # set spawn, checkpoint, and finish positions
        self.checkpoints = []
        self.spawn_pos = Vector2(500,2965)
        self.checkpoints.append([500,2965])
        self.checkpoints.append([200,2515])
        self.checkpoints.append([250,1665])
        self.finish_pos = Vector2(950,565)
    