import pygame
from pygame.locals import *
import time
import random
import os
from pygame import mixer

SIZE = 40
BLACK = "#3B3B3B"

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = self.load_image("apple.jpg")
        self.x, self.y = self.place_randomly()

    def load_image(self, filename):
        try:
            image_path = os.path.join("E:/Python/Snake-Game/resource", filename)
            return pygame.image.load(image_path).convert()
        except pygame.error as e:
            print(f"Error loading image {filename}: {e}")
    
    def move(self):
        self.x=random.randint(1,19)*SIZE
        self.y=random.randint(1,16)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def place_randomly(self):
        return random.randint(1, 19) * SIZE, random.randint(1, 16) * SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = self.load_image("piece.png")
        self.direction = 'down'
        self.length = 1
        self.x, self.y = [40], [40]

    def load_image(self, filename):
        try:
            image_path = os.path.join("E:/Python/Snake-Game/resource", filename)
            return pygame.image.load(image_path).convert()
        except pygame.error as e:
            print(f"Error loading image {filename}: {e}")

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((800, 700))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()


    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >=  x2 and x1<=x2 + SIZE:
            if y1>=y2  and y1<=y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg_path = os.path.join(os.getcwd(), "E:/Python/Snake-Game/resource/background.png")
        bg = pygame.image.load(bg_path)
        self.surface.blit(bg, (0, 0))


    def play_sound(self, sound_file):
        try:
            sound_path = os.path.join(os.getcwd(), "E:/Python/Snake-Game/resource", sound_file)
            pygame.mixer.Sound(sound_path).play()
        except pygame.error as e:
            print(f"Error playing sound {sound_file}: {e}")


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if (self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y)):
            self.play_sound("Apple-bite.mp3")
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself or the screen boundaries
        if (
            self.snake.x[0] < 0
            or self.snake.x[0] >= 800
            or self.snake.y[0] < 0
            or self.snake.y[0] >= 700
            or self.check_self_collision()):
            self.play_sound("crash.mp3")
            self.show_game_over()
            time.sleep(2)
            self.reset()

    def check_self_collision(self):
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 28)
        score = font.render(f"Score: {self.snake.length-1}", True, (0,0,0))
        self.surface.blit(score, (650, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 25)
        line1 = font.render(f"Game is over! Your score is {self.snake.length-1}", True, (90,0,255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (90,0,255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    elif not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                print(f"Exception caught: {e}")
                self.show_game_over()
                pause = True
                self.reset()


            time.sleep(.15)

if __name__ == '__main__':
    game = Game()
    game.run()
