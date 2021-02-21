# name: elisa_-_snake.py
# auth: (c) 2020 christian bitter
# desc: a simply snake clone
# in snake, we have a snake that the player can steer
# the goal of the player is to:
# 	eat the food that appears in the world
# 	by eating food the snake grows
# 	and the player has to manage to not bite himself, and stay clear of walls
# vers: 0.2

from random import randint
import time
import pygame

C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_FOOD = (168, 228, 255)
C_SNAKE = (128, 255, 129)
C_SNAKE_TAIL = (128, 192, 156)
C_FOREST     = (16, 80, 64)
C_EMPTY = (32, 32, 32)

EMPTY_IDX = -2
FOOD_IDX = -1
SNAKE_IDX = 0
SNAKE_TAIL_IDX = 1

def on_quit():
	print("Elisa -> Quit()")

def clear_buffer(buffer, clear_color):
	buffer.fill(clear_color)

def draw_snake(buffer, _xi, _yi, tile_size):
	pygame.draw.rect(buffer, C_SNAKE, (_xi, _yi, tile_size, tile_size), 0)
	pygame.draw.rect(buffer, (16, 192, 16), (_xi, _yi, tile_size, tile_size), 5)
	pygame.draw.rect(buffer, (32, 192, 32), (_xi, _yi, tile_size, tile_size), 3)
	pygame.draw.rect(buffer, (64, 192, 64), (_xi, _yi, tile_size, tile_size), 1)

def draw_world(buffer, x_off:int, y_off:int, tile_size:int, world:list):
	_x0, _y0 = x_off, y_off
	world_width, world_height = len(world), len(world[0])

	for _i in range(len(world)):
		_xi = x_off
		_yi = _y0 + _i * tile_size
		_scan_line = world[_i]
		for _j in range(len(_scan_line)):
			tile_i = _scan_line[_j]

			if tile_i == FOOD_IDX:
				pygame.draw.rect(buffer, C_FOOD, (_xi, _yi, tile_size, tile_size), 0)	
			elif tile_i == SNAKE_IDX:
				draw_snake(buffer, _xi, _yi, tile_size)
			elif tile_i == SNAKE_TAIL_IDX:
				pygame.draw.rect(buffer, C_SNAKE_TAIL, (_xi, _yi, tile_size, tile_size), 0)
			else:
				pass

			_xi += tile_size

	pygame.draw.rect(buffer, C_WHITE, (x_off, x_off, world_width * tile_size, world_height * tile_size), 1)

def main():
	no_pass, no_fail = pygame.init()

	if no_fail > 0:
		print("Not all pygame modules initialized correctly")
		print(pygame.get_error())
	else:
		print("All pygame modules initializes")

	if not pygame.font:
		print("Pygame - fonts not loaded")
	if not pygame.mixer:
		print("Pygame - audio not loaded")
	if not pygame.display:
		print("Pygame - display not loaded")
	if not pygame.mouse:
		print("Pygame - mouse not loaded")

	pygame.register_quit(on_quit)

	w, h, t = 640, 480, "Elisa - Snake"
	c_white = (255, 255, 255)

	screen_buffer = pygame.display.set_mode(size=(w, h), flags=0)
	pygame.display.set_caption(t, "Snake")
	pygame.mouse.set_visible(True)

	back_buffer: pygame.Surface = pygame.Surface(screen_buffer.get_size())
	back_buffer = back_buffer.convert()
	back_buffer.fill(c_white)

	fps_watcher = pygame.time.Clock()
	is_done = False

	world_x, world_y = 50, 50
	world_width, world_height = 20, 20
	tile_size = 20
	world = [
		world_width * [EMPTY_IDX] for y in range(world_height)
	]

	# Display some text
	font  = pygame.font.Font(None, 36)
	font2 = pygame.font.Font(None, 28)

	# food is placed, if there is none
	world_has_food = False
	snake_length   = 1
	snake = []
	snake_x, snake_y = 10, 10	
	move_x, move_y = 0, 0
	started = False
	shrink = True
	points = 0

	game_message = None
	loose_message = None

	while not is_done:
		elapsed_millis = fps_watcher.tick(10)

		shrink = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_done = True
				break
		
		# we cannot move into our opposite movement direction since this means we bite ourself
		key_map = pygame.key.get_pressed()
		if key_map[pygame.K_LEFT] and move_x != 1:
			move_x = -1
			move_y = 0
			started = True
		elif key_map[pygame.K_RIGHT] and move_x != -1:
			move_x = 1
			move_y = 0
			started = True
		elif key_map[pygame.K_DOWN] and move_y != -1:
			move_y = 1
			move_x = 0
			started = True
		elif key_map[pygame.K_UP] and move_y != 1:
			move_y = -1
			move_x = 0
			started = True
		else:
			pass

		clear_buffer(back_buffer, C_FOREST)

		if not started:
			game_message = font.render(f"SNAKE", 1, C_SNAKE)
			back_buffer.blit(game_message, (250, 150))
			game_message = font2.render(f"Press Arrow Key to Start", 1, C_SNAKE_TAIL)			
			back_buffer.blit(game_message, (180, 250))
		else:
			snake_x, snake_y = snake_x + move_x, snake_y + move_y
			snake.append((snake_x, snake_y))

			if started and not (0 <= snake_x < world_width) or not (0 <= snake_y < world_height):
				loose_message = "Be careful little snake ... walls hurt!"
				is_done = True
				break

			if started and world[snake_y][snake_x] >= SNAKE_IDX:
				loose_message = "Oh no you have grown too quick ...!"
				is_done = True
				break
		
			if world[snake_y][snake_x] == FOOD_IDX:
				# in this case we also do not remove the tail
				points += 1
				snake_length += 1
				world_has_food = False
				shrink = False
		
			while not world_has_food:
				x, y = randint(0, world_width - 1), randint(0, world_height - 1)				
				if world[y][x] == EMPTY_IDX:
					world[y][x] = FOOD_IDX
					world_has_food = True			

			# chop off everything after length
			if shrink and len(snake) > snake_length:
				rem   = snake[0]
				snake = snake[1:]
				x_rem, y_rem = rem
				world[y_rem][x_rem] = EMPTY_IDX

			# the last is always the head			
			for i, (snake_x, snake_y) in enumerate(snake):
				if i == len(snake) - 1:
					world[snake_y][snake_x] = SNAKE_IDX
				else:
					world[snake_y][snake_x] = SNAKE_TAIL_IDX

			# eating a food item increases the length by one and leads to not removing the tail in this iteration
			draw_world(back_buffer, world_x, world_y, tile_size, world)

			text_score = font.render(f"Score: {points}", 1, C_WHITE)
			back_buffer.blit(text_score, (200, 10))

		screen_buffer.blit(back_buffer, (0, 0))
		pygame.display.flip()

	text_loose = font2.render(loose_message, 1, C_WHITE)
	screen_buffer.blit(text_loose, (150, 200))
	pygame.display.flip()

	time.sleep(1)

	pygame.quit()

if __name__ == '__main__':
	main()
