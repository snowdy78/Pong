import pygame as pg
from pygame import Vector2


class Color:
	def __init__(self, r: int, g: int, b: int, a: int = 255):
		assert 0 <= r <= 255, "Color param r needs to be less than 256 and more than 0"
		assert 0 <= g <= 255, "Color param g needs to be less than 256 and more than 0"
		assert 0 <= b <= 255, "Color param b needs to be less than 256 and more than 0"
		assert 0 <= a <= 255, "Color param a needs to be less than 256 and more than 0"
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def __add__(self, c):
		return Color((self.r + c.r)/2, (self.g + c.g)/2, (self.b + c.b)/2, (self.a + c.a)/2)
	def get_tuple(self):
		return self.r, self.g, self.b, self.a

