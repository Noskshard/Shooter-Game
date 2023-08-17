import pygame
import os
import time
import random
import enemy_variety as E
import shop as S
pygame.font.init()

WIDTH , HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

# load images

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
YELLOW_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
RED_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
COIN = pygame.image.load(os.path.join("assets", "pixel_coin.webp"))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img,(self.x, self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return self.y > height or self.y < 0
    
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.max_health = health
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
        
    def cooldown(self):
        if self.cool_down_counter >= S.cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()
    
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=100)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.health = health
        self.player_damage = 50
        self.money = 0


    def move_lasers(self,vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    self.laser_hit_enemy(laser, obj, objs)
        
    def laser_hit_enemy(self, laser, obj, objs):
        if laser.collision(obj):
            if obj.color == "red":
                obj.health -= self.player_damage
                if obj.health == 0:
                    objs.remove(obj)
                    create_coin(obj)
            else:
                objs.remove(obj)
                create_coin(obj)
            self.lasers.remove(laser) 

    def draw(self, window):
        super().draw(window)
        self.draw_healthbar(window)
    
    def shoot(self):
        if self.cool_down_counter == 0:
            print(S.lasers)
            if S.lasers == 1:
                laser = Laser(self.x, self.y, self.laser_img)
                self.lasers.append(laser)
            elif S.lasers == 2:
                laser1 = Laser(self.x + self.get_width() / 2, self.y, self.laser_img)
                self.lasers.append(laser1)
                laser2 = Laser(self.x - self.get_width() / 2, self.y, self.laser_img)
                self.lasers.append(laser2)
            elif S.lasers == 3:
                laser1= Laser(self.x, self.y, self.laser_img)
                self.lasers.append(laser1)
                laser2= Laser(self.x - self.get_width()/ 2, self.y, self.laser_img)
                self.lasers.append(laser2)
                laser3= Laser(self.x + self.get_width()/ 2, self.y, self.laser_img)
                self.lasers.append(laser3)
            self.cool_down_counter = 1

    def draw_healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=100)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.color = color

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            if self.ship_img == BLUE_SHIP:
                laser = Laser(self.x - self.get_width()/2, self.y, self.laser_img)
            else:
                laser = Laser(self.x - 13, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1   

    def draw(self, window):
        super().draw(window)
        if self.color == "red":
            self.draw_healthbar(window)

    def draw_healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height(), self.ship_img.get_width(), 5))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height(), self.ship_img.get_width() * (self.health/self.max_health), 5))
 
class Coin(Laser):
    def __init__(self, x, y, img, coin_width, coin_height):
        super().__init__(x, y, img)
        self.img = pygame.transform.scale(COIN, (coin_width, coin_height))
        self.mask = pygame.mask.from_surface(self.img)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

coins = []

def create_coin(enemy_ship):
    short_edge = min(enemy_ship.get_width(), enemy_ship.get_height())
    long_edge = max(enemy_ship.get_width(), enemy_ship.get_height())
    delta = (long_edge - short_edge) / 2
    coin = Coin(enemy_ship.x + delta, enemy_ship.y, COIN, short_edge, short_edge)
    coins.append(coin)

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    lost = False
    lost_count = 0
    laser_vel = 8

    enemies = []
    wave_length = 5
    default_enemy_vel = 1
    player_vel = 5

    player = Player(300, 600)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))

        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        money_label = main_font.render(f"Money: {player.money}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH / 2 - level_label.get_width() / 2, 10))
        WIN.blit(money_label, (WIDTH - money_label.get_width() - 10, 10))
        player.draw(WIN)
        for coin in coins:
            coin.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2 - lost_label.get_height() / 2))    


        pygame.display.update()

    while(run):
        clock.tick(FPS)
        redraw_window() 

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0 and len(coins) == 0:
            if level >= 1:
                S.shop_menu(WIN, BG, WIDTH, HEIGHT, player.money)
                player.money = S.money
            if S.clicked_more_health:
                player.health += player.max_health
                player.max_health *= 2
                S.clicked_more_health = False
            if S.clicked_regen_health:
                player.health = player.max_health if player.health > player.max_health / 2 else player.health + player.max_health / 2
                S.clicked_regen_health = False
            level += 1
            pixel_enemy_ratio = 100
            if level > 3:
                pixel_enemy_ratio = 70
            elif level > 6:
                pixel_enemy_ratio = 40
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-wave_length * pixel_enemy_ratio, -10), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: 
            player.x -= player_vel       
        if keys[pygame.K_d] and player.x + player_vel < WIDTH - player.get_width():
            player.x += player_vel    
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel < HEIGHT - player.get_height():
            player.y += player_vel 
        if keys[pygame.K_SPACE]:
            player.shoot()

        for coin in coins[:]:
            coin.move(laser_vel)
            if collide(coin, player):
                player.money += 1
                coins.remove(coin)
            if coin.y > HEIGHT:
                coins.remove(coin)
        
        for enemy in enemies:
            enemy.move(E.enemy_vel_based_on_level(default_enemy_vel, level, enemy))
            enemy.move_lasers(laser_vel / 4, player)

            if  random.randrange(0, 2*FPS) == 1:
                enemy.shoot()

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            
            if collide(enemy, player):
                player.health -= E.enemy_collision_damage(enemy, 20)
                enemies.remove(enemy)

        player.move_lasers(-3* laser_vel, enemies)
    
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
main_menu() 