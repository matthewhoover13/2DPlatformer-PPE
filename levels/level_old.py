from pygame import Vector2
from level import Level
from physics_objects import Circle, Polygon, Wall

BOUNCE_COLOR = [255,255,0]
BOUNCE_FRICTION = 0
GROUND_COLOR = [100,255,100]
GROUND_FRICTION = 0.8
ICE_COLOR = [0,255,255]
ICE_FRICTION = 0.3
OBSTACLE_COLOR = [255,0,0]
OBSTACLE_FRICTION = 0
WALL_COLOR = [100,255,100]
WALL_FRICTION = 1

class LevelOld(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_up_level()
        self.local_to_global_space()
    
    def set_up_level(self):
        self.background_color = [100,100,255]
        walls = []
        # ceiling
        walls.append(Polygon(pos=[1000,0], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-1000,-5],[1000,-5],[1000,5],[-1000,5]]))
        # right wall
        walls.append(Polygon(pos=[2000,500], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-500],[5,-500],[5,500],[-5,500]]))
        # left wall
        walls.append(Polygon(pos=[0,500], color=WALL_COLOR, friction=WALL_FRICTION, offsets=[[-5,-500],[5,-500],[5,500],[-5,500]]))
        
        # floors
        floors = []
        # first floor
        floors.append(Polygon(pos=[1000,1000], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-1000,-5],[1000,-5],[1000,5],[-1000,5]]))
        # ledge to second floor
        floors.append(Polygon(pos=[2000,875], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[0,-5],[0,5],[-100,5],[-100,-5]]))
        # second floor
        floors.append(Polygon(pos=[1000,750], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-1000,-5],[800,-5],[800,5],[-1000,5]]))
        # ledge to third floor
        floors.append(Polygon(pos=[0,625], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[100,-5],[100,5],[0,5],[0,-5]]))
        # third floor
        floors.append(Polygon(pos=[1000,500], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-800,-5],[1000,-5],[1000,5],[-800,5]]))
        # ledge to fourth floor
        floors.append(Polygon(pos=[2000,375], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=1000, offsets=[[0,-5],[0,5],[-100,5],[-100,-5]]))
        # fourth floor
        floors.append(Polygon(pos=[1000,250], color=ICE_COLOR, friction=ICE_FRICTION, offsets=[[-1000,-5],[800,-5],[800,5],[-1000,5]]))
        
        # obstacles
        obstacles = []
        # first floor obstacles
        obstacles.append(Polygon(pos=[500,994], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[750,994], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[1000,994], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-100],[5,-100],[5,0]]))
        obstacles.append(Polygon(pos=[1500,994], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        # second floor obstacles
        obstacles.append(Polygon(pos=[1500,744], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[1375,506], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[5,0],[5,50],[-5,50],[-5,0]]))
        obstacles.append(Polygon(pos=[1250,744], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[1125,506], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[5,0],[5,50],[-5,50],[-5,0]]))
        obstacles.append(Polygon(pos=[1000,744], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[875,506], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[5,0],[5,50],[-5,50],[-5,0]]))
        obstacles.append(Polygon(pos=[750,744], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[625,506], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[5,0],[5,50],[-5,50],[-5,0]]))
        obstacles.append(Polygon(pos=[400,744], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[400,506], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[5,0],[5,50],[-5,50],[-5,0]]))
        # third floor obstacles
        obstacles.append(Polygon(pos=[450,256], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,0],[50,0],[0,50]]))
        obstacles.append(Polygon(pos=[500,494], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,-50],[0,0],[-50,0]]))
        obstacles.append(Polygon(pos=[690,256], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,0],[60,0],[0,60]]))
        obstacles.append(Polygon(pos=[750,494], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,-60],[0,0],[-60,0]]))
        obstacles.append(Polygon(pos=[930,256], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,0],[70,0],[0,70]]))
        obstacles.append(Polygon(pos=[1000,494], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,-70],[0,0],[-70,0]]))
        obstacles.append(Polygon(pos=[1250,256], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,0],[0,60],[-60,0]]))
        obstacles.append(Polygon(pos=[1190,494], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,-60],[60,0],[0,0]]))
        obstacles.append(Polygon(pos=[1500,256], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,0],[0,50],[-50,0]]))
        obstacles.append(Polygon(pos=[1450,494], color=BOUNCE_COLOR, friction=BOUNCE_FRICTION, bounce=500, offsets=[[0,-50],[50,0],[0,0]]))
        obstacles.append(Circle(pos=[1700,375], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, radius=50))
        # fourth floor obstacles
        obstacles.append(Polygon(pos=[1600,244], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[1400,244], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-100],[5,-100],[5,0]]))
        obstacles.append(Polygon(pos=[1200,244], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-50],[5,-50],[5,0]]))
        obstacles.append(Polygon(pos=[1200,6], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[5,0],[5,50],[-5,50],[-5,0]]))
        obstacles.append(Polygon(pos=[1000,244], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-100],[5,-100],[5,0]]))
        obstacles.append(Polygon(pos=[1000,6], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[5,0],[5,50],[-5,50],[-5,0]]))
        obstacles.append(Polygon(pos=[700,244], color=OBSTACLE_COLOR, friction=OBSTACLE_FRICTION, offsets=[[-5,0],[-5,-125],[5,-125],[5,0]]))
        obstacles.append(Polygon(pos=[400,244], color=GROUND_COLOR, friction=GROUND_FRICTION, offsets=[[-5,0],[-5,-150],[5,-150],[5,0]]))

        # add all objects to the main objects list
        for wall in walls:
            self.objects.append(wall)
        for floor in floors:
            self.objects.append(floor)
        for obstacle in obstacles:
            self.objects.append(obstacle)
        
        # set spawn, checkpoint, and finish positions
        self.spawn_pos = Vector2(50,950)
        self.checkpoints.append([50,950])
        self.checkpoints.append([1750,700])
        self.checkpoints.append([250,450])
        self.checkpoints.append([1750,200])
        self.finish_pos = Vector2(50,200)
    