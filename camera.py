import pygame as pg
from pygame import Vector2
from math import floor, cos, sin, acos, asin, pi
from line import *
from circle import *
from rect import *
from emath import *


class Camera:
	def __init__(self, spawn_pos: Vector2, direction: Vector2, line_count: int, line_length: float, fov: float):
		self.llen = line_length
		self.pos = spawn_pos
		self.dir = direction.normalize()
		self.lcount = line_count
		self.fov = fov
		self.speed = 5

	def get_angle(self):
		d = self.dir
		a = acos(d.x)/(pi/180)
		return 360 - a if d.y < 0 else a

	def get_line_angle(self, n: int):
		fov = self.fov
		count = self.lcount
		delta = fov/count
		return (self.get_angle() - fov/2 + n*delta)*pi/180

	def move(self):
		if pg.key.get_pressed()[pg.K_w]:
			self.pos += self.speed * self.dir
		if pg.key.get_pressed()[pg.K_s]:
			self.pos -= self.speed * self.dir
		if pg.key.get_pressed()[pg.K_d]:
			self.pos += self.speed * perp(self.dir)
		if pg.key.get_pressed()[pg.K_a]:
			self.pos -= self.speed * perp(self.dir)

	def draw(self, screen, lines: tuple):
		pos = self.pos
		fov = self.fov
		lcount = self.lcount
		len = self.llen
		dir = self.dir
		delta = fov/lcount
		for i in range(lcount):
			a = self.get_line_angle(i)
			l = Line(pos, pos + len*Vector2(cos(a), sin(a)))
			for line in lines:
				pt = intersect(l.p1, l.p2, line.p1, line.p2)
				if pt:
					l.p2 = pt
					rd = reflect(l.p2 - l.p1, line.p2 - line.p1)
					rlen = max(len - (l.p2 - l.p1).length(), 0)
					rl = Line(pt, pt + rlen*rd)
					rl.draw(screen)
			l.draw(screen)
		c = Circle(self.pos, 25)
		c.draw(screen)