import pygame as pg
from pygame import Vector2
from color import *
from emath import *
from math import floor, cos, sin, pi
from circle import *
from line import *
from threading import *
import random


class Ball:
	max_speed = 50
	speed_increment = 0.5
	r = 25
	pg.mixer.init()
	reflect_voice = pg.mixer.Sound("audio\\pong.mp3")

	def __init__(self, start_pos: Vector2, direction: Vector2 = Vector2(1, 0), start_speed: float = 0, color: Color = Color(255, 255, 255)):
		self.pos = Vector2(start_pos)
		spread = 30
		rand1 = random.randint(180 - spread, 360 + spread - 180)
		rand2 = random.randint(-spread, spread)
		rand = rand1 if random.randint(0, 1) else rand2
		self.dir = Vector2(cos(rand * pi / 180), sin(rand * pi / 180)).normalize()
		self.color = color
		self.speed = float(start_speed)
		self.start_speed = start_speed
		self.spawn_pos = start_pos
		self.va = Vector2(1, 0) if self.dir.x >= 0 else Vector2(-1, 0)

	def respawn(self):
		self.pos = Vector2(self.spawn_pos)
		self.speed = float(self.start_speed)

	def on_reflect(self):
		rf = self.reflect_voice
		rf.play()
		if self.speed + self.speed_increment < self.max_speed:
			self.speed += self.speed_increment

	def move(self, objects: list):
		x = self.pos.x
		y = self.pos.y
		radius = self.r
		spd = float(self.speed)
		for obj in objects:
			if type(obj) is Rectangle:
				for i in range(obj.get_point_count()):
					p1, p2 = obj.get_side(i)
					pts = intersectLC(p1, p2, Circle(self.pos, radius))
					pt = intersect(self.pos, self.pos + self.dir*radius, p1, p2)
					if pt:
						v = Vector2(p2 - p1)
						r = (reflect(self.dir, Vector2(v.x, v.y))).normalize()
						self.dir = r
						self.on_reflect()
			elif type(obj) is Line:
				p1, p2 = obj.p1, obj.p2
				pts = intersectLC(p1, p2, Circle(self.pos, radius))
				pt = intersect(self.pos, self.pos + self.dir * radius, p1, p2)
				if pt:
					v = Vector2(p2 - p1)
					r = (reflect(self.dir, Vector2(v.x, v.y))).normalize()
					self.dir = r
					self.on_reflect()
		self.pos += self.dir * spd

	def draw(self, screen: pg.Surface):
		c = Circle(self.pos, self.r)
		c.color = self.color
		c.draw(screen)

