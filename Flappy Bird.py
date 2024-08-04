import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images and scale them
bird_image = pygame.image.load('bird.png')
start_screen_image = pygame.image.load('start_screen.png')
background_image = pygame.image.load('background.png')
pipe_image = pygame.image.load('pipe.png')
footer_image = pygame.image.load('footer.png')

background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_screen_image = pygame.transform.scale(start_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
footer_image = pygame.transform.scale(footer_image, (SCREEN_WIDTH, footer_image.get_height()))

PIPE_WIDTH = 80
PIPE_HEIGHT = 400
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))

# Load sound effects
pygame.mixer.music.load('bgmusic.mp3')
pygame.mixer.music.play(-1)
collision_sound = pygame.mixer.Sound('collision.wav')
 
# Initialize screen and font
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
font = pygame.font.Font(None, 36)

# Game variables
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_speed = 0
gravity = 0.25
jump_strength = -5

pipe_gap = 150
pipe_frequency = 1500
last_pipe_time = pygame.time.get_ticks()

pipes = []

score = 0
game_over = False
game_started = False

score_thresholds = [10]
score_increments = [10]

def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_image, pipe['top_rect'])
        screen.blit(pygame.transform.flip(pipe_image, False, True), pipe['bottom_rect'])

def draw_footer():
    screen.blit(footer_image, (0, SCREEN_HEIGHT - footer_image.get_height()))

def display_score(score):
    score_surface = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface, (10, 10))

def get_score_increment(score):
    for threshold, increment in zip(score_thresholds, score_increments):
        if score < threshold:
            return increment
    return score_increments[-1]

def main():
    global bird_y, bird_speed, game_over, game_started, pipes, last_pipe_time, score

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started:
                        game_started = True
                    if game_over:
                        bird_y = SCREEN_HEIGHT // 2
                        bird_speed = 0
                        pipes = []
                        score = 0
                        game_over = False
                        last_pipe_time = pygame.time.get_ticks()
                    else:
                        bird_speed = jump_strength

        if game_started and not game_over:
            bird_speed += gravity
            bird_y += bird_speed

            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_time > pipe_frequency:
                pipe_y = random.randint(100, SCREEN_HEIGHT - 100 - pipe_gap)
                pipe_top = pygame.Rect(SCREEN_WIDTH, pipe_y - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)
                pipe_bottom = pygame.Rect(SCREEN_WIDTH, pipe_y + pipe_gap, PIPE_WIDTH, SCREEN_HEIGHT - pipe_y - pipe_gap)
                new_pipe = {
                    'top_rect': pipe_top,
                    'bottom_rect': pipe_bottom,
                    'passed': False
                }
                pipes.append(new_pipe)
                last_pipe_time = current_time

            for pipe in pipes:
                pipe['top_rect'].x -= 2.5
                pipe['bottom_rect'].x -= 2.5

            pipes = [pipe for pipe in pipes if pipe['top_rect'].x > -PIPE_WIDTH]

            bird_rect = pygame.Rect(bird_x, bird_y, bird_image.get_width(), bird_image.get_height())
            collision_occurred = False
            for pipe in pipes:
                if bird_rect.colliderect(pipe['top_rect']) or bird_rect.colliderect(pipe['bottom_rect']):
                    collision_occurred = True
                    break
                if pipe['top_rect'].x < bird_x and not pipe['passed']:
                    pipe['passed'] = True
                    score += get_score_increment(score)

            if collision_occurred:
                collision_sound.play()  # Play collision sound effect
                game_over = True

            if bird_y > SCREEN_HEIGHT - footer_image.get_height() - bird_image.get_height():
                bird_y = SCREEN_HEIGHT - footer_image.get_height() - bird_image.get_height()
                bird_speed = 0
                collision_sound.play()  # Play collision sound effect
                game_over = True

            if bird_y < 0:
                bird_y = 0
                bird_speed = 0
                collision_sound.play()  # Play collision sound effect
                game_over = True

            screen.blit(background_image, (0, 0))
            draw_pipes(pipes)
            draw_bird(bird_x, bird_y)
            draw_footer()
            display_score(score)

        elif not game_started:
            screen.blit(start_screen_image, (0, 0))

        elif game_over:
            screen.blit(start_screen_image, (0, 0))
            display_score(score)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
