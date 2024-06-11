import pygame
import time
from button import Button
from player import Player
from world import World
from enemy import Enemy
from lava import Lava
from exit import Exit

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

tile_size = 50
game_over = 0
main_menu = True

sun_img = pygame.image.load('sun.png')
bg_img = pygame.image.load('sky.png')
restart_img = pygame.image.load('restart_btn.png')
start_img = pygame.image.load('start_btn.png')
exit_img = pygame.image.load('exit_btn.png')

# Initialize the timer variables
start_time = 0
fastest_time = float('inf')

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 7, 2, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world = World(world_data, blob_group, lava_group, exit_group, tile_size)
player = Player(100, screen_height - 130)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

# Function to load the fastest time
def load_fastest_time():
    try:
        with open("fastest_time.txt", "r") as file:
            return float(file.read().strip())
    except:
        return float('inf')

# Function to save the fastest time
def save_fastest_time(time):
    with open("fastest_time.txt", "w") as file:
        file.write(str(time))

fastest_time = load_fastest_time()

run = True
while run:
    clock.tick(fps)
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu:
        if exit_button.draw(screen):
            run = False
        if start_button.draw(screen):
            main_menu = False
            start_time = time.time()  # Start the timer when the game starts
    else:
        world.draw(screen)
        if game_over == 0:
            blob_group.update()
        blob_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        game_over = player.update(game_over, world, blob_group, lava_group, exit_group, screen)

        # Display the current timer only if the game is not over
        if game_over == 0:
            current_time = time.time() - start_time
        else:
            current_time = current_time  # Maintain the current time when the game is over

        font = pygame.font.SysFont('Arial', 30)
        timer_text = font.render(f'Time: {current_time:.2f}', True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))

        # Display the fastest time
        if fastest_time < float('inf'):
            fastest_time_text = font.render(f'Fastest Time: {fastest_time:.2f}', True, (255, 255, 255))
            screen.blit(fastest_time_text, (10, 50))

        # if player has died
        if game_over == -1:
            if restart_button.draw(screen):
                player.reset(100, screen_height - 130)
                game_over = 0
                start_time = time.time()  # Reset the timer
        if game_over == 1:
            if current_time < fastest_time:
                fastest_time = current_time
                save_fastest_time(fastest_time)
            if restart_button.draw(screen):
                player.reset(100, screen_height - 130)
                game_over = 0
                start_time = time.time()  # Reset the timer

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
