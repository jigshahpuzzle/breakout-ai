import pygame, sys
from pygame.locals import *

def executable():
	env = PongGameEnv()
	env.startup()

class PongGameEnv(object):

	def __init__(self):
		self.fps = 200
		self.width = 400
		self.height = 300
		self.paddle_size = 50
		self.paddle_offset = 20
		self.line_thickness = 10

	def draw_bg(self):
		self.display.fill((0, 0, 0))
		pygame.draw.rect(self.display, (255, 255, 255),
			((0,0),(self.width,self.height)), self.line_thickness*2)
		pygame.display.update()

	def startup(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((self.width, self.height))
		self.draw_bg()
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()


if __name__=='__main__':
    executable()

