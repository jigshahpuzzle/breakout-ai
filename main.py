import pygame, sys
from pygame.locals import *

def executable():
	width = 400
	height = 400
	fps = 60
	env = PongGameEnv(width, height, fps)
	env.run_game()

class PongGameEnv(object):

	def __init__(self, width, height, fps):
		self.fps = fps
		self.width = width
		self.height = height
		self.colors = Colors()

	def draw_bg(self):
		self.display.fill(self.colors.maroon)

	def run_game(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((self.width, self.height))
		paddle = Paddle(self.width, self.height)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			keys=pygame.key.get_pressed()
			if keys[K_LEFT]:
				paddle.move_left()
			if keys[K_RIGHT]:
				paddle.move_right()
			self.draw_bg()
			paddle.draw_paddle(self.display)
			pygame.display.update()
			self.clock.tick(self.fps)

class Paddle(object):

	def __init__(self, game_width, game_height):
		self.xpos = game_width / 2
		self.ypos = game_height - 30
		self.width = game_width / 8
		self.length = 4
		self.colors = Colors()

	def draw_paddle(self, display):
		paddle = pygame.Rect(self.xpos, self.ypos, self.width, self.length)
		pygame.draw.rect(display, self.colors.black, paddle)
		pass

	def move_left(self):
		self.xpos += -2

	def move_right(self):
		self.xpos += 2

class Brick(object):

	def __init__(self):
		pass

class Colors(object):

	def __init__(self):
		self.white = (0, 0, 0)
		self.black = (255, 255, 255)
		self.maroon = (150, 0, 0)


if __name__=='__main__':
    executable()

