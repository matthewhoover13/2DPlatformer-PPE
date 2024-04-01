import math
from pygame.math import Vector2

# Returns a new contact object of the correct type
# This function has been done for you.
def generate_contact(a, b):
    # Check if a's type comes later than b's alphabetically.
    # We will label our collision types in alphabetical order, 
    # so the lower one needs to go first.
    if b.contact_type < a.contact_type:
        a, b = b, a
    # This calls the class of the appropriate name based on the two contact types.
    return globals()[f"Contact_{a.contact_type}_{b.contact_type}"](a, b)
    
# Resolves a contact (by the default method) and returns True if it needed to be resolved
def resolve_contact(contact, restitution=0, friction=0, jump=0):
    # Resolve overlap
    overlap = contact.overlap()
    if overlap > 0:
        m = 1/(1/contact.a.mass + 1/contact.b.mass)
        contact.a.pos += m/contact.a.mass*contact.overlap()*contact.normal()
        contact.b.pos -= m/contact.b.mass*contact.overlap()*contact.normal()

        # Resolve velocity
        sa = contact.point() - contact.a.pos
        sa_ortho = Vector2(-sa[1], sa[0])
        sb = contact.point() - contact.b.pos
        sb_ortho = Vector2(-sb[1], sb[0])
        vel_a_contact = contact.a.vel + contact.a.avel * sa_ortho
        vel_b_contact = contact.b.vel + contact.b.avel * sb_ortho
        v = vel_a_contact - vel_b_contact
        if v.dot(contact.normal()) < 0:
            # Calculate impulse
            n = contact.normal()
            vn = v.dot(n)
            Jn = -(1+restitution)*m*(vn)+m*jump
            t = contact.normal().rotate(90)
            vt = v.dot(t)
            if vt < 0:
                t *= -1
                vt *= -1
            Jt = -m*vt
            if abs(Jt) > friction*Jn:
                Jt = -friction*Jn
            else:
                # Calculate tangential slide from normal velocity and tangential velocity
                slide = abs(vt/vn)*overlap
                contact.a.pos -= slide*m/contact.a.mass*t
                contact.b.pos += slide*m/contact.b.mass*t
            if jump != 0:
                Jt *= 0.1
            impulse = Jn*n + Jt*t
            contact.a.impulse(impulse)
            contact.b.impulse(-impulse)
        return True
    return False

# Resolves a contact with a bumper
def resolve_bumper_contact(contact, rebound=0, friction=0, jump=0):
    # Resolve overlap
    overlap = contact.overlap()
    if overlap > 0:
        m = 1/(1/contact.a.mass + 1/contact.b.mass)
        contact.a.pos += m/contact.a.mass*contact.overlap()*contact.normal()
        contact.b.pos -= m/contact.b.mass*contact.overlap()*contact.normal()

        # Resolve velocity
        sa = contact.point() - contact.a.pos
        sa_ortho = Vector2(-sa[1], sa[0])
        sb = contact.point() - contact.b.pos
        sb_ortho = Vector2(-sb[1], sb[0])
        vel_a_contact = contact.a.vel + contact.a.avel * sa_ortho
        vel_b_contact = contact.b.vel + contact.b.avel * sb_ortho
        v = vel_a_contact - vel_b_contact
        if v.dot(contact.normal()) < 0:
            # Calculate impulse
            n = contact.normal()
            vn = v.dot(n)
            Jn = m*(-v.dot(contact.normal())+rebound)
            t = contact.normal().rotate(90)
            vt = v.dot(t)
            if vt < 0:
                t *= -1
                vt *= -1
            Jt = -m*vt
            if abs(Jt) > friction*Jn:
                Jt = -friction*Jn
            else:
                # Calculate tangential slide from normal velocity and tangential velocity
                slide = abs(vt/vn)*overlap
                contact.a.pos -= slide*m/contact.a.mass*t
                contact.b.pos += slide*m/contact.b.mass*t
            if jump != 0:
                Jt *= 0.1
            impulse = Jn*n + Jt*t
            contact.a.impulse(impulse)
            contact.b.impulse(-impulse)
        return True
    return False

# Generic contact class, to be overridden by specific scenarios
class Contact():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.renew()
 
    def renew(self):  # virtual function
        pass

    def overlap(self):  # virtual function
        return 0

    def normal(self):  # virtual function
        return Vector2(0, 0)
    
    def point(self):  # virtual function
        return Vector2(0, 0)


# Contact class for two circles
class Contact_Circle_Circle(Contact):
    def __init__(self, a, b):
        super().__init__(a, b)

    def overlap(self):
        return self.a.radius + self.b.radius - (self.a.pos - self.b.pos).magnitude()  # Overlap between two objects

    def normal(self):
        if self.a.pos == self.b.pos:
            return Vector2(0,0)
        return (self.a.pos - self.b.pos).normalize()  # Normal from b to a
    
    def point(self):
        return self.a.pos + self.a.radius * -self.normal()

# Contact class for a circle and a polygon
class Contact_Circle_Polygon(Contact):
    def __init__(self, a, b):
        self.circle = a
        self.polygon = b
        super().__init__(a, b)
    
    def renew(self):
        # check overlap with each side
        # check overlap with a vertex

        min_overlap = math.inf
        self.circle_overlaps_vertex = False

        # one option
        #for i in range(len(self.polygon.points)):
        #    wall_pos = self.polygon.points[i]
        #    wall_normal = self.polygon.normals[i]
        
        # another option, use zip
        for i, (wall_pos, wall_normal) in enumerate(zip(self.polygon.points, self.polygon.normals)):
            overlap = self.circle.radius - (self.circle.pos - wall_pos).dot(wall_normal)
            if overlap < min_overlap:
                min_overlap = overlap
                self.index = i  # index of the side of least overlap
        
        # check if the circle is beyond either of the two endpoints
        point1 = self.polygon.points[self.index]
        point2 = self.polygon.points[self.index - 1]
        side = point1 - point2
        if (self.circle.pos - point1).dot(side) > 0:
            self.circle_overlaps_vertex = True
            self.index = self.index  # index is the index of the vertex
        elif (self.circle.pos - point2).dot(side) < 0:
            self.circle_overlaps_vertex = True
            self.index = self.index - 1  # index is the index of the vertex

    def overlap(self):
        if self.circle_overlaps_vertex:
            # circle overlaps vertex
            return self.circle.radius - (self.a.pos - self.polygon.points[self.index]).magnitude()
        else:
            # circle overlaps side
            wall_pos = self.polygon.points[self.index]
            wall_normal = self.polygon.normals[self.index]
            return self.circle.radius - (self.circle.pos - wall_pos).dot(wall_normal)  # Overlap between two objects

    def normal(self):
        if self.circle_overlaps_vertex:
            # circle overlaps vertex
            return (self.circle.pos - self.polygon.points[self.index]).normalize()
        else:
            # circle overlaps side
            return self.polygon.normals[self.index]  # Normal from b to a
    
    def point(self):
        if self.circle_overlaps_vertex:
            return self.polygon.points[self.index]  # vertex of polygon
        else:
            return self.circle.pos - self.circle.radius * self.normal()  # circle position displaced by radius in the opposite direction of normal

# Contact class for a circle and a wall
class Contact_Circle_Wall(Contact):
    def __init__(self, a, b):
        super().__init__(a, b)
        self.circle = a
        self.wall = b

    def overlap(self):
        return self.circle.radius - (self.circle.pos - self.wall.pos).dot(self.wall.normal)  # Overlap between two objects

    def normal(self):
        return self.wall.normal  # Normal from b to a
    
    def point(self):
        return self.circle.pos + self.circle.radius * -self.normal()

# Empty class for polygon on polygon collision
class Contact_Polygon_Polygon(Contact):
    def __init__(self, a, b):
        super().__init__(a, b)

# Empty class for polygon on wall collision
class Contact_Polygon_Wall(Contact):
    def __init__(self, a, b):
        super().__init__(a, b)

# Empty class for wall on wall collision
class Contact_Wall_Wall(Contact):
    def __init__(self, a, b):
        super().__init__(a, b)
