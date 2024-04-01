import pygame
from pygame.math import Vector2
import itertools
import math

class SingleForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self):
        for obj in self.objects_list:
            force = self.force(obj)
            obj.add_force(force)

    def force(self, obj): # virtual function
        return Vector2(0, 0)


class PairForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self):
        # Loop over all pairs of objects and apply the calculated force
        # to each object, respecting Newton's 3rd Law.  
        # Use either two nested for loops (taking care to do each pair once)
        # or use the itertools library (specifically, the function combinations).
        for pair in itertools.combinations(self.objects_list, 2):
            force = self.force(pair[0], pair[1])
            pair[0].add_force(force)
            pair[1].add_force(-force)

    def force(self, a, b): # virtual function
        return Vector2(0, 0) # return force on a due to b


class BondForce:
    def __init__(self, pairs_list=[]):
        # pairs_list has the format [[obj1, obj2], [obj3, obj4], ... ]
        self.pairs_list = pairs_list

    def apply(self):
        # Loop over all pairs from the pairs list.  
        # Apply the force to each member of the pair respecting Newton's 3rd Law.
        for pair in self.pairs_list:
            force = self.force(pair[0], pair[1])
            pair[0].add_force(force)
            pair[1].add_force(-force)

    def force(self, a, b): # virtual function
        return Vector2(0, 0)

# Add Gravity, SpringForce, SpringRepulsion, AirDrag
class Gravity(SingleForce):
    def __init__(self, acc=(0,0), **kwargs):
        self.acc = Vector2(acc)
        super().__init__(**kwargs)

    def force(self, obj):
        return obj.mass*self.acc
        # Note: this will throw an error if the object has infinite mass.
        # Think about how to handle those.
    
class SpringForce(BondForce):
    def __init__(self, stiff=0, nat_len=0, damp=0, **kwargs):
        self.stiff = stiff
        self.nat_len = nat_len
        self.damp = damp
        super().__init__(**kwargs)
    
    def force(self, a, b):
        r = a.pos - b.pos
        v = a.vel - b.vel
        if r.magnitude() == 0:
            return Vector2(0,0)
        return (-self.stiff * (r.magnitude() - self.nat_len) - self.damp * v.dot(r.normalize())) * r.normalize()
    
    def draw(self, window):
        for pair in self.pairs_list:
            line_color = pygame.Vector3((pair[0].color[0]+pair[1].color[0])/2, (pair[0].color[1]+pair[1].color[1])/2, (pair[0].color[2]+pair[1].color[2])/2)
            pygame.draw.line(window, line_color, pair[0].pos, pair[1].pos)

class AirDrag(SingleForce):
    def __init__(self, drag=0, density=0, area=0, wind=Vector2(0,0), **kwargs):
        self.drag = drag
        self.density = density
        self.area = area
        self.wind = wind
        super().__init__(**kwargs)

    def force(self, obj):
        v = obj.vel - self.wind
        return -0.5*self.drag*self.density*self.area*v.magnitude()*v
        #return -0.5*self.drag*self.density*self.area*v.magnitude()*v

class SpringRepulsion(PairForce):
    def __init__(self, k=0, **kwargs):
        self.k = k
        super().__init__(**kwargs)
    
    def force(self, a, b):
        r = (a.pos-b.pos)
        if a.radius + b.radius - r.magnitude() > 0:
            if r.magnitude() == 0:
                return Vector2(0,0)
            else:
                return self.k * (a.radius+b.radius-r.magnitude()) * r.normalize()
        else:
            return Vector2(0,0)

class Friction(SingleForce):
    def __init__(self, u=1, g=1, **kwargs):
        self.u = u
        self.g = g
        super().__init__(**kwargs)
    
    def force(self, obj):
        if obj.vel.magnitude() == 0:
            return Vector2(0,0)
        return -1 * self.u * obj.mass * self.g * obj.vel.normalize()
