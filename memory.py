import sys

from PIL import Image
import random
import pygame
import os
import time



def draw_text(text, font, text_col, x, y, background):
    img = font.render(text, True, text_col)
    img_rect = img.get_rect()
    img_rect.left = x-img_rect.width/2
    img_rect.top = y
    if background:
        pygame.draw.rect(screen, (255-text_col[0], 255-text_col[1], 255-text_col[2]), img_rect)
    screen.blit(img, (x-img_rect.width/2, y))

def extract_sprites(sheet_path, sprite_width, sprite_height):
    sheet = Image.open(sheet_path)
    sheet_width = sheet.size[0]
    sheet_height = sheet.size[1] - sprite_height
    sprites = []
    for y in range(0, sheet_height, sprite_height):
        for x in range(0, sheet_width, sprite_width):
            box = (x, y, x + sprite_width, y + sprite_height)
            sprite = sheet.crop(box)
            sprites.append(sprite)
    return sprites

def pil_image_to_surface(pil_image):
    return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

# Sprite sheet pad
sheet_path = "Fruits/Sheet/Sheet_Fruits_StandAlone.png"
if not os.path.exists(sheet_path):
    raise FileNotFoundError(f"Sprite sheet niet gevonden op: {sheet_path}")

sprite_width, sprite_height = 96, 96
sprites_original = extract_sprites(sheet_path, sprite_width, sprite_height)
player = 1
player_points = [0, 0]
player_color = [(0, 0, 255), (255, 0, 0)]
new_sprites = []
vakjes_rooster = [6, 5]
for i in range(int(vakjes_rooster[0] * vakjes_rooster[1] / 2)):
    random_index = random.randint(0, len(sprites_original) - 1)
    new_sprites.append(sprites_original[random_index])
    sprites_original.pop(random_index)

fruits = [pil_image_to_surface(sprite) for sprite in new_sprites]
fruits.extend(fruits)  # Dubbele lijst voor memory game
random.shuffle(fruits)

fruits_rooster = []
fruits_rect = []
index = 0
for x in range(vakjes_rooster[0]):
    fruits_rooster.append([])
    fruits_rect.append([])
    for y in range(vakjes_rooster[1]):
        fruits_rooster[x].append(fruits[index])
        fruits_rect[x].append(pygame.Rect([x * sprite_width, y * sprite_height], [sprite_width, sprite_height]))
        index += 1

pygame.init()
text_font = pygame.font.SysFont("papyrus", 30)
screen = pygame.display.set_mode((sprite_width * vakjes_rooster[0], sprite_height * vakjes_rooster[1]))
pygame.display.set_caption('Memory')
selected = []
show = []

def draw_game():
    if mode == 0:
        screen.fill(player_color[player-1])
        for x in range(vakjes_rooster[0]):
            for y in range(vakjes_rooster[1]):
                sprite = fruits_rooster[x][y]
                rect = fruits_rect[x][y]
                screen.blit(pygame.image.load("Fruits/A_Panel_96x96.png"), rect.topleft)

                if [x, y] in show or [x, y] == selected:
                    screen.blit(sprite, rect.topleft)

    elif mode == 1:
        rect1 = pygame.Rect([0, 0], (sprite_width * vakjes_rooster[0], sprite_height * vakjes_rooster[1]))
        rect2 = pygame.Rect([(sprite_width * vakjes_rooster[0])/2, 0], (sprite_width * vakjes_rooster[0], sprite_height * vakjes_rooster[1]))
        pygame.draw.rect(screen, player_color[0], rect1)
        pygame.draw.rect(screen, player_color[1], rect2)
        draw_text(str(player_points[0]), text_font, (0, 0, 0), sprite_width * vakjes_rooster[0]/4, sprite_height * vakjes_rooster[1] /2, False)
        draw_text(str(player_points[1]), text_font, (0, 0, 0), sprite_width * vakjes_rooster[0] / 4 * 3, sprite_height * vakjes_rooster[1] /2, False)

    pygame.display.flip()
running = True
mode = 0
while running:
    if mode == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                for x in range(vakjes_rooster[0]):
                    for y in range(vakjes_rooster[1]):
                        if fruits_rect[x][y].colliderect(pygame.Rect([mouse_x, mouse_y], [1, 1])):
                            if not selected:
                                selected = [x, y]

                            elif fruits_rooster[x][y] == fruits_rooster[selected[0]][selected[1]]:
                                if selected != [x, y] and not [x, y] in show:
                                    #yes
                                    show.append([x, y])
                                    show.append(selected)
                                    player_points[player-1] += 1
                                    selected = []
                                    if len(show) == len(fruits):
                                        mode = 1
                                #else unvalid
                            else:
                                #no
                                player = [1, 2][[2, 1].index(player)]
                                sprite = fruits_rooster[x][y]
                                rect = fruits_rect[x][y]
                                screen.blit(sprite, rect.topleft)
                                pygame.display.update()
                                time.sleep(0.5)
                                selected = []
        if mode == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    draw_game()


pygame.quit()
sys.exit()
