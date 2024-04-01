import copy
import enum
import pygame
from pygame.math import Vector2
from button import Button
from camera import Camera
from level import Level
from levels.level_four import LevelFour
from levels.level_select import LevelSelect
from levels.level_one import LevelOne
from levels.level_three import LevelThree
from levels.level_two import LevelTwo
from physics_objects import Circle
from contact import generate_contact, resolve_bumper_contact, resolve_contact
from forces import Gravity
import math

# scene enum
class Scene(enum.Enum):
    MENU = 1
    CONTROLS = 2
    GAME = 3
    SELECT = 4
    SHOP = 5

# functions
def death(object):
    global current_checkpoint, warps
    object.vel = Vector2(0,0)
    warp(object, warps, current_checkpoint)

def delete_times():
    file = open(TIMES_FILE_PATH, "w")
    for i in range(len(levels)-1):
        file.write("0\n")

def finish_time(time, level):
    if get_best_time(level) <= 0 or time < get_best_time(level):
        file = open(TIMES_FILE_PATH, "r")
        times = file.readlines()
        file.close()
        file = open(TIMES_FILE_PATH, "w")
        times[level-1] = f"{time}\n"
        file.writelines(times)
        file.close()

def get_best_time(level):
    if level <= 0 or level >= len(levels):
        return 0
    file = open(TIMES_FILE_PATH, "r")
    time = file.readlines()[level-1]
    file.close()
    return float(time)

def hide_buttons():
    for button in buttons:
        button.active = False
        button.selected = False

def next_button():
    for i in range(len(buttons)):
        if buttons[i].selected:
            for j in range(len(buttons)):
                if j > i and buttons[j].active:
                    buttons[j].selected = True
                    buttons[i].selected = False
                    return
            for j in range(len(buttons)):
                if j < i and buttons[j].active:
                    buttons[j].selected = True
                    buttons[i].selected = False
                    return

def previous_button():
    for i in range(len(buttons)):
        if buttons[i].selected:
            for j in reversed(range(len(buttons))):
                if j < i and buttons[j].active:
                    buttons[j].selected = True
                    buttons[i].selected = False
                    return
            for j in reversed(range(len(buttons))):
                if j > i and buttons[j].active:
                    buttons[j].selected = True
                    buttons[i].selected = False
                    return

def select(button):
    global coins, current_checkpoint, current_level, jump_upgrades, paused, running, scene, speed_upgrades, time_trial, ui
    if button.text == TEXT_PLAY:
        paused = False
        ui = False
        hide_buttons()
        menu_button.pos = Vector2(width/2, height/2 + 100)
        warp(player, warps, 0)
        scene = Scene.GAME
    elif button.text == TEXT_CONTROLS:
        hide_buttons()
        menu_button.pos = Vector2(width/2, height/2 + 200)
        menu_button.active = True
        menu_button.selected = True
        scene = Scene.CONTROLS
    elif button.text == TEXT_MENU:
        hide_buttons()
        current_level = 0
        play_button.selected = True
        play_button.active = True
        controls_button.active = True
        quit_button.active = True
        scene = Scene.MENU
    elif button.text == TEXT_RESUME:
        paused = False
        ui = False
        hide_buttons()
    elif button.text == TEXT_QUIT:
        running = False
    elif button.text == TEXT_FREE:
        scene = Scene.GAME
        ui = False
        paused = False
        free_button.active = False
        free_button.selected = False
        time_button.active = False
        back_button.active = False
    elif button.text == TEXT_TIME:
        scene = Scene.GAME
        ui = False
        paused = False
        free_button.active = False
        free_button.selected = False
        time_button.active = False
        time_button.selected = False
        back_button.active = False
        time_trial = True
    elif button.text == TEXT_JUMP:
        if jump_upgrades < UPGRADE_MAX:
            if coins >= pow(2, jump_upgrades + 1):
                coins -= pow(2, jump_upgrades + 1)
                jump_upgrades += 1
    elif button.text == TEXT_SPEED:
        if speed_upgrades < UPGRADE_MAX:
            if coins >= pow(2, speed_upgrades + 1):
                coins -= pow(2, speed_upgrades + 1)
                speed_upgrades += 1
    elif button.text == TEXT_BACK:
        scene = Scene.GAME
        ui = False
        paused = False
        hide_buttons()
        back_button.selected = False
        warp(player, warps, 0)
        current_checkpoint = 0
        current_level = 0

def start_level(level_index):
    global timer
    if level_index <= len(levels):
        for i in range(len(warps)):
            if warps[i] - levels[level_index].pos == levels[level_index].spawn_pos:
                warp(player, warps=warps, index=i)
                timer = 0

def warp(object, warps=[], index=0):
    object.vel = Vector2(0,0)
    copy_warps = copy.deepcopy(warps)
    if index < len(warps):
        object.pos = copy_warps[index]
    else:
        object.pos = copy_warps[index % (len(warps))]

# controls
CAMERA_MOVE_DOWN = pygame.K_DOWN
CAMERA_MOVE_LEFT = pygame.K_LEFT
CAMERA_MOVE_RIGHT = pygame.K_RIGHT
CAMERA_MOVE_UP = pygame.K_UP
DELETE_DATA = pygame.K_DELETE
JUMP = pygame.K_SPACE
MOVE_LEFT = pygame.K_a
MOVE_RIGHT = pygame.K_d
NEXT_WARP = pygame.K_RIGHTBRACKET
PAUSE = pygame.K_ESCAPE
PREVIOUS_WARP = pygame.K_LEFTBRACKET
UI_DOWN = pygame.K_DOWN
UI_LEFT = pygame.K_LEFT
UI_RIGHT = pygame.K_RIGHT
UI_SELECT = pygame.K_RETURN
UI_UP = pygame.K_UP
WARP = pygame.K_RETURN

# constants
BOUNCE_COLOR = [255,150,0]
CAMERA_SPEED = 10
CAMERA_ZOOM_SPEED = 0.1
CHECKPOINT_COLOR = [0,0,255]
CHECKPOINT_RADIUS = 10
DEATH_COLOR = [255,0,0]
FINISH_COLOR = [255,0,255]
FINISH_RADIUS = 20
JUMP_TIME = 8
JUMP_UPGRADE = 20
MARGINS = [0.3,0.4,0.1,0.4]
MAX_JUMP = 540
RESTITUTION = 0.2
SELECTED_COLOR = [150,150,150]
SPEED = 7
SPEED_UPGRADE = 1
TEXT_COLOR = [255,255,255]
TIMES_FILE_PATH = "times.txt"
UPGRADE_MAX = 5
ZOOM_MAX = 10
ZOOM_MIN = 0.1

# variables
coins = 3
jump_velocity = 0
stored_jump_velocity = 0
current_checkpoint = 0
current_level = 0
paused = False
ui = True
debug = True
time_trial = False
timer = 0
speed_upgrades = 0
jump_upgrades = 0

# initialize pygame and open window
pygame.init()
pygame.font.init()
width, height = 800, 600
window = pygame.display.set_mode([width, height])
center = Vector2(width/2, height/2)
diagonal = math.sqrt(width**2 + height**2)
header_font = pygame.font.SysFont("Calibri", 72, True, False)
font = pygame.font.SysFont("Calibri", 48, False, False)
scene = Scene.MENU

# set timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

# set objects
objects = [] 

player = Circle(pos=(100,300), radius=30, mass=1, color=[0,0,255], width=0)
objects.append(player)

gravity_objects = objects.copy()

levels = []
levels.append(LevelSelect(pos=Vector2(0,500)))
levels.append(LevelOne(pos=Vector2(2000,0)))
levels.append(LevelTwo(pos=Vector2(7000,0)))
levels.append(LevelThree(pos=Vector2(13000,0)))
levels.append(LevelFour(pos=Vector2(15000,0)))
for level in levels:
    for obj in level.objects:
        objects.append(obj)
    for coin in level.coins:
        objects.append(coin)
warps = []
for level in levels:
    for checkpoint in level.checkpoints:
        warps.append(Vector2(checkpoint + level.pos))
for point in warps:
    objects.append(Circle(pos=point, radius=CHECKPOINT_RADIUS, color=CHECKPOINT_COLOR, collision=False))
for level in levels:
    objects.append(Circle(pos=level.finish_pos+level.pos, radius=FINISH_RADIUS, color=FINISH_COLOR, collision=False))

warp(player, warps, 0)

level_warps = []
level_warps.append(Circle(pos=levels[0].pos+Vector2(200,-200), radius=FINISH_RADIUS, color=FINISH_COLOR, collision=False))
level_warps.append(Circle(pos=levels[0].pos+Vector2(400,-200), radius=FINISH_RADIUS, color=FINISH_COLOR, collision=False))
level_warps.append(Circle(pos=levels[0].pos+Vector2(600,-200), radius=FINISH_RADIUS, color=FINISH_COLOR, collision=False))
level_warps.append(Circle(pos=levels[0].pos+Vector2(800,-200), radius=FINISH_RADIUS, color=FINISH_COLOR, collision=False))
for level_warp in level_warps:
    objects.append(level_warp)
shop_warp = Circle(pos=levels[0].pos+Vector2(0,-100), collision=False)
objects.append(shop_warp)

# set gravity
gravity = Gravity([0,980], objects_list=gravity_objects)

# set camera
camera = Camera(objects=objects, focus=[width/2,height/2], zoom=1, focus_object=player, margins=MARGINS)

## set ui buttons
# button texts
buttons = []
TEXT_BACK = "Back"
TEXT_CONTROLS = "Controls"
TEXT_FREE = "Free Play"
TEXT_JUMP = "Upgrade Jump"
TEXT_MENU = "Back to Main Menu"
TEXT_PLAY = "Play Game"
TEXT_QUIT = "Quit"
TEXT_RESUME = "Resume"
TEXT_SPEED = "Upgrade Speed"
TEXT_TIME = "Time Trial"
# create buttons
play_button = Button(text=TEXT_PLAY, pos=[width/2, height/2], active=True, selected=True)
buttons.append(play_button)
controls_button = Button(text=TEXT_CONTROLS, pos=[width/2, height/2 + 100], active=True)
buttons.append(controls_button)
resume_button = Button(text=TEXT_RESUME, pos=[width/2, height/2])
buttons.append(resume_button)
menu_button = Button(text=TEXT_MENU, pos=[width/2, height/2 + 100])
buttons.append(menu_button)
quit_button = Button(text=TEXT_QUIT, pos=[width/2, height/2 + 200], active=True)
buttons.append(quit_button)
free_button = Button(text=TEXT_FREE, pos=[width/2, height/2 - 75])
buttons.append(free_button)
time_button = Button(text=TEXT_TIME, pos=[width/2, height/2 + 25])
buttons.append(time_button)
jump_button = Button(text=TEXT_JUMP, pos=[width/4, height/2])
buttons.append(jump_button)
speed_button = Button(text=TEXT_SPEED, pos=[3*width/4, height/2])
buttons.append(speed_button)
back_button = Button(text=TEXT_BACK, pos=[width/2, height/2 + 125])
buttons.append(back_button)

# game loop
running = True
while running:
    # EVENT loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL and debug and not ui:
            camera.zoom += event.y * CAMERA_ZOOM_SPEED
            camera.zoom = max(camera.zoom, ZOOM_MIN)
            camera.zoom = min(camera.zoom, ZOOM_MAX)
        elif event.type == pygame.KEYDOWN and event.key == PAUSE and not paused:
            paused = True
            ui = True
            resume_button.selected = True
            resume_button.active = True
            menu_button.active = True
            quit_button.active = True
        elif event.type == pygame.KEYUP and event.key == UI_SELECT and ui:
            for button in buttons:
                if button.active and button.selected:
                    select(button)
                    break
        elif event.type == pygame.KEYDOWN and event.key == UI_DOWN and ui:
            next_button()
        elif event.type == pygame.KEYDOWN and event.key == UI_UP and ui:
            previous_button()
        elif event.type == pygame.KEYDOWN and event.key == UI_RIGHT and ui:
            next_button()
        elif event.type == pygame.KEYDOWN and event.key == UI_LEFT and ui:
            previous_button()
        elif event.type == pygame.KEYUP and event.key == NEXT_WARP and debug:
            warp(player, warps, current_checkpoint+1)
            current_checkpoint += 1
            if current_checkpoint >= len(warps):
                current_checkpoint = 0
        elif event.type == pygame.KEYUP and event.key == PREVIOUS_WARP and debug:
            warp(player, warps, current_checkpoint-1)
            current_checkpoint -= 1
            if current_checkpoint < 0:
                current_checkpoint = len(warps)-1
        elif event.type == pygame.KEYUP and event.key == WARP and debug:
            warp(player, warps, current_checkpoint)
        elif event.type == pygame.KEYUP and event.key == DELETE_DATA:
            delete_times()

    if not paused:
        if time_trial:
            timer += dt
        
        keys = pygame.key.get_pressed()
        if keys[MOVE_LEFT]:
            player.avel = -(SPEED + SPEED_UPGRADE * speed_upgrades)
        elif keys[MOVE_RIGHT]:
            player.avel = SPEED + SPEED_UPGRADE * speed_upgrades
        else:
            player.avel = 0
        if keys[JUMP]:
            max_jump_with_upgrades = MAX_JUMP + JUMP_UPGRADE * jump_upgrades
            stored_jump_velocity += max_jump_with_upgrades / JUMP_TIME
            stored_jump_velocity = min(stored_jump_velocity, max_jump_with_upgrades)
            if stored_jump_velocity == max_jump_with_upgrades:
                jump_velocity = stored_jump_velocity
        else:
            jump_velocity = stored_jump_velocity
            stored_jump_velocity = 0
        if debug and not ui:
            if keys[CAMERA_MOVE_LEFT]:
                camera.focus[0] -= CAMERA_SPEED / camera.zoom
                camera.focus_object = None
            if keys[CAMERA_MOVE_RIGHT]:
                camera.focus[0] += CAMERA_SPEED / camera.zoom
                camera.focus_object = None
            if keys[CAMERA_MOVE_DOWN]:
                camera.focus[1] += CAMERA_SPEED / camera.zoom
                camera.focus_object = None
            if keys[CAMERA_MOVE_UP]:
                camera.focus[1] -= CAMERA_SPEED / camera.zoom
                camera.focus_object = None

        # clear and apply forces
        for o in objects:
            o.clear_force()
        gravity.apply()
        # update objects
        for o in objects:
            o.update(dt)

        # collisions
        for obj in objects:
            # if isinstance(obj, Level) and obj.enabled:
            #     for level_obj in obj.objects:
            #         if level_obj.collision:
            #             c = generate_contact(player, level_obj)
            #             if c.overlap() > 0 and level_obj.color == DEATH_COLOR:
            #                 death(player)
            #                 if not win:
            #                     coins -= 1
            #             else:
            #                 if level_obj.bounce > 0:
            #                     resolve_bumper_contact(c, level_obj.bounce, friction=level_obj.friction, jump=jump_velocity)
            #                 else:
            #                     resolve_contact(c, restitution=RESTITUTION, friction=level_obj.friction, jump=jump_velocity)
            # else:
            if obj.collision:
                c = generate_contact(player, obj)
                if c.overlap() > 0 and obj.color == DEATH_COLOR:
                    death(player)
                    coins -= 1
                else:
                    if obj.bounce > 0:
                        resolve_bumper_contact(c, obj.bounce, friction=obj.friction, jump=jump_velocity)
                    else:
                        resolve_contact(c, restitution=RESTITUTION, friction=obj.friction, jump=jump_velocity)
        
        # check for warping to levels from hub
        for i in range(len(level_warps)):
            c = generate_contact(player, level_warps[i])
            if c.overlap() > 0:
                start_level(i+1)
                current_level = i+1
                ui = True
                paused = True
                scene = Scene.SELECT
                free_button.active = True
                free_button.selected = True
                time_button.active = True
                back_button.active = True
        # check for shop collision
        c = generate_contact(player, shop_warp)
        if c.overlap() > 0:
            paused = True
            ui = True
            scene = Scene.SHOP
            jump_button.active = True
            speed_button.active = True
            back_button.active = True
            back_button.selected = True

        # check if out of coins
        coins = max(coins, 0)
        
        # check for collecting coins
        for level in levels:
            for coin in level.coins:
                if coin.visible:
                    c = generate_contact(player, coin)
                    if c.overlap() > 0:
                        coin.visible = False
                        coins += 1

        # check if finished level
        for level in levels:
            if (player.pos - (level.pos + level.finish_pos)).magnitude() < FINISH_RADIUS + player.radius:
                warp(player, warps, 0)
                current_checkpoint = 0
                coins += 1
                if time_trial:
                    time_trial = False
                    finish_time(timer, current_level)
                for coin in levels[current_level].coins:
                    coin.visible = True
                current_level = 0

        # check for new checkpoint
        for point in warps:
            if (player.pos - point).magnitude() < CHECKPOINT_RADIUS + player.radius:
                if warps.index(point) > current_checkpoint:
                    current_checkpoint = warps.index(point)

    # DRAW section
    # clear the screen
    if current_level > 0:
        window.fill(levels[current_level].background_color)
    else:
        window.fill([100,100,255])

    # draw everything
    if scene == Scene.MENU:
        window.fill([100,100,100])
        text = header_font.render("Platformer", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, 100])
    elif scene == Scene.CONTROLS:
        window.fill([100,100,100])
        text = header_font.render("Controls", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, 70])
        text = font.render("A | D : Move", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, height/2 - text.get_height()/2 - 100])
        text = font.render("Space : Jump", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, height/2 - text.get_height()/2 - 50])
        text = font.render("Esc : Pause", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, height/2 - text.get_height()/2])
        text = font.render("Arrows : UI", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, height/2 - text.get_height()/2 + 50])
        text = font.render("Enter : Select", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, height/2 - text.get_height()/2 + 100])
    elif scene == Scene.GAME:
        camera.update_and_draw(window)
        window.blit(font.render(f"Coins: {coins}", True, [255,255,255]), [10,10])
        if paused and ui:
            text = header_font.render("Paused", True, [255,255,255])
            window.blit(text, [width/2 - text.get_width()/2, height/2 - text.get_height()/2 - 100])
        if time_trial:
            text = font.render(f"{round(timer,3):.3f}", True, TEXT_COLOR)
            window.blit(text, [width - text.get_width() - 10, 10])
    elif scene == Scene.SELECT:
        window.fill([100,100,100])
        text = header_font.render(f"Level {current_level}", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, 75])
        text = font.render(f"Best Time: {round(get_best_time(current_level),3):.3f}", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, height-100])
    elif scene == Scene.SHOP:
        window.fill([100,100,100])
        window.blit(font.render(f"Coins: {coins}", True, [255,255,255]), [10,10])
        text = header_font.render("Upgrades", True, TEXT_COLOR)
        window.blit(text, [width/2 - text.get_width()/2, 75])
        if jump_upgrades >= UPGRADE_MAX:
            text = font.render("Upgrades maxed", True, TEXT_COLOR)
        else:
            text = font.render(f"Cost: {pow(2, jump_upgrades + 1)}", True, TEXT_COLOR)
        window.blit(text, [width/4 - text.get_width()/2, height/2 - 100])
        if speed_upgrades >= UPGRADE_MAX:
            text = font.render("Upgrades maxed", True, TEXT_COLOR)
        else:
            text = font.render(f"Cost: {pow(2, speed_upgrades + 1)}", True, TEXT_COLOR)
        window.blit(text, [3 * width/4 - text.get_width()/2, height/2 - 100])
    for button in buttons:
        if button.active:
            button.draw(window, font)

    # update the display
    pygame.display.update()

    # delay for correct timing
    clock.tick(fps)
