import random

from manim import *
import time
import math

config.assets_dir = "Images"  # folder relative to main.py
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 14.0  # physical units for scene height
config.frame_width = 14.0  # physical units for scene width
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
	d = (a.y - b.y)/(a.x - b.x)
	return d
def distance(a: Vector2D, b: Vector2D):
	d = math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)
	return d
def mediumpoint(a: Vector2D, b: Vector2D):
	d=Vector2D((a.x+b.x)/2,(a.y+b.y)/2)
	return d
def foot(ponto: Vector2D, declive):
	d=-1/declive
	b=-(d * ponto.x) + ponto.y
	return b,d#pee
def perpendicular_bisector(a: Vector2D, b: Vector2D):
	mx = (a.x + b.x) / 2
	my = (a.y + b.y) / 2
	m = -(b.x - a.x) / (b.y - a.y)
	b = my - m * mx
	return m, b
def intersection(m1, m2, b1, b2):
	x=(b2-b1)/(m1-m2)
	y=m1*((b2-b1)/(m1-m2))+b1
	return Vector2D(x,y)


class Main(Scene):
	def construct(self):
		text1 = Text("Ola a todos").shift((0, 2.7, 0))
		axes = Axes(x_range=[-8.888, 8.888], y_range=[-5, 5])
		dot = Dot(
			axes.coords_to_point(2, 1.7, 0),
			radius=0.1,  # size
			color=RED,  # color
		)
		dot1 = Dot(
			axes.coords_to_point(2.9, -1.7, 0),
			radius=0.1,  # size
			color=GREEN,  # color
		)
		dot2 = Dot(
			axes.coords_to_point(-3.7, 0.9, 0),
			radius=0.1,  # size
			color=BLUE,  # color
		)
		dot3 = Dot(
			axes.coords_to_point(2, 4),
			radius=0.1,
			color=RED,
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
		d1 = lambda: slope(V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot2.get_center())))
		f1 = lambda: foot(V2D(axes.point_to_coords(dot.get_center())), d1())
		line = always_redraw(lambda: axes.plot(
			lambda x: f1()[1] * x + f1()[0], color=BLUE
		))
		d2 = lambda: slope(V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot2.get_center())))
		f2 = lambda: foot(V2D(axes.point_to_coords(dot1.get_center())), d2())
		line1 = always_redraw(lambda: axes.plot(
			lambda x: f2()[1] * x + f2()[0], color=BLUE
		))
		d3 = lambda: slope(V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot.get_center())))
		f3 = lambda: foot(V2D(axes.point_to_coords(dot2.get_center())), d3())
		line2 = always_redraw(lambda: axes.plot(
			lambda x: f3()[1] * x + f3()[0], color=BLUE
		))
		line3 = always_redraw(lambda: axes.plot(
			lambda x: d1() * x + d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1]
		))
		p1 = lambda: intersection(
			d1(), f1()[1], d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], f1()[0])
		pe1 = always_redraw(lambda: Dot(
			point = axes.coords_to_point(p1().x, p1().y, 0 ), #axes.coords_to_point
			radius = 0.1,
			color = WHITE,
		))
		print(d1(), f1()[1], d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], f1()[0])
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
			Create(PM3),
			Create(line),
			Create(dot3),
			Create(axes),
			Create(line1),
			Create(line2),
			Create(line3),
			Create(pe1)
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

class Amir(Scene):
	def construct(self):
		line1 = Line(
			start=(-6, 0, 0),
			end=(6, 0, 0),
			color=WHITE)

		line2=Line(
			start=(0, -6, 0),
			end=(0, 6, 0),
			color=WHITE)


		self.play(
			Create(line1),
				Create(line2),
		)

		img = ImageMobject("image-removebg-preview")
		img.scale(0.6)                    # resize
		img.move_to((0, 0., 0))         # center it
		          # offset position

		self.play(FadeIn(img))
		self.play(img.animate.move_to((-3, 2., 0)))
		self.wait(2)

		img1 = ImageMobject("9pcircle03.svg")
		img1.scale(0.44)  # resize
		img1.move_to((0, 0, 0))  # center it
		# offset position

		self.play(FadeIn(img1))
		self.play(img1.animate.move_to((3, 2.1, 0)))
		self.wait(2)
		img2 = ImageMobject("314c33e6-839c-4ffe-88f4-381e14f789b1-removebg-preview")
		img2.scale(0.6)  # resize
		img2.move_to((0, 0, 0))  # center it
		# offset position

		self.play(FadeIn(img2))
		self.play(img2.animate.move_to((-3, -2.3, 0)))
		self.wait(2)

		img3 = ImageMobject("f5bbcb0b-d75d-4de0-99ec-43d2004d905e-removebg-preview")
		img3.scale(0.6)  # resize
		img3.move_to((0, 0, 0))  # center it
		# offset position

		self.play(FadeIn(img3))
		self.play(img3.animate.move_to((3, -2.3, 0)))
		self.wait(2)

