import pygame, sys
from pygame.locals import *
from ai import AIPlayer
from math import *

'''
Run in main method
'''
def executable():
	width = 400
	height = 400
	fps = 80
	env = PongGameEnv(width, height, fps)
	env.run_game(1)

'''
Generates game background and executes the main
game loop
'''
class PongGameEnv(object):

	def __init__(self, width, height, fps):
		self.fps = fps
		self.width = width
		self.height = height
		self.colors = Colors()

	def draw_bg(self):
		self.display.fill(self.colors.maroon)

	# game_mode 1 = ai, game_mode 2 = human
	def run_game(self, game_mode):
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
		ai_player = AIPlayer()
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
			if game_mode == 1:
				move = ai_player.generate_move(ball, paddle)
				if move == 1:
					paddle.move_left()
				elif move == 2:
					paddle.move_right()
			elif game_mode == 2:
				keys=pygame.key.get_pressed()
				if keys[K_LEFT]:
					paddle.move_left()
				if keys[K_RIGHT]:
					paddle.move_right()
			bricks = ball.move_ball(paddle, bricks)
			# Redraw
			self.draw_bg()
			paddle.draw_paddle(self.display)
			ball.draw_ball(self.display)
			for brick in bricks:
				brick.draw_brick(self.display)
			# Update Display
			pygame.display.update()
			self.clock.tick(self.fps)

'''
Controls logic for generating the ball and handling
collisions with paddle, bricks, and wall
'''
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

	def move_ball(self, paddle, bricks):
		prev_x = self.xpos
		prev_y = self.ypos
		self.xpos = self.xpos + self.v_x
		self.ypos = self.ypos + self.v_y
		# Handle Edge Collisions
		if self.xpos >= self.game_width - 2 or self.xpos <= 2:
			self.v_x *= -1
		# Handle Top Collision
		if self.ypos <= 2:
			self.v_y *= -1
		# Handle Bottom Collision
		if self.ypos >= self.game_height - 1:
			self.alive = False
		# Handle Paddle Collision
		pad = paddle.paddle
		if self.ypos >= pad.top - 2:
			if self.xpos >= pad.left and self.xpos <= pad.right:
				collision_pos = self.xpos - ((pad.left + pad.right) / 2)
				orientation = collision_pos * 2
				or_angle = 90 - orientation
				v_mag = sqrt((self.v_x ** 2) + (self.v_y ** 2))
				self.v_y = -1 * v_mag * sin(radians(or_angle))
				self.v_x = v_mag * cos(radians(or_angle))
				self.ypos -= 1
		# Handle Brick Collision
		updated_bricks = []
		brick_height = self.game_height / 25
		for brick in bricks:
			curr = brick.brick
			if prev_x <= curr.right and prev_x >= curr.left:
				if self.ypos >= curr.top and self.ypos <= curr.bottom:
					self.v_y *= -1
				else:
					updated_bricks.append(brick)
			elif prev_y >= curr.top and prev_y <= curr.bottom:
				if self.xpos >= curr.left and self.xpos <= curr.right:
					self.v_x *= -1
				else:
					updated_bricks.append(brick)
			else:
				updated_bricks.append(brick)
		return updated_bricks

'''
Generates the paddle and provides interfaces for
humans and the AI to move it.
'''
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

'''
Generates the bricks for the game
'''
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
		pygame.draw.rect(display, self.colors.black, brick)
		pygame.draw.rect(display, self.colors.brown, brick_fill)
		self.brick = brick

'''
Color shades used by the game
'''
class Colors(object):

	def __init__(self):
		self.black = (0, 0, 0)
		self.white = (255, 255, 255)
		self.maroon = (150, 0, 0)
		self.blue = (85, 155, 215)
		self.brown= (210, 105, 30)

if __name__=='__main__':
    executable()

