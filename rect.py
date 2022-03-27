import pygame as pg
from pygame import Vector2
from color import *
from math import floor, cos, sin, pi, sqrt


class Rectangle:
	def __init__(self, p: Vector2 = Vector2(0, 0), s: Vector2 = Vector2(1, 1), color: Color = Color(255, 255, 255)):
		self.size = Vector2(s.x, s.y)
		self.pos = Vector2(p.x, p.y)
		self.color = color

	def get_side(self, n: int):
		w = self.size.x
		h = self.size.y
		x = self.pos.x
		y = self.pos.y
		alpha = pi * (2 * n - 1) / 4
		beta = pi * (2 * n + 1) / 4
		u1 = w / sqrt(2) * cos(alpha)
		v1 = h / sqrt(2) * sin(alpha)
		u2 = w / sqrt(2) * cos(beta)
		v2 = h / sqrt(2) * sin(beta)
		return Vector2(floor(x + u1), floor(y + v1)), Vector2(floor(x + u2), floor(y + v2))

	def get_point_count(self):
		return 4

	def draw(self, screen: pg.Surface):
		x = self.pos.x
		y = self.pos.y
		w = self.size.x
		h = self.size.y
		pg.draw.rect(screen, self.color.get_tuple(), (floor(x - w / 2), floor(y - h / 2), floor(w), floor(h)))
