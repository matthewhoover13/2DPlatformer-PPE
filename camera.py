import copy
from pygame import Vector2
from level import Level

from physics_objects import Circle, Polygon, Wall

class Camera():
    def __init__(self, objects=[], focus=Vector2(0,0), zoom=1, focus_object=None, margins=[0,0,0,0]):
        self.objects = objects
        self.objects_camera_space = copy.deepcopy(self.objects)
        self.focus = focus
        self.zoom = max(zoom, 0)
        self.focus_object = focus_object
        self.margins = []
        for margin in margins:
            margin = min(margin, 0.5)
            margin = max(margin, 0)
            self.margins.append(margin)
    
    def update_and_draw(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        center = Vector2(width/2, height/2)
        if self.focus_object != None:
            if self.objects_camera_space[0].pos[0] > width * (1 - self.margins[1]):
                self.focus[0] += self.objects_camera_space[0].pos[0] - width * (1 - self.margins[1])
            if self.objects_camera_space[0].pos[0] < width * self.margins[3]:
                self.focus[0] += self.objects_camera_space[0].pos[0] - width * self.margins[3]
            if self.objects_camera_space[0].pos[1] > height * (1 - self.margins[2]):
                self.focus[1] += self.objects_camera_space[0].pos[1] - height * (1 - self.margins[2])
            if self.objects_camera_space[0].pos[1] < height * self.margins[0]:
                self.focus[1] += self.objects_camera_space[0].pos[1] - height * self.margins[0]
        self.objects_camera_space = copy.deepcopy(self.objects)
        for i in range(len(self.objects_camera_space)):
            self.update(self.objects_camera_space[i], center)
        for obj in self.objects_camera_space:
            if obj.visible:
                obj.draw(screen)
    
    def update(self, object, center):
        if isinstance(object, Level):
            for obj in object.objects:
                self.update(obj, center)
        else:
            world_diff = object.pos - center
            scaled_diff = world_diff * self.zoom
            object.pos = center + scaled_diff + (center - self.focus) * self.zoom
            if isinstance(object, Circle):
                object.radius = object.radius * self.zoom
                object.width = int(object.width * self.zoom)
            elif isinstance(object, Polygon):
                for k in range(len(object.offsets)):
                    object.offsets[k] = object.offsets[k] * self.zoom
                object.width = int(object.width * self.zoom)
                object.normals_length = object.normals_length * self.zoom
                object.update_points()
            elif isinstance(object, Wall):
                point1WorldDiff = object.point1 - center
                point2WorldDiff = object.point2 - center
                point1ScaledDiff = point1WorldDiff * self.zoom
                point2ScaledDiff = point2WorldDiff * self.zoom
                object.point1 = center + point1ScaledDiff + (center - self.focus) * self.zoom
                object.point2 = center + point2ScaledDiff + (center - self.focus) * self.zoom
    