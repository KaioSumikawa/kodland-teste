import random, math
from pygame import Rect

WIDTH, HEIGHT = 900, 600
STATE_MENU, STATE_GAME = "menu", "game"
game_state, sound_on = STATE_MENU, True
score, coins = 0, []
COIN_COUNT = 10

class Button:
    def __init__(self, image, pos, action, scale=0.5):
        self.actor = Actor(image, center=pos)
        self.actor.scale, self.action = scale, action
    def draw(self): self.actor.draw()
    def check_click(self, pos):
        if Rect(self.actor.x-75, self.actor.y-50, 150, 100).collidepoint(pos):
            self.action(); return True
        return False

class SoundButton(Button):
    def __init__(self, pos, action, scale=0.5):
        super().__init__("button_sound_on", pos, action, scale)
    def update_state(self, is_sound_on):
        self.actor.image = "button_sound_on" if is_sound_on else "button_sound_off"

class Coin:
    def __init__(self, pos):
        self.actor = Actor("coin", center=pos)
        self.actor.scale, self.collected = 0.5, False
    def draw(self):
        if not self.collected: self.actor.draw()
    def check_collision(self, hero_hitbox):
        if not self.collected and Rect(self.actor.x-15, self.actor.y-15, 30, 30).colliderect(hero_hitbox):
            self.collected = True; return True
        return False

class Character:
    def __init__(self, pos, idle_frames, walk_right_frames, walk_left_frames, scale=0.18, speed=3, hitbox_size=40, is_hero=False):
        self.pos, self.speed, self.target = list(pos), speed, None
        self.anim_timer, self.frame, self.state, self.direction = 0, 0, "idle", "right"
        self.idle_frames, self.walk_right_frames, self.walk_left_frames = idle_frames, walk_right_frames, walk_left_frames
        self.hitbox_size, self.actor = hitbox_size, Actor(idle_frames[0], center=pos)
        self.actor.scale, self.is_hero, self.move_sound_cooldown = scale, is_hero, 0
    
    def update_movement(self):
        if not self.target: return
        dx, dy = self.target[0]-self.pos[0], self.target[1]-self.pos[1]
        if (dist:=math.hypot(dx, dy)) > 2:
            self.pos[0] += self.speed*dx/dist; self.pos[1] += self.speed*dy/dist
            self.state = "walk"
            if self.is_hero and sound_on and self.move_sound_cooldown <= 0:
                try: sounds.move.play(); self.move_sound_cooldown = 30
                except: pass
            if dx > 0: self.direction = "right"
            elif dx < 0: self.direction = "left"
        else: self.target, self.state = None, "idle"
        if self.move_sound_cooldown > 0: self.move_sound_cooldown -= 1
    
    def animate(self, speed=10):
        self.anim_timer += 1
        if self.anim_timer > speed:
            self.anim_timer, self.frame = 0, (self.frame+1)%2
        frames = self.walk_right_frames if self.state=="walk" and self.direction=="right" else self.walk_left_frames if self.state=="walk" else self.idle_frames
        self.actor._flip_x = (self.direction=="left" and self.state=="idle")
        self.actor.image, self.actor.center = frames[self.frame], self.pos
    
    def update(self): self.update_movement(); self.animate()
    def draw(self): self.actor.draw()
    def get_hitbox(self):
        hs = self.hitbox_size//2
        return Rect(self.pos[0]-hs, self.pos[1]-hs, self.hitbox_size, self.hitbox_size)

class Hero(Character):
    def __init__(self, pos):
        super().__init__(pos, ["hero_idle_1","hero_idle_2"], ["hero_walk_right_1","hero_walk_right_2"], 
                        ["hero_walk_left_1","hero_walk_left_2"], scale=0.18, speed=3, hitbox_size=35, is_hero=True)

class Enemy(Character):
    def __init__(self, area):
        pos = [random.randint(area.left,area.right), random.randint(area.top,area.bottom)]
        super().__init__(pos, ["enemy_idle_1","enemy_idle_2"], ["enemy_walk_right_1","enemy_walk_right_2"], 
                        ["enemy_walk_left_1","enemy_walk_left_2"], scale=0.18, speed=1.2, hitbox_size=40)
        self.area, self.move_counter, self.idle_timer, self.is_idle = area, 0, 0, False
    
    def choose_target(self):
        self.target = (random.randint(self.area.left,self.area.right), random.randint(self.area.top,self.area.bottom))
        self.move_counter, self.is_idle = random.randint(30, 90), False
    
    def go_idle(self):
        self.target, self.state, self.idle_timer, self.is_idle = None, "idle", random.randint(60, 180), True
    
    def update(self):
        if self.is_idle:
            self.idle_timer -= 1
            if self.idle_timer <= 0: self.choose_target()
        else:
            if not self.target or self.move_counter <= 0 or random.random() < 0.01:
                self.go_idle() if random.random() < 0.3 else self.choose_target()
            super().update(); self.move_counter -= 1

enemy_area = Rect(50, 50, 800, 500)
hero, enemies = None, []

menu_bg, game_bg = Actor("menu_background", center=(WIDTH//2, HEIGHT//2)), Actor("game_background", center=(WIDTH//2, HEIGHT//2))
game_logo = Actor("logo_penguin_parade", center=(WIDTH//2, 150)); game_logo.scale = 1.2

def spawn_coins(count=COIN_COUNT):
    global coins
    coins = [Coin((random.randint(100,WIDTH-100), random.randint(100,HEIGHT-100))) for _ in range(count)]

def reset_game():
    global hero, enemies, score
    hero, enemies, score = Hero((WIDTH//2, HEIGHT//2)), [Enemy(enemy_area) for _ in range(4)], 0
    hero.target = None; spawn_coins()

reset_game()
if sound_on: music.play("bg_music")

def start_game():
    global game_state
    reset_game(); game_state = STATE_GAME; music.stop()
    if sound_on: music.play("game_music")

def toggle_sound():
    global sound_on; sound_on = not sound_on
    sound_button.update_state(sound_on)
    if sound_on: music.play("bg_music" if game_state==STATE_MENU else "game_music")
    else: music.stop()

def exit_game(): quit()

start_button = Button("button_start", (750,350), start_game, 0.5)
sound_button = SoundButton((750,450), toggle_sound, 0.5)
exit_button = Button("button_exit", (750,550), exit_game, 0.5)
buttons = [start_button, sound_button, exit_button]

def draw():
    screen.clear()
    if game_state == STATE_MENU:
        menu_bg.draw(); game_logo.draw()
        for b in buttons: b.draw()
    else:
        game_bg.draw()
        coins_left = len([c for c in coins if not c.collected])
        screen.draw.text("Enemies:", topleft=(20, 20), fontsize=28, color=(220, 100, 100))
        screen.draw.text(f"{len(enemies)}", topleft=(130, 20), fontsize=28, color=(255, 50, 50))
        screen.draw.text("Score:", topright=(WIDTH-20, 20), fontsize=28, color=(255, 200, 0))
        screen.draw.text(f"{score}", topright=(WIDTH-130, 20), fontsize=28, color=(255, 255, 0))
        screen.draw.text("Coins:", topright=(WIDTH-20, 60), fontsize=24, color=(255, 180, 0))
        screen.draw.text(f"{coins_left}/{COIN_COUNT}", topright=(WIDTH-130, 60), fontsize=24, color=(255, 220, 0))
        screen.draw.text("Click to move hero | ESC to menu", center=(WIDTH//2, HEIGHT-25), fontsize=22, color=(100, 200, 255))
        for coin in coins: coin.draw()
        hero.draw()
        for e in enemies: e.draw()

def update():
    global score
    if game_state == STATE_GAME:
        hero.update()
        for e in enemies: e.update()
        for e in enemies:
            if hero.get_hitbox().colliderect(e.get_hitbox()):
                if sound_on:
                    try: sounds.enemy_hit.play()
                    except: pass
                hero.pos = list(random.choice([(100,100),(WIDTH-100,100),(100,HEIGHT-100),(WIDTH-100,HEIGHT-100)]))
                hero.target = None
        hero_hitbox = hero.get_hitbox()
        for coin in coins[:]:
            if coin.check_collision(hero_hitbox):
                if sound_on:
                    try: sounds.coin.play()
                    except: pass
                score += 10; coins.remove(coin)
        if len(coins) == 0: spawn_coins()

def on_mouse_down(pos):
    if game_state == STATE_MENU:
        for b in buttons:
            if b.check_click(pos): break
    else: hero.target = pos

def on_key_down(key):
    global game_state
    if key == keys.ESCAPE:
        if game_state == STATE_GAME:
            game_state = STATE_MENU; music.stop()
            if sound_on: music.play("bg_music")
        else: exit_game()

print("Penguin Parade iniciado! Números agora em cores fortes para melhor visibilidade.")

import pgzrun
pgzrun.go()