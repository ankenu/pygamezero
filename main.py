import pgzrun
from pgzero.builtins import *
import random


WIDTH = 1024
HEIGHT = 512
TITLE = "Игра"
FPS = 60

btn_size = 128
btn_space = 56
start_btn = Actor('start-btn', (WIDTH/2 - (btn_size + btn_space), HEIGHT/2))
sound_btn = Actor('soundon-btn', (WIDTH/2, HEIGHT/2))
exit_btn = Actor('exit-btn', (WIDTH/2 + btn_size + btn_space, HEIGHT/2))

foreground_1 = Actor("foreground_1")
foreground_2 = Actor("foreground_2")
foreground_3 = Actor("foreground_3")
foreground_4 = Actor("foreground_4")
foreground_5 = Actor("foreground_5")
foreground_6 = Actor("foreground_6")
foreground_7 = Actor("foreground_7")
foreground_8 = Actor("foreground_8", (WIDTH/2+WIDTH, HEIGHT/2+10))
foreground_9 = Actor("foreground_9", (WIDTH/2+WIDTH, HEIGHT/2+10))
foreground_10 = Actor("foreground_10", (WIDTH/2+WIDTH, HEIGHT/2+10))
foreground_11 = Actor("foreground_11", (WIDTH/2+WIDTH, HEIGHT/2+10))
foreground_12 = Actor("foreground_12", (WIDTH/2+WIDTH, HEIGHT/2+10))
foreground_13 = Actor("foreground_13", (WIDTH/2+WIDTH, HEIGHT/2+10))
foreground_14 = Actor("foreground_14", (WIDTH/2+WIDTH, HEIGHT/2+10))
foreground_15 = Actor("foreground_15", (WIDTH/2+WIDTH, HEIGHT/2+10))

character = Actor("run_right_1", (WIDTH/2, HEIGHT - 64))
bunny = Actor("bunny_stay_1", (WIDTH, HEIGHT - 64))
chicken = Actor("chicken_stay_1", (WIDTH + WIDTH/2, HEIGHT - 64))

mode = "start"
is_playing_music = True
game_amount = 0

def start():
    global mode, game_amount
    mode = "start"
    game_amount += 1

    character.frame = 1
    character.state = "run_right"
    character.jump_length = 200
    character.step = 6
    character.collision_max = 4
    character.collision_current = 0
    character.score = 0

    bunny.frame = 1
    bunny.state = "bunny_stay"
    bunny.passed = False
    bunny.pos = (WIDTH, HEIGHT - 64)

    chicken.frame = 1
    chicken.state = "chicken_stay"
    chicken.passed = False
    chicken.pos = (WIDTH + WIDTH/2, HEIGHT - 64)

def draw():
    global game_amount
    screen.fill((216, 171, 189))
    if mode == "start":
        if game_amount > 1:
            screen.draw.text(
                "Game over",
                color='red',
                midtop=(WIDTH // 2, 10),
                fontsize=200
            )
        start_btn.draw()
        sound_btn.draw()
        exit_btn.draw()
    elif mode == "game":
        foreground_1.draw()
        foreground_2.draw()
        foreground_3.draw()
        foreground_4.draw()
        foreground_5.draw()
        foreground_6.draw()
        foreground_7.draw()

        screen.draw.text(
            str(character.score),
            color='white',
            midtop=(WIDTH // 2, 10),
            fontsize=340
        )

        foreground_8.draw()
        foreground_9.draw()
        foreground_10.draw()
        foreground_11.draw()
        foreground_12.draw()
        foreground_13.draw()
        foreground_14.draw()
        foreground_15.draw()

        if foreground_8.x > -(WIDTH/2 + WIDTH):
            foreground_8.x -= 0.5
        else:
            foreground_8.x = WIDTH + WIDTH/2
            
        if foreground_11.x > -(WIDTH/2 + WIDTH):
            foreground_11.x -= 1.2
        else:
            foreground_11.x = WIDTH + WIDTH/2
            
        if foreground_12.x > -(WIDTH/2 + WIDTH):
            foreground_12.x -= 2
        else:
            foreground_12.x = WIDTH + WIDTH/2
            
        if foreground_13.x > -(WIDTH/2 + WIDTH):
            foreground_13.x -= character.step
        else:
            foreground_13.x = WIDTH + WIDTH/2
        
        if bunny.x > -(WIDTH/2 + WIDTH):
            bunny.x -= character.step
        else:
            bunny.passed = False
            bunny.x = WIDTH + WIDTH/2 + random.randint(0, WIDTH//2)
        
        if chicken.x > -(WIDTH/2 + WIDTH):
            chicken.x -= character.step
        else:
            chicken.passed = False
            chicken.x = WIDTH + random.randint(WIDTH//2, WIDTH) + 150

        if bunny.x < WIDTH/2 - 70 and bunny.passed == False:
            bunny.passed = True
            character.score += 1
            character.step += 0.25
            sounds.coin.play()
        elif chicken.x < WIDTH/2 - 70 and chicken.passed == False:
            chicken.passed = True
            character.score += 1
            character.step += 0.25
            sounds.coin.play()

        character.draw()
        bunny.draw()
        chicken.draw()
    
def update_character(actor):
    if actor.state == "run_right" and actor.frame < 12 or actor.state == "jump" and actor.frame < 6 or actor.state == "bunny_stay" and actor.frame < 8 or actor.state == "chicken_stay" and actor.frame < 13:
        actor.frame += 1
    else:
        actor.frame = 1
    actor.image = f"{actor.state}_{actor.frame}"

def update(dt):
    global mode
    if mode == "start":
        None
    elif mode == "game":
        update_character(character)
        update_character(bunny)
        update_character(chicken)

        if character.colliderect(bunny) or character.colliderect(chicken):
            if character.collision_current > character.collision_max:
                sounds.over.play()
                start()
            else:
                character.collision_current += 1
        else:
            character.collision_current = 0
    
            
def on_mouse_down(pos, button):
    global mode, is_playing_music
    if mode == "start":
        if button == mouse.LEFT and start_btn.collidepoint(pos):
            mode = "game"
        elif button == mouse.LEFT and sound_btn.collidepoint(pos) and sound_btn.image == "soundon-btn":
            music.pause()
            is_playing_music = False
            sound_btn.image = "soundoff-btn"
        elif button == mouse.LEFT and sound_btn.collidepoint(pos) and sound_btn.image == "soundoff-btn":
            music.unpause()
            is_playing_music = True
            sound_btn.image = "soundon-btn"
        elif button == mouse.LEFT and exit_btn.collidepoint(pos):
            exit()

def jump_end():
    character.state = character.previous_state

def jump_start_end():
    animate(character, duration=0.325, pos=(character.pos[0], character.pos[1] + character.jump_length), on_finished=jump_end)

def on_key_down(key, mod, unicode):
    global mode, is_playing_music
    if mode == "game":
        if key == keys.SPACE and character.state != "jump":
            character.previous_state = character.state
            character.state = "jump"
            if is_playing_music:
                sounds.jump.play()
            animate(character, duration=0.325, pos=(character.pos[0], character.pos[1] - character.jump_length), on_finished=jump_start_end)

music.play("time_for_adventure.mp3")
start()
pgzrun.go()
