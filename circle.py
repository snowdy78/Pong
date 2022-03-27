import pygame as pg
from pygame import Vector2
from color import *


class Circle:
	def __init__(self, pos: Vector2 = Vector2(0, 0), r: float = 1, scale: Vector2 = Vector2(1, 1), color: Color = Color(255, 255, 255)):
		self.pos = pos
		self.r = r
		self.scale = scale
		self.color = color

	def draw(self, screen: pg.Surface):
		p = self.scale.x
		q = self.scale.y
		r = self.r
		x = self.pos.x
		y = self.pos.y
		pg.draw.ellipse(screen, self.color.get_tuple(), pg.rect.Rect((x - r * p, y - q * r, p * r * 2, q * r * 2)))
