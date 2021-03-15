import pygame

pygame.init()
width = 1400
height = 840
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
white = (255,255,255)
green = (0, 255, 0)
black = (0, 0, 0)
f = "pic/"

char = pygame.image.load(f+'standing.png')
walkRight = [pygame.transform.rotozoom(pygame.image.load(f+'Run__00'+str(i)+'.png'), 0, 0.15) for i in range(1, 10)]
walkLeft = [
pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load(f+'Run__00'+str(i)+'.png'), 0, 0.15), 1, 0) for i in range(1, 10)]
attackRight = [pygame.transform.rotozoom(pygame.image.load(f+'Attack__00'+str(i)+'.png'), 0, 0.15) for i in range(1, 10)]
attackLeft = [
pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load(f+'Attack__00'+str(i)+'.png'), 0, 0.15), 1, 0) for i in range(1, 10)]

class Ninja():
	def __init__(self, x, y, v, d, h, e):
		self.x = x
		self.y = y
		self.v = v # velocity
		self.d = d # direction
		self.health = h # health
		self.total_health = h
		self.e = e # determine is player 1 or 2 
		self.atk_dir = "r";
		self.atk_status = 0 # 0 for not atk
		self.walkCount = 0
		self.atkCount = 0
		self.standing = True
		self.char_width = char.get_width()/2
		self.char_height = char.get_height()
		self.isJump = False
		self.JumpCount = -10

	def move(self, dir):
		self.d = dir
		if(dir == "r" and self.x < width - self.v - self.char_width):
			self.x = self.x + self.v
			self.standing = False
		if(dir == "l" and self.x > self.v):
			self.x = self.x - self.v
			self.standing = False
		if(dir == "u" and self.y > self.v + 300):
			self.y = self.y - self.v
			self.standing = False
		if(dir == "d" and self.y < height - self.v - self.char_height - 100):
			self.y = self.y + self.v
			self.standing = False

	def jump(self):
		if(self.JumpCount <= 10):
			neg = 1 if self.JumpCount <= 0 else -1
			self.y -= (self.JumpCount ** 2) * 0.2 * neg
			self.JumpCount += 1
		else:
			self.JumpCount = -10
			self.isJump = False

	def attack(self, d_dir):
		dart = Dart(self.x, self.y + self.char_height, 8, d_dir)
		darts.append(dart)

	def hit(self, d_dir):
		self.atk_dir = d_dir
		self.atk_status = 1
		self.atkCount = 0
		hitf = Hitflow(self.x, self.y + self.char_height/2, d_dir)
		flows.append(hitf)

	def draw(self, window):
		if self.atk_status == 0:
			if self.walkCount + 1 >= 27:
				self.walkCount = 0
			if not(self.standing):
				if self.d == "l" or self.d == "d":
					window.blit(walkLeft[self.walkCount//3], (self.x,self.y))
					self.walkCount += 1
				elif self.d == "r" or self.d == "u":
					window.blit(walkRight[self.walkCount//3], (self.x,self.y))
					self.walkCount += 1
			else:
				if self.d == "r" or self.d == "u":
					window.blit(walkRight[0], (self.x, self.y))
				else:
					window.blit(walkLeft[0], (self.x, self.y))
		# normal attack
		elif self.atk_status == 1:
			if self.atkCount + 1 >= 27:
				self.atk_status = 0
				self.walkCount = 0
			if self.atk_dir == "l":
				window.blit(attackLeft[self.atkCount//3], (self.x,self.y))
			elif self.atk_dir == "r":
				window.blit(attackRight[self.atkCount//3], (self.x,self.y))
			self.atkCount += 1
			
		# draw blood
		if(self.e == 1):
			pygame.draw.rect(window, green, (150, 80, self.health*0.03, 6))
		else:
			pygame.draw.rect(window, green, (1250-self.health*0.03, 700, self.health*0.03, 6))
	
class Hitflow(object):
	def __init__(self, x, y, d):
		self.x = x + (100 if d == "r" else -40)
		self.y = y
		self.d = d
	def valid(self, ex, ey, ew, eh):
		if(self.d == "r"):
			if(ew >= ex - self.x >= 0 and eh >= ey - self.y >= -eh): return True
		elif(self.d == "l"):
			if(ew >= self.x - ex >= 0 and eh >= ey - self.y >= -eh): return True
		return False


class Dart(object):
	def __init__(self, x, y, v, d):
		self.x = x + (40 if d == "r" else -40)
		self.y = y
		self.v = v
		self.d = d

	def move(self):
		if self.d == "r":
			self.x += self.v
		elif self.d == "l":
			self.x -= self.v

def dm_dart():
	radius = 3
	for dart in darts:
		continue
		# dart hit man or out of bound
	for dart in darts:
		dart.move()
		pygame.draw.circle(window, black, (dart.x, dart.y), radius)

def hurt(player):
	for f in flows:
		if(f.valid(player.x, player.y, player.char_width, player.char_height)):
			player.health -= 100

def redrawWindow():
	window.fill(white)
	man1.draw(window)
	man2.draw(window)
	dm_dart()

	pygame.display.update()

man1 = Ninja(200, 500, 5, "r", 10000, 1)
man2 = Ninja(1100, 500, 10, "l", 15000 ,2)
run = True
darts = []
flows = []
dart_time = 0

while run:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_LEFT]:
		man1.move("l")        
	elif keys[pygame.K_RIGHT]:
		man1.move("r")
	elif keys[pygame.K_UP]:
		man1.move("u")
	elif keys[pygame.K_DOWN]:
		man1.move("d")
	else:
		man1.standing = True
		man1.walkCount = 0
	if(man1.isJump == False and keys[pygame.K_SPACE]):
		man1.isJump = True
	if man1.isJump:
		man1.jump()
	if keys[pygame.K_a] and dart_time <= 0:
		dart_time = 10
		man1.attack("l")
	elif keys[pygame.K_d] and dart_time <= 0:
		dart_time = 10
		man1.attack("r")

	if keys[pygame.K_e]:
		man1.hit("r")
	elif keys[pygame.K_q]:
		man1.hit("l")

	hurt(man2)
	flows.clear()
	dart_time -= 1
	redrawWindow()

pygame.quit()









