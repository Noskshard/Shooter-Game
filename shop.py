import pygame
import os

pygame.font.init()
FASTER_FIRING_RATE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "faster_firing_rate.png")), (210, 210))
MORE_LASERS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "more_lasers.png")), (210, 210))
MORE_HEALTH = pygame.transform.scale(pygame.image.load(os.path.join("assets", "more_health.webp")), (210, 210))
REGEN_HEALTH = pygame.transform.scale(pygame.image.load(os.path.join("assets", "regen_health.png")), (210, 210))
title_font = pygame.font.SysFont("comicsans", 50)
item_font = pygame.font.SysFont("comicsans", 20)
button_font = pygame.font.SysFont("comicsans", 40)
title_height = title_font.get_height()
item_width = 210
cooldown = 30
clicked_more_health = False
clicked_regen_health = False
lasers = 1
money = 0

class ShopItem:
    def __init__(self, x, y , label, img, window):
        self.x = x
        self.y = y
        self.label = label
        self.img = img
        self.edge = item_width
        self.rect = img.get_rect(center = (x + 105, y + 105))
        self.window = window
    
    def check_click(self, event):
        return self.rect.collidepoint(event.pos)
    
    def draw(self):
        self.window.blit(self.img, (self.x, self.y))
        self.window.blit(self.label, (self.x, self.edge + self.y))
    

def shop_menu(window, BG, WIDTH, HEIGHT, player_money):
    global money
    global cooldown
    global clicked_more_health
    global clicked_regen_health
    global lasers
    gap = 30
    run = True
    money = player_money
    while run:
        window.blit(BG, (0,0))
        faster_rate = ShopItem(gap, title_height + gap + 10, item_font.render("Firing Rate x2: $10", 1, (255, 255, 0)), FASTER_FIRING_RATE, window)
        if lasers == 1:
            more_lasers = ShopItem(item_width + 2*gap, title_height + gap + 10, item_font.render("+1 Laser: $10", 1, (255, 255, 0)), MORE_LASERS, window)
        elif lasers == 2:
            more_lasers = ShopItem(item_width + 2*gap, title_height + gap + 10, item_font.render("+1 Laser: $20", 1, (255, 255, 0)), MORE_LASERS, window)
        elif lasers == 3:
            more_lasers = ShopItem(item_width + 2*gap, title_height + gap + 10, item_font.render("Unavailable", 1, (255, 255, 0)), MORE_LASERS, window)
        more_health = ShopItem(2*item_width + 3*gap, title_height + gap + 10, item_font.render("HP x2: $20", 1, (255, 255, 0)), MORE_HEALTH, window)
        regen_health = ShopItem(gap, title_height + item_width+ 2*gap + 10, item_font.render("Regen 50% HP: $5", 1, (255, 255, 0)), REGEN_HEALTH, window)
        next_level_label = button_font.render("NEXT LEVEL", 1, (0, 255, 0))
        title_label = title_font.render("Shop", 1, (255,255,0))
        money_label = title_font.render(f"Money: {money}", 1, (0, 255, 0))
        window.blit(money_label, (WIDTH/2 + 120, 10))
        
        faster_rate.draw()
        more_lasers.draw()
        more_health.draw()
        regen_health.draw()
        window.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 10))
        next_level_rect = pygame.draw.rect(window, (255, 255,0), (WIDTH/2 - 150, HEIGHT - 100, 300, 60))
        window.blit(next_level_label, (WIDTH/2 - next_level_label.get_width()/ 2, HEIGHT - 100))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if faster_rate.check_click(event):
                    if money >= 10:
                        cooldown /= 2
                        money -= 10
                if more_lasers.check_click(event):
                    if lasers == 1 and money >= 10:
                        lasers += 1
                        money -= 10
                    elif lasers == 2 and money >= 20:
                        lasers += 1
                        money -= 20
                if more_health.check_click(event):
                    if money >= 20:
                        clicked_more_health = True
                        money -= 20
                if regen_health.check_click(event):
                    if money >= 5:
                        clicked_regen_health = True
                        money -= 5
                if next_level_rect.collidepoint(event.pos):
                    return
    pygame.quit()
