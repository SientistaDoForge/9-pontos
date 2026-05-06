import random

from manim import *
import time
import math


config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 7.0  # physical units for scene height
config.frame_width = 12.0  # physical units for scene width
config.frame_rate = 60
class Vector2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y
def V2D(p):
	return Vector2D(p[0], p[1])
def randPos(dot, ammount):
	x = dot[0] + random.uniform(-ammount, ammount)
	y = dot[1] + random.uniform(-ammount, ammount)
	return x, y, dot[2]
def slope(a: Vector2D, b: Vector2D):
	d = (a.x - b.x)/(a.y - b.y)
	return d
def distance(a: Vector2D, b: Vector2D):
	d = math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)
	return d
def mediumpoint(a: Vector2D, b: Vector2D):
	d=Vector2D((a.x+b.x)/2,(a.y+b.y)/2)
	return d
def foot(ponto: Vector2D, declive):
	d=-1/declive
	b=d-(-1/declive)
	return b,d
def perpendicular_bisector(a: Vector2D, b: Vector2D):
	mx = (a.x + b.x) / 2
	my = (a.y + b.y) / 2
	m = -(b.x - a.x) / (b.y - a.y)
	b = my - m * mx
	return m, b
def intersection(m1, m2, b1, b2):
	x=b2-b1/(m1-m2)
	y=m1*(b2-b1/(m1-m2))+b1
	return Vector2D(x,y)


class Main(Scene):
	def construct(self):
		text1 = Text("Ola a todos").shift((0, 2.7, 0))
		dot = Dot(
			point=(2, 1.7, 0),
			radius=0.1,  # size
			color=RED,  # color
		)
		dot1 = Dot(
			point=(2.9, -1.7, 0),
			radius=0.1,  # size
			color=RED,  # color
		)
		dot2 = Dot(
			point=(-3.7, 0.9, 0),
			radius=0.1,  # size
			color=RED,  # color
		)
		triangle = always_redraw(lambda: Polygon(
			dot.get_center(),
			dot1.get_center(),
			dot2.get_center(),
			color = WHITE
		))
		PM1 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).x,
				   mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).y,
				   0),
		))
		PM2 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).x,
				   mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).y,
				   0),
		))
		PM3 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).x,
				   mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).y,
				   0),
		))

		# Step 1
		self.play(Write(text1))
		self.wait(6.7)
		self.play(
			Create(dot),
			Create(dot1),
			Create(dot2),
			Create(triangle),
			Create(PM1),
			Create(PM2),
			Create(PM3)
		)
		self.wait(1)
		self.play(
			dot.animate.move_to(randPos(dot1.get_center(), 0.5)),
			dot1.animate.move_to(randPos(dot2.get_center(), 0.5)),
			dot2.animate.move_to(randPos(dot.get_center(), 0.5)),
		)
		self.wait(1)
		self.play(
			dot.animate.move_to(randPos(dot1.get_center(), 0.5)),
			dot1.animate.move_to(randPos(dot2.get_center(), 0.5)),
			dot2.animate.move_to(randPos(dot.get_center(), 0.5)),
		)
		self.wait(1)
		self.play(
			dot.animate.move_to(randPos(dot1.get_center(), 0.5)),
			dot1.animate.move_to(randPos(dot2.get_center(), 0.5)),
			dot2.animate.move_to(randPos(dot.get_center(), 0.5)),
		)
		self.wait(1)
		self.play(
			dot.animate.move_to(randPos(dot1.get_center(), 0.5)),
			dot1.animate.move_to(randPos(dot2.get_center(), 0.5)),
			dot2.animate.move_to(randPos(dot.get_center(), 0.5)),
		)
		self.wait(1)
		self.play(
			dot.animate.move_to(randPos(dot1.get_center(), 0.5)),
			dot1.animate.move_to(randPos(dot2.get_center(), 0.5)),
			dot2.animate.move_to(randPos(dot.get_center(), 0.5)),
		)
		self.wait(1)

class PM(Scene):
	def construct(self):
		dot0 = Dot(
			point=(2, 2, 0),
			radius=0.1,  # size
			color=RED
					  )  # color
		dot=Dot(
			point=(2, 2, 0),
			radius=0.1,  # size
			color=RED,  # color
					  )

		dot1 = Dot(
			point=(2.4, -1.4, 0),
			radius=0.1,  # size
			color=RED,  # color
			)
		dot2 = Dot(
			point=(-3.7, 1.7, 0),
			radius=0.1,  # size
			color=RED,  # color
			 )
		pontoM1=always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).x,
				   mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).y,
				   0),
			))

