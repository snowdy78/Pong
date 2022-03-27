import pygame as pg
from pygame import Vector2
from color import *
from rect import *
from emath import *


class Button:
	def __init__(self, pos: Vector2, size: Vector2, char_size: int = 30, content: str = ""):
		self.frame_color = Color(0, 0, 0, 0)
		self.bg_color = Color(255, 255, 255)
		self.color = Color(0, 0, 0)
		self.pos = pos
		self.size = size
		self.content = content
		self.char_size = char_size
		self.frame_size = 0
		self.before_clicked = False
		self.clicked = False
		self.pressed = False
		self.intersect = False

	def wait_for(self, before):
		mpos = Vector2(pg.mouse.get_pos())
		mstates = pg.mouse.get_pressed(3)
		if inside(mpos, Rectangle(self.pos, self.size)):
			self.intersect = True
			if before[0] and not mstates[1]:
				self.pressed = True
			elif not before[0] and mstates[1]:
				self.clicked = True
				self.pressed = False
			else:
				self.clicked = False
				self.pressed = False
		else:
			self.intersect = False
			self.pressed = False
			self.clicked = False

	def draw(self, screen: pg.Surface):
		p = self.pos
		s = self.size
		fs = self.frame_size
		rect = Rectangle(p, s)
		rect.color = self.bg_color
		rect.draw(screen)
		if fs > 0:
			frame1 = Rectangle(Vector2(p.x + (s.x - fs) / 2, p.y), Vector2(fs, s.y))
			frame2 = Rectangle(Vector2(p.x - (s.x - fs) / 2, p.y), Vector2(fs, s.y))
			frame3 = Rectangle(Vector2(p.x, p.y + (s.y - fs) / 2), Vector2(s.x, fs))
			frame4 = Rectangle(Vector2(p.x, p.y - (s.y - fs) / 2), Vector2(s.x, fs))
			frames = [frame1, frame2, frame3, frame4]
			for frame in frames:
				frame.color = self.frame_color
				frame.draw(screen)
		font = pg.font.Font(None, self.char_size)
		text = font.render(self.content, True, self.color.get_tuple(), self.bg_color.get_tuple())
		screen.blit(text, (floor(self.pos.x - s.x / 3), floor(self.pos.y - s.y / 4)))
