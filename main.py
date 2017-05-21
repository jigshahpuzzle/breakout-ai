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
		# Initialize Basic State
		pygame.init()
		self.clock = pygame.time.Clock()
		# Initialize Objects
		self.display = pygame.display.set_mode((self.width, self.height))
		paddle = Paddle(self.width, self.height)
		ball = Ball(self.width, self.height)
		bricks = []
		brick_width = self.width / 10
		brick_height = self.height / 25
		for x in range(20):
			for y in range(5):
				brick_x = x * (self.width / 10)
				brick_y = y * (self.height / 25) + 20
				brick = Brick(self.width, self.height, brick_x, brick_y)
				bricks.append(brick)
		# Draw Objects
		self.draw_bg()
		paddle.draw_paddle(self.display)
		ball.draw_ball(self.display)
		for brick in bricks:
			brick.draw_brick(self.display)
		# Update Objects Every Tick
		while ball.alive:
			# Handle events
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			# Handle Object Movements
			keys=pygame.key.get_pressed()
			if keys[K_LEFT]:
				paddle.move_left()
			if keys[K_RIGHT]:
				paddle.move_right()
			ball.move_ball(paddle)
			# Redraw
			self.draw_bg()
			paddle.draw_paddle(self.display)
			ball.draw_ball(self.display)
			for brick in bricks:
				brick.draw_brick(self.display)
			# Update Display
			pygame.display.update()
			self.clock.tick(self.fps)

class Ball(object):

	def __init__(self, game_width, game_height):
		self.xpos = game_width / 2
		self.ypos = game_height / 2
		self.game_width = game_width
		self.game_height = game_height
		self.colors = Colors()
		self.v_x = 1
		self.v_y = 2
		self.alive = True

	def draw_ball(self, display):
		ball = pygame.Rect(self.xpos, self.ypos, 5, 5)
		pygame.draw.rect(display, self.colors.white, ball)

	def move_ball(self, paddle):
		self.xpos = self.xpos + self.v_x
		self.ypos = self.ypos + self.v_y
		if self.xpos >= self.game_width or self.xpos <= 0:
			self.v_x *= -1
		if self.ypos <= 0:
			self.v_y *= -1
		if self.ypos >= self.game_height:
			self.alive = False
		pad = paddle.paddle
		if self.ypos >= pad.top - 2:
			if self.xpos >= pad.left and self.xpos <= pad.right:
				self.v_y *= -1

class Paddle(object):

	def __init__(self, game_width, game_height):
		self.game_width = game_width
		self.xpos = game_width / 2
		self.ypos = game_height - 30
		self.width = game_width / 8
		self.length = 4
		self.colors = Colors()

	def draw_paddle(self, display):
		paddle = pygame.Rect(self.xpos, self.ypos, self.width, self.length)
		pygame.draw.rect(display, self.colors.white, paddle)
		self.paddle = paddle

	def move_left(self):
		if self.xpos > 5:
			self.xpos += -2

	def move_right(self):
		if self.xpos < self.game_width - 5 - self.width:
			self.xpos += 2

class Brick(object):

	def __init__(self, game_width, game_height, xpos, ypos):
		self.width = game_width / 10
		self.height = game_height / 25
		self.colors = Colors()
		self.xpos = xpos
		self.ypos = ypos

	def draw_brick(self, display):
		brick = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
		brick_fill = pygame.Rect(self.xpos + 1, self.ypos + 1,
						self.width - 1, self.height - 1)
		pygame.draw.rect(display, self.colors.blue, brick)
		pygame.draw.rect(display, self.colors.black, brick_fill)

class Colors(object):

	def __init__(self):
		self.black = (0, 0, 0)
		self.white = (255, 255, 255)
		self.maroon = (150, 0, 0)
		self.blue = (85, 155, 215)


if __name__=='__main__':
    executable()

