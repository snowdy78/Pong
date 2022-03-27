import pygame as pg
from pygame import Vector2
from rect import Rectangle
from circle import Circle
from math import sqrt, sin, cos, acos, asin, pi


def dot(u: Vector2, v: Vector2):
	return u.x * v.x + u.y * v.y


def set_limit(x: float, minimum : float, maximum : float):
	return min(max(minimum, x), maximum)


def rot(v: Vector2):
	v = Vector2(v).normalize()
	a = acos(v.x)/(pi/180)
	return 360 - a if v.y < 0 else a


def perp(v:Vector2):
	return Vector2(v.y, -v.x).normalize()


def reflect(v: Vector2, u: Vector2):
	"""
	:param v: Vector to reflect
	:param u: Vector from reflect
	:return: reflected Vector2
	"""
	return (2 * u * dot(u, v) / dot(u, u) - v).normalize()


def intersectRL(p1, p2, p3, p4):
	x1 = p1.x
	x2 = p2.x
	x3 = p3.x
	x4 = p4.x
	y1 = p1.y
	y2 = p2.y
	y3 = p3.y
	y4 = p4.y
	d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
	if d == 0:
		return
	t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
	u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / d
	if t > 0:
		return Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def intersect(p1, p2, p3, p4):
	x1 = p1.x
	x2 = p2.x
	x3 = p3.x
	x4 = p4.x
	y1 = p1.y
	y2 = p2.y
	y3 = p3.y
	y4 = p4.y
	d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
	if d == 0:
		return
	t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
	u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / d
	if 0 < t < 1 and 0 < u < 1:
		return Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def count_pointsLC(a, b, c, elps: Circle):
	p = elps.scale.x
	q = elps.scale.y
	r = elps.r
	xc = elps.pos.x
	yc = elps.pos.y
	H = a**2 * p**2 + b**2 * q**2
	if H == 0:
		return
	D = (c - b * yc) * (2 * a * xc - c + b * yc) + r ** 2 * H - a ** 2 * xc ** 2
	kx = - a * c * p ** 2 - b ** 2 * xc * q ** 2 + a * b * yc * p ** 2
	ky = - b * c * q ** 2 - a ** 2 * yc * p ** 2 + a * b * xc * q ** 2
	if D > 0:
		X1 = (-kx + b * p * q * sqrt(D)) / H
		X2 = (-kx - b * p * q * sqrt(D)) / H
		Y1 = (-ky - a * p * q * sqrt(D)) / H
		Y2 = (-ky + a * p * q * sqrt(D)) / H
		return Vector2(X1, Y1), Vector2(X2, Y2)
	if D == 0:
		X = -kx / H
		Y = -ky / H
		return Vector2(X, Y),


def Belongs(x, m, n):
	return m <= x <= n or n <= x <= m


def pointOnLine(p: Vector2, p1: Vector2, p2: Vector2) -> bool:
	return Belongs(p.y, p1.y, p2.y) and Belongs(p.x, p1.x, p2.x)


def pointsOnLine(pts, p1, p2):
	for p in pts:
		if p:
			if pointOnLine(p, p1, p2):
				yield p


def intersectLC(p1, p2, circle: Circle):
	x2 = p2.x
	x1 = p1.x
	y2 = p2.y
	y1 = p1.y
	a = y1 - y2
	b = x2 - x1
	c = y1 * b + x1 * a
	pts = count_pointsLC(a, b, c, circle)
	if pts:
		return tuple(pointsOnLine(pts, p1, p2))


def intersectRC(rect: Rectangle, circle: Circle):
	pts = list()
	for i in range(4):
		p1, p2 = rect.get_side(i)
		s = intersectLC(p1, p2, circle)
		if s:
			for p in s:
				pts.append(p)
	return pts


def nearest(p1, p2, pts: list) -> Vector2:
	while None in pts:
		pts.remove(None)
	npts = list()
	lengths = list()
	for u in pts:
		if pointOnLine(u, p1, p2):
			npts.append(u)
			lengths.append((p1 - u).length)
	if not lengths:
		return p2
	min_value = min(lengths)
	for i, j in zip(range(len(lengths)), range(len(npts))):
		if min_value == lengths[i]:
			return npts[j]


def inside(v: Vector2, rect: Rectangle):
	x = v.x
	y = v.y
	w = rect.size.x
	h = rect.size.y
	x1 = rect.pos.x
	y1 = rect.pos.y
	return Belongs(x, x1 + w/2, x1 - w/2) and Belongs(y, y1 + h/2, y1 - h/2)
