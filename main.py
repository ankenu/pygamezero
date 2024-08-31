import pgzrun
from pgzero.builtins import *


WIDTH = 1024
HEIGHT = 512
TITLE = "Игра"
FPS = 20

btn_size = 128
btn_space = 56

start_btn = Actor('start-btn', (WIDTH/2 - (btn_size + btn_space), HEIGHT/2))
sound_btn = Actor('soundon-btn', (WIDTH/2, HEIGHT/2))
exit_btn = Actor('exit-btn', (WIDTH/2 + btn_size + btn_space, HEIGHT/2))

tiles = ['empty', 'block']
tile_size = 64

class Item:
    def __init__(self, img, pos, state = "stay"):
        self.state = state
        self.frame = 1
        self.actor = Actor(img, pos)

    def animate(self, state, limit):
        self.state = state
        if self.frame < limit:
            self.frame += 1
        else:
            self.frame = 1
        self.actor.image = f"{self.state}_{self.frame}"

class Player(Item):
    def __init__(self, img = "stay_1", pos =  (32, HEIGHT - 96 - 64*2), step = 4, jump_length = 192, state = 'stay'):
        super().__init__(img, pos, state)
        self.step = step
        self.jump_length = jump_length
        self.jump_start_pos = (0, 0)
        self.oranges = 0

    def stay(self):
        self.animate('stay', 11)

    def run_left(self):
        self.animate('run_left', 12)

    def run_right(self):
        self.animate('run_right', 12)
    
    def jump(self):
        self.animate('jump', 1)
    
    def jump_left(self):
        self.animate('jump_left', 6)
    
    def jump_right(self):
        self.animate('jump_right', 6)

    def fall(self):
        self.animate('fall', 1)

    def fall_right(self):
        self.animate('fall_right', 1)
    
    def fall_left(self):
        self.animate('fall_left', 1)
    
    def is_on_block():
        None

mode = "start"
is_playing_music = True
player = None
tile_map = []
tile_map_x = 0

def start():
    global tile_map, tile_map_x, player
    tile_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '.', 0, 0, 'c', 0, 'c', 0, 'c', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '.', 0, 0, 'b', 0, 0, 0, '.', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '.', '.', '.', '.', 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '.', '.', '.', '.', '.', '.', '.', '.', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '.', '.', '.', '.', '.', 0, 'b', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, '.', 0, 0, 'c', 0, 0, '.', 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    tile_map_x = 0
    player = Player()

def draw():
    global game_amount

    screen.clear()
    screen.fill((216, 171, 189))
    
    if mode == "start":
        start_btn.draw()
        sound_btn.draw()
        exit_btn.draw()
    elif mode == "fail":
        screen.draw.text(
            "FAIL",
            color='red',
            midtop=(WIDTH // 2, 10),
            fontsize=200
        )
        start_btn.draw()
        sound_btn.draw()
        exit_btn.draw()
    elif mode == "win":
        screen.draw.text(
            "VICTORY",
            color='green',
            midtop=(WIDTH // 2, 10),
            fontsize=200
        )
        start_btn.draw()
        sound_btn.draw()
        exit_btn.draw()
    elif mode == "game":
        for row in range(len(tile_map)):
            for column in range(len(tile_map[row])):
                x = column * tile_size - tile_map_x
                y = row * tile_size
                screen.blit('empty', (x, y))

        screen.draw.text(
            str(player.oranges),
            color='white',
            midtop=(WIDTH // 2, 10),
            fontsize=500
        )

        for row in range(len(tile_map)):
            for column in range(len(tile_map[row])):
                x = column * tile_size - tile_map_x
                y = row * tile_size
                if isinstance(tile_map[row][column], str):
                    if tile_map[row][column] == ".":
                        tile_map[row][column] = Item("orange_1", (x, y), "orange")
                    elif tile_map[row][column] == "b":
                        tile_map[row][column] = Item("bunny_stay_1", (x, y), "bunny_stay")
                    elif tile_map[row][column] == "c":
                        tile_map[row][column] = Item("chicken_stay_1", (x, y), "chicken_stay")
                    tile_map[row][column].actor.topleft = (x, y)
                    tile_map[row][column].actor.draw()
                elif isinstance(tile_map[row][column], Item):
                    tile_map[row][column].actor.draw()
                    tile_map[row][column].actor.topleft = (x, y)
                    if tile_map[row][column].state == "orange":
                        tile_map[row][column].animate("orange", 17)
                    elif tile_map[row][column].state == "bunny_stay":
                        tile_map[row][column].animate("bunny_stay", 8)
                    elif tile_map[row][column].state == "chicken_stay":
                        tile_map[row][column].animate("chicken_stay", 13)
                else:
                    tile = tiles[tile_map[row][column]]
                    if tile != "empty":
                        screen.blit(tile, (x, y))
        player.actor.draw()

def get_tile(pos):
    global mode

    x, y = pos
    row = int(y / tile_size)
    column = int((x + tile_map_x) / tile_size)
    if column < len(tile_map[0]) and row < len(tile_map):
        if isinstance(tile_map[row][column], int):
            return tiles[tile_map[row][column]]
        elif isinstance(tile_map[row][column], str):
            # ВРЕМЕННО
            return "empty"
        elif tile_map[row][column].state == "orange":
            if is_playing_music:
                sounds.coin.play()
            player.oranges += 1
            tile_map[row][column] = 0
            return "empty"
        elif tile_map[row][column].state == "bunny_stay" or tile_map[row][column].state == "chicken_stay":
            sounds.over.play()
            mode = "fail"
    return None

def update(dt):
    global mode, tile_map_x

    if mode == "game":
        x, y = player.actor.pos
        
        if player.state == "jump" or player.state == "jump_left" or player.state == "jump_right":
            tile = get_tile(player.actor.midtop)
            if tile == "empty":
                _, y_start_pos = player.jump_start_pos
                if y_start_pos - y < player.jump_length:
                    y -= player.step * 2
                elif player.state == "jump_right":
                    player.fall_right()
                elif player.state == "jump_left":
                    player.fall_left()
                else:
                    player.fall()
            elif tile == "block":
                player.fall()

        if player.state == "fall" or player.state == "fall_right" or player.state == "fall_left":
            # Falling to a block or an empty tile
            tile = get_tile(player.actor.midbottom)
            tile_side = get_tile(player.actor.bottomright) if player.state == "fall_right" else get_tile(player.actor.bottomleft)
            if (player.state == "fall_right" or player.state == "fall_left") and tile_side == "empty" or player.state == "fall" and tile == "empty":
                if player.state == "fall_right":
                    x += player.step
                    player.fall_right()
                elif player.state == "fall_left":
                    x -= player.step
                    player.fall_left() 
                elif player.state == "fall":
                    player.fall()
                y += player.step * 2
            elif (player.state == "fall_right" or player.state == "fall_left") and tile_side == "block" or tile == "block":
                player.stay()
        elif keyboard.D or keyboard.RIGHT or player.state == "jump_right" or (keyboard.D or keyboard.RIGHT) and (player.state == "jump" or player.state == "fall"):
            # Right tile check
            tile = get_tile(player.actor.midright)
            if tile == "empty":
                x += player.step

                if player.state == "jump_right":
                    player.jump_right()
                elif player.state == "jump" or player.state == "fall":
                    player.fall_right()
                elif keyboard.SPACE:
                    player.jump_start_pos = player.actor.pos
                    player.jump_right()
                else:
                    player.run_right()
            elif tile == "block":
                player.stay()

            # Bottom tile check
            tile = get_tile(player.actor.midbottom)
            if tile == "empty" and player.state != "jump_right" and player.state != "fall_right":
                player.fall()
                y += player.step * 2
            elif tile == "block" and player.state == "fall":
                player.run_right()
        elif keyboard.A or keyboard.LEFT or player.state == "jump_left" or (keyboard.A or keyboard.LEFT) and (player.state == "jump" or player.state == "fall"):
            # Left tile check
            tile = get_tile(player.actor.midleft)
            if tile == "empty":
                x -= player.step

                if player.state == "jump_left":
                    player.jump_left()
                elif player.state == "jump" or player.state == "fall":
                    player.fall_left()
                elif keyboard.SPACE:
                    player.jump_start_pos = player.actor.pos
                    player.jump_left()
                else:
                    player.run_left()
            elif tile == "block":
                player.stay()

            # Bottom tile check
            tile = get_tile(player.actor.midbottom)
            if tile == "empty" and player.state != "jump_left" and player.state != "fall_left":
                player.fall()
                y += player.step * player.step / 2
            elif tile == "block" and player.state == "fall":
                player.run_left()
        elif player.state == "jump":
            player.jump()
        elif keyboard.SPACE:
            player.jump_start_pos = player.actor.pos
            player.jump()
        elif player.state != "fall" and player.state != "fall_right" and player.state != "fall_left":
            player.stay()
        
        if x > tile_size / 4 and x < WIDTH:
            if y >= HEIGHT:
                sounds.over.play()
                mode = "fail"
            if (x >= WIDTH / 2 or tile_map_x > 0) and tile_map_x < tile_size * len(tile_map[0]) - WIDTH:
                tile_map_x += x - player.actor.pos[0]
                player.actor.pos = (player.actor.pos[0], y)
            elif x > WIDTH - tile_size:
                mode = "win"
            else:
                player.actor.pos = (x, y)
        elif player.state != "run_right" and player.state != "run_left":
            player.fall()
    
            
def on_mouse_down(pos, button):
    global mode, is_playing_music
    if mode == "start" or mode == "win" or mode == "fail":
        if button == mouse.LEFT and start_btn.collidepoint(pos):
            start()
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

music.play("time_for_adventure.mp3")
start()
pgzrun.go()
