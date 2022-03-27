import pygame as pg
from pygame import Vector2
from color import *
from math import *


class Line:
	def __init__(self, p1, p2, color: Color = Color(255, 255, 255)):
		self.p1 = p1
		self.p2 = p2
		self.color = color

	def length(self):
		return sqrt((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2)

	def Ax(self):
		return self.p1.y - self.p2.y

	def By(self):
		return self.p2.x - self.p1.x

	def C(self):
		return self.p1.y*self.p2.x - self.p2.y*self.p1.x

	def draw(self, screen):
		pg.draw.line(screen, self.color.get_tuple(), self.p1, self.p2)
