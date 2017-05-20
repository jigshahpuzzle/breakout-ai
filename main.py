import pygame, sys
from pygame.locals import *

def executable():
	env = PongGameEnv(400, 400)
	env.startup()

class PongGameEnv(object):

	def __init__(self, width, height):
		self.fps = 200
		self.width = width
		self.height = height
		self.colors = Colors()

	def draw_bg(self):
		self.display.fill(self.colors.maroon)

	def startup(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((self.width, self.height))
		self.draw_bg()
		paddle = Paddle()
		paddle.draw_paddle(self.display)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			self.draw_bg()
			paddle.draw_paddle(self.display)
			pygame.display.update()
			self.clock.tick(self.fps)

class Paddle(object):

	def __init__(self):
		self.xpos = 200
		self.ypos = 370
		self.width = 50
		self.height = 50
		self.colors = Colors()

	def draw_paddle(self, display):
		paddle = pygame.Rect(self.xpos, self.ypos, self.width, 4)
		pygame.draw.rect(display, self.colors.black, paddle)
		pass

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

