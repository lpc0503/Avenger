from Declaration import *
# from chess import *
######## 可寫在interface
## TODO ICEJJ
def block(where,center_x,center_y,size,color):
	py.draw.rect(where,color,[center_x-size/2,center_y-size/2,size,size])
	py.draw.rect(where,black,[center_x-size/2,center_y-size/2,size,size],3)

def bound(where):
	for i in range(0,36):
		block(where,boundary_x[i],boundary_y[i],60,cyan_blue)
	for i in (90,150,210,270,330,390,450,510):
		for j in (90,150,210,270,330,390,450,510):
			block(where,i,j,60,white)
##########

	# block(400,400,600,cyan_blue)
	# block(400,400,480,white)

def blitRotate(surf, image, pos, originPos, angle):

	# calcaulate the axis aligned bounding box of the rotated image
	w, h       = image.get_size()
	box        = [py.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
	box_rotate = [p.rotate(angle) for p in box]
	min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
	max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

	# calculate the translation of the pivot 
	pivot        = py.math.Vector2(originPos[0], -originPos[1])
	pivot_rotate = pivot.rotate(angle)
	pivot_move   = pivot_rotate - pivot

	# calculate the upper left origin of the rotated image
	origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

	# get a rotated image
	rotated_image = py.transform.rotate(image, angle)

	# rotate and blit the image
	surf.blit(rotated_image, origin)
	# py.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()))

## end blitRotate

## board
board = py.Surface((600,600))

def board_build() :
	board.fill(white)
	bound(board)
	for i in range( 0 ,len(obstacle_x) ) :
		block(board,board_x[obstacle_x[i]][obstacle_y[i]],board_y[obstacle_x[i]][obstacle_y[i]],60,cyan_blue)
	for i in range( 0 ,len(soldier_x) ) :
		block(board,board_x[soldier_x[i]][soldier_y[i]],board_y[soldier_x[i]][soldier_y[i]],60,red)
	for i in range( 0 ,len(enemy_x) ) :
		block(board,board_x[enemy_x[i]][enemy_y[i]],board_y[enemy_x[i]][enemy_y[i]],60,green)

board_angle = 0
board_change_angle = 0
action = True
board_center_pos = (400,400)
board_mode = 0

def board_display(surface):
	global board_change_angle
	global board_angle
	global action
	global move
	if board_change_angle > 0 :
		board_angle += 2
		board_change_angle -=2
	if board_change_angle < 0 :
		board_angle -= 2
		board_change_angle += 2
	if board_change_angle == 0 :
		action = True
	board_angle = board_angle % 360

	blitRotate(surface,board,board_center_pos,(300,300),board_angle)

## end board_display

start_move = False
def board_action(event):
	global board_change_angle
	global board_mode
	global action
	global move
	global start_move

	if event.type == py.KEYDOWN:
		if event.key == py.K_RIGHT:
			if action == True and move == False :
				action = False
				move = True
				board_change_angle = -90
				board_mode += 1
				board_mode = board_mode%4
				print('right')
				start_move = True
		if event.key == py.K_LEFT:
			if action == True and move == False :
				action = False
				move = True
				board_change_angle = 90
				board_mode -= 1
				board_mode = board_mode%4
				print('left')
				start_move = True
		if event.key == py.K_DOWN :
			print('down')

## end board_action

## end board

## chess

obstacle_x = []
obstacle_y = []

def add_obstacle(x,y) :
	obstacle_x.append(x)
	obstacle_y.append(y)
	is_board[x][y] = 1

def clear_obstacle() :
	for i in range(0,len(obstacle_x)) :
		is_board[obstacle_x[i]][obstacle_y[i]] = 0
	obstacle_x.clear()
	obstacle_y.clear()
	board_build()

soldier_x = []
soldier_y = []

def add_soldier(x,y) :
	if is_board[x][y] == 0:
		is_board[x][y] = 1
		soldier_x.append(x)
		soldier_y.append(y)

def kill_soldier(x,y) :
	for i in range(0,len(soldier_x)) :
		if soldier_x[i] == x and soldier_y[i] == y :
			is_board[soldier_x[i]][soldier_y[i]] = 0
			del soldier_x[i]
			del soldier_y[i]
			return

def is_soldier(x,y) :
	for i in range(0,len(soldier_x)) :
		if soldier_x[i] == x and soldier_y[i] == y :
			return True
	return False

def clear_soldier() :
	for i in range(0,len(soldier_x)) :
		is_board[soldier_x[i]][soldier_y[i]] = 0
	soldier_x.clear()
	soldier_y.clear()
	board_build()

move = False
def soldier_down() :
	if action and move :
		for i in range(0,len(soldier_x)) :
			if board_mode == 0 :
				if soldier_x[i] < 7 and is_board[soldier_x[i]+1][soldier_y[i]] == 0 :
					is_board[soldier_x[i]][soldier_y[i]] = 0
					is_board[soldier_x[i]+1][soldier_y[i]] = 1
					soldier_x[i] += 1
			if board_mode == 1 :
				if soldier_y[i] < 7 and is_board[soldier_x[i]][soldier_y[i]+1] == 0 :
					is_board[soldier_x[i]][soldier_y[i]] = 0
					is_board[soldier_x[i]][soldier_y[i]+1] = 1
					soldier_y[i] += 1
			if board_mode == 2 :
				if soldier_x[i] > 0 and is_board[soldier_x[i]-1][soldier_y[i]] == 0 :
					is_board[soldier_x[i]][soldier_y[i]] = 0
					is_board[soldier_x[i]-1][soldier_y[i]] = 1
					soldier_x[i] -= 1
			if board_mode == 3 :
				if soldier_y[i] > 0 and is_board[soldier_x[i]][soldier_y[i]-1] == 0 :
					is_board[soldier_x[i]][soldier_y[i]] = 0
					is_board[soldier_x[i]][soldier_y[i]-1] = 1
					soldier_y[i] -= 1

## end soldier down

enemy_x = []
enemy_y = []

def add_enemy(x,y) :
	if is_board[x][y] == 0 :
		is_board[x][y] = 1
		enemy_x.append(x)
		enemy_y.append(y)

def kill_enemy(x,y) :
	for i in range(0,len(enemy_x)) :
		if enemy_x[i] == x and enemy_y[i] == y :
			is_board[enemy_x[i]][enemy_y[i]] = 0
			del enemy_x[i]
			del enemy_y[i]
			return

def is_enemy(x,y) :
	for i in range(0,len(enemy_x)) :
		if enemy_x[i] == x and enemy_y[i] == y :
			return True
	return False

def clear_enemy() :
	for i in range(0,len(enemy_x)) :
		is_board[enemy_x[i]][enemy_y[i]] = 0
	enemy_x.clear()
	enemy_y.clear()
	board_build()

move = False
def enemy_down() :
	if action and move :
		for i in range(0,len(enemy_x)) :
			if board_mode == 0 :
				if enemy_x[i] < 7 and is_board[enemy_x[i]+1][enemy_y[i]] == 0 :
					is_board[enemy_x[i]][enemy_y[i]] = 0
					is_board[enemy_x[i]+1][enemy_y[i]] = 1
					enemy_x[i] += 1
			if board_mode == 1 :
				if enemy_y[i] < 7 and is_board[enemy_x[i]][enemy_y[i]+1] == 0 :
					is_board[enemy_x[i]][enemy_y[i]] = 0
					is_board[enemy_x[i]][enemy_y[i]+1] = 1
					enemy_y[i] += 1
			if board_mode == 2 :
				if enemy_x[i] > 0 and is_board[enemy_x[i]-1][enemy_y[i]] == 0 :
					is_board[enemy_x[i]][enemy_y[i]] = 0
					is_board[enemy_x[i]-1][enemy_y[i]] = 1
					enemy_x[i] -= 1
			if board_mode == 3 :
				if enemy_y[i] > 0 and is_board[enemy_x[i]][enemy_y[i]-1] == 0 :
					is_board[enemy_x[i]][enemy_y[i]] = 0
					is_board[enemy_x[i]][enemy_y[i]-1] = 1
					enemy_y[i] -= 1

## end enemy down

def move_checker():
	global move
	check_move = False
	for i in range(0,len(soldier_x)) :
		if board_mode == 0 :
			if soldier_x[i] < 7 and is_board[soldier_x[i]+1][soldier_y[i]] == 0 :
				check_move = True
		if board_mode == 1 :
			if soldier_y[i] < 7 and is_board[soldier_x[i]][soldier_y[i]+1] == 0 :
				check_move = True
		if board_mode == 2 :
			if soldier_x[i] > 0 and is_board[soldier_x[i]-1][soldier_y[i]] == 0 :
				check_move = True
		if board_mode == 3 :
			if soldier_y[i] > 0 and is_board[soldier_x[i]][soldier_y[i]-1] == 0 :
				check_move = True
	for i in range(0,len(enemy_x)) :
		if board_mode == 0 :
			if enemy_x[i] < 7 and is_board[enemy_x[i]+1][enemy_y[i]] == 0 :
				check_move = True
		if board_mode == 1 :
			if enemy_y[i] < 7 and is_board[enemy_x[i]][enemy_y[i]+1] == 0 :
				check_move = True
		if board_mode == 2 :
			if enemy_x[i] > 0 and is_board[enemy_x[i]-1][enemy_y[i]] == 0 :
				check_move = True
		if board_mode == 3 :
			if enemy_y[i] > 0 and is_board[enemy_x[i]][enemy_y[i]-1] == 0 :
				check_move = True
	if start_move :
		move = check_move

## edn move checker

def defeat():
	if move == False and action == True :
		if board_mode == 0 :
			for i in range(7,0,-1):
				for j in range(0,8):
					if is_board[i][j] == 1 and is_board[i-1][j] == 1 :
						if is_soldier(i,j) and is_enemy(i-1,j) :
							kill_soldier(i,j)
							py.time.delay(100)
						if is_enemy(i,j) and is_soldier(i-1,j) :
							kill_enemy(i,j)
							py.time.delay(100)
		if board_mode == 1 :
			for j in range(7,0,-1):
				for i in range(0,8):
					if is_board[i][j] == 1 and is_board[i][j-1] == 1 :
						if is_soldier(i,j) and is_enemy(i,j-1) :
							kill_soldier(i,j)
							py.time.delay(100)
						if is_enemy(i,j) and is_soldier(i,j-1) :
							kill_enemy(i,j)
							py.time.delay(100)
		if board_mode == 2 :
			for i in range(0,7):
				for j in range(0,8):
					if is_board[i][j] == 1 and is_board[i+1][j] == 1 :
						if is_soldier(i,j) and is_enemy(i+1,j) :
							kill_soldier(i,j)
							py.time.delay(100)
						if is_enemy(i,j) and is_soldier(i+1,j) :
							kill_enemy(i,j)
							py.time.delay(100)
		if board_mode == 3 :
			for j in range(0,7):
				for i in range(0,8):
					if is_board[i][j] == 1 and is_board[i][j+1] == 1 :
						if is_soldier(i,j) and is_enemy(i,j+1) :
							kill_soldier(i,j)
							py.time.delay(100)
						if is_enemy(i,j) and is_soldier(i,j+1) :
							kill_enemy(i,j)
							py.time.delay(100)

## end defeat

## end chess

##### -------------------- chang it to class -------------------- #####
##### -------------------- chang it to class -------------------- #####
##### -------------------- chang it to class -------------------- #####

class chess :

	def __init__(self,x,y,camp) :
		if is_board[x][y] == 0 :
			self.x = x
			self.y = y
			self.camp = camp
			self.order = None
			is_board[x][y] = 1


	def draw(self) :
		if self.camp == 'obstacle' :
			block(board,board_x[self.x][self.y],board_y[self.x][self.y],60,cyan_blue)
		elif self.camp == 'soldier' :
			block(board,board_x[self.x][self.y],board_y[self.x][self.y],60,red)
		elif self.camp == 'enemy' :
			block(board,board_x[self.x][self.y],board_y[self.x][self.y],60,green)

	def whoami(self,x,y):
		if self.x == x and self.y == y :
			return self.camp
		return None

	def down(self) :
		if action and move :
			if self.camp == 'soldier' or self.camp == 'enemy' :
				if board_mode == 0 :
					if self.x < 7 and is_board[self.x+1][self.y] == 0 :
						is_board[self.x][self.y] = 0
						is_board[self.x+1][self.y] = 1
						self.x += 1
				if board_mode == 1 :
					if self.y < 7 and is_board[self.x][self.y+1] == 0 :
						is_board[self.x][self.y] = 0
						is_board[self.x][self.y+1] = 1
						self.y += 1
				if board_mode == 2 :
					if self.x > 0 and is_board[self.x-1][self.y] == 0 :
						is_board[self.x][self.y] = 0
						is_board[self.x-1][self.y] = 1
						self.x -= 1
				if board_mode == 3 :
					if self.y > 0 and is_board[self.x][self.y-1] == 0 :
						is_board[self.x][self.y] = 0
						is_board[self.x][self.y-1] = 1
						self.y -= 1

	def kill(self,x,y) :
		if self.x == x and self.y == y :
			is_board[self.x][self.y] = 0
			return 'kill'
		return None

	def check(self) :
		global move
		mark = False
		if board_mode == 0 :
			if self.x < 7 and is_board[self.x+1][self.y] == 0 :
				mark = True
		if board_mode == 1 :
			if self.y < 7 and is_board[self.x][self.y+1] == 0 :
				mark = True
		if board_mode == 2 :
			if self.x > 0 and is_board[self.x-1][self.y] == 0 :
				mark = True
		if board_mode == 3 :
			if self.y > 0 and is_board[self.x][self.y-1] == 0 :
				mark = True
		if start_move :
			move = mark
