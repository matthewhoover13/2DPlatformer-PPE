import math
from pygame.math import Vector2
import pygame

class Particle:
    # Constructor
    def __init__(self, mass=math.inf, pos=(0,0), collision=True, visible=True, vel=(0,0), momi=math.inf, angle=0, avel=0, friction=0, bounce=0):
        self.mass = mass
        self.pos = Vector2(pos)
        self.collision = collision
        self.visible = visible
        self.vel = Vector2(vel)
        self.momi = momi
        self.angle = angle # in radians
        self.avel = avel
        self.torque = 0
        self.friction = friction
        self.bounce = bounce
        self.clear_force()

    def clear_force(self):
        self.force = Vector2(0,0)
        
    def add_force(self, force):
        self.force += force

    def update(self, dt):
        # update velocity using the current force
        self.vel += (self.force/self.mass)*dt
        # update position using the newly updated velocity
        self.pos += self.vel*dt

        # rotation
        self.avel += (self.torque/self.momi)*dt
        self.angle += self.avel*dt
    
    def impulse(self, impulse):
        self.vel += impulse / self.mass


class Circle(Particle):
    def __init__(self, radius=10, color=[255,255,255], width=0, **kwargs):
        # ** kwargs is a dictionary to catch all the other keyword arguments
        super().__init__(**kwargs) # calls the superclass constructor
        # **kwargs unpacking the kwargs dictionary into key=value, key=value, etc.
        self.radius = radius
        self.color = color
        self.width = width
        self.contact_type = "Circle"

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.radius, self.width)

class Wall(Particle):
    def __init__(self, point1, point2, reverse=False, color=[0,0,0], width=1, **kwargs):
        self.point1 = Vector2(point1)
        self.point2 = Vector2(point2)
        self.contact_type = "Wall"
        super().__init__(pos=(self.point1 + self.point2)/2, **kwargs)
        self.width = width
        self.color = color
        self.normal = (self.point2 - self.point1).normalize().rotate(90)
        if reverse:
            self.normal *= -1

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.point1, self.point2, self.width)
    
    def update(self, dt):
        pass

class Polygon(Particle):
    def __init__(self, offsets=[], color=[255,255,255], width=0, normals_length=0, reverse=False, **kwargs):
        self.contact_type = "Polygon"
        # convert all offsets into Vector2
        self.offsets = []
        for offset in offsets:
            self.offsets.append(Vector2(offset))
        
        # calculate local normals, normals of the unrotated shape
        self.local_normals = []
        for i in range(len(self.offsets)):
            normal = (self.offsets[i-1] - self.offsets[i]).normalize().rotate(90)
            if reverse:
                normal *= -1
            self.local_normals.append(normal)

        self.color = color
        self.width = width
        self.normals_length = normals_length

        super().__init__(**kwargs)

        self.points = self.offsets.copy()
        self.normals = self.local_normals.copy()
        self.update_points()
    
    # compute where the vertices are in space
    def update_points(self):
        for i in range(len(self.offsets)):
            self.points[i] = self.pos + self.offsets[i].rotate_rad(self.angle)
            self.normals[i] = self.local_normals[i].rotate_rad(self.angle)
    
    def draw(self, window):
        pygame.draw.polygon(window, self.color, self.points, self.width)
        if self.normals_length > 0:
            for i in range(len(self.normals)):
                pygame.draw.line(window, [0,0,0], self.points[i], self.points[i] + self.normals[i]*self.normals_length)
    
    # need to override update from Particle so we also update the points
    def update(self, dt):
        super().update(dt)
        self.update_points()
