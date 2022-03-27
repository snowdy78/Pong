import pygame as pg
from pygame import Vector2
from color import *
from math import floor


class Text:
	def __init__(self, text: str, char_size: int):
		self.pos = Vector2(0, 0)
		self.char_size = char_size
		self.font = pg.font.Font(None, char_size)
		self.color = Color(255, 255, 255)
		self.bg_color = Color(0, 0, 0, 0)
		self.content = text

	def set_color(self, color: Color):
		self.color = color

	def set_background_color(self, color: Color):
		self.bg_color = color

	def set_font(self, filepath: str):
		self.font = pg.font.Font(str, self.char_size)

	def set_char_size(self, size):
		self.char_size = size
		self.font = pg.font.Font(None, self.char_size)

	def set_position(self, pos: Vector2):
		self.pos = pos

	def set_text(self, text: str):
		self.content = text

	def draw(self, screen: pg.Surface):
		txt = self.font.render(self.content, True, self.color.get_tuple(), self.bg_color.get_tuple())
		screen.blit(txt, (floor(self.pos.x), floor(self.pos.y)))
