import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 50, 0)
black = (0, 0, 0)

# creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#background image
bgimg = pygame.image.load("images/snakeb.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game title
pygame.display.set_caption("Snake is Hungry")
pygame.display.update()

# clock
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_scree(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, green, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, green, [x, y, snake_size, snake_size])


def welcome():
    pygame.mixer.music.load('images/snake.mp3')
    pygame.mixer.music.play(-1)
    exit_game = False
    while not exit_game:
        gameWindow.blit(bgimg, (0,0))
        text_scree("WELCOME TO SNAKE IS HUNGRY", black, 150, 150)
        text_scree("Press ENTER to PLAY", black, 250, 430)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('images/snake_song.mp3')
                    pygame.mixer.music.play(-1)
                    game_loop()

        pygame.display.update()
        clock.tick(60)


# game loop
def game_loop():
    # Game specific variable
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 30
    fps = 60
    score = 0
    vel_x = 0
    vel_y = 0

    init_velocity = 3

    if 100 <= score < 200:
        init_velocity = 10

    if 200 <= score < 300:
        init_velocity = 15

    food_x = random.randint(30, screen_width/2)
    food_y = random.randint(30, screen_height/2)

    snk_list = []
    snk_length = 1

    if(not os.path.exists("highScore.txt")):
        with open("highScore.txt", "w")as f:
            f.write("0")

    with open("highScore.txt", "r") as f:
        highScore = f.read()

    while not exit_game:
        if game_over:
            with open("highScore.txt", "w") as f:
                f.write(str(highScore))

            gameWindow.blit(bgimg, (0,0))
            text_scree(f"GAME OVER! [score is: {score}]", black, screen_width/4, screen_height/8)
            text_scree("Press ENTER to Continue", black, screen_width/4, screen_height / 4)
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        vel_x = init_velocity
                        vel_y = 0
                    if event.key == pygame.K_LEFT:
                        vel_x = -init_velocity
                        vel_y = 0
                    if event.key == pygame.K_UP:
                        vel_y = -init_velocity
                        vel_x = 0
                    if event.key == pygame.K_DOWN:
                        vel_y = init_velocity
                        vel_x = 0

            snake_x += vel_x
            snake_y += vel_y

            if abs(snake_x-food_x) < 15 and abs(snake_y-food_y) < 15:

                score += 10
                food_x = random.randint(30, screen_width / 2)
                food_y = random.randint(30, screen_height / 2)
                snk_length += 10
                if score > int(highScore):
                    highScore = score


            gameWindow.blit(bgimg, (0,0))
            text_scree("SCORE : " + str(score) + "  HIGHEST : " + str(highScore), red, 10, 10)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size - 5, snake_size - 5])

            head =[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('images/go.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('images/go.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, green, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
