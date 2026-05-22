import random
from asyncio import wait

#Caso esteja a ler isto, olá professora

from manim import *
import time
import math

config.assets_dir = "Images"  # folder relative to main.py
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 8
config.frame_width = 14.2222  # physical units for scene width
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


def circle_intersections(c1: Vector2D, r1: float, c2: Vector2D, r2: float):
	d = distance(c1, c2)
	a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
	h = math.sqrt(r1 ** 2 - a ** 2)

	# Point on the line between centers at distance a from c1
	mx = c1.x + a * (c2.x - c1.x) / d
	my = c1.y + a * (c2.y - c1.y) / d

	# Perpendicular offset
	dx = h * (c2.y - c1.y) / d
	dy = h * (c2.x - c1.x) / d

	p1 = Vector2D(mx + dx, my - dy)
	p2 = Vector2D(mx - dx, my + dy)
	return p1, p2

def point_to_line_distance(point: Vector2D, slope_val: float, intercept: float) -> float:
	"""
    Distância de um ponto a uma reta definida por y = slope_val*x + intercept
    (i.e., slope_val*x - y + intercept = 0)
    Fórmula: |m*px - py + b| / sqrt(m^2 + 1)
    """
	return abs(slope_val * point.x - point.y + intercept) / math.sqrt(slope_val ** 2 + 1)


def incircle_radius(
		A: Vector2D, B: Vector2D, C: Vector2D,
		incentro: Vector2D,
		slope_BC: float
) -> float:
	"""
    Raio da circunferência inscrita = distância do incentro ao lado BC.
    O lado BC tem equação: y = slope_BC * x + b_BC
    onde b_BC = B.y - slope_BC * B.x
    """
	b_BC = B.y - slope_BC * B.x
	return point_to_line_distance(incentro, slope_BC, b_BC)


def excircle_radius(
		excenter: Vector2D,
		slope_val: float,
		intercept: float
) -> float:
	"""
    Raio de uma excircunferência = distância do exincentro ao lado oposto.
    """
	return point_to_line_distance(excenter, slope_val, intercept)


	p1 = Vector2D(mx + dx, my - dy)
	p2 = Vector2D(mx - dx, my + dy)
	return p1, p2
def line_circle_intersection(m, intercept: float, center: Vector2D, radius: float):
    # y = mx + intercept into (x - cx)^2 + (y - cy)^2 = r^2
    A = 1 + m**2
    B = 2 * (m * (intercept - center.y) - center.x)
    C = center.x**2 + (intercept - center.y)**2 - radius**2

    discriminant = B**2 - 4 * A * C
    x1 = (-B + math.sqrt(discriminant)) / (2 * A)
    x2 = (-B - math.sqrt(discriminant)) / (2 * A)
    y1 = m * x1 + intercept
    y2 = m * x2 + intercept

    return Vector2D(x1, y1), Vector2D(x2, y2)
class Main(Scene):
	def construct(self):
		text1 = Text("Ola a todos").shift((0, 2.7, 0))
		axes = Axes(
			x_range=[-14.2222, 14.2222],
			x_length=14.2222,
			y_range=[-8, 8],
			y_length=8,
		)
		dot = Dot(
			axes.coords_to_point(2, 1.7, 0),
			radius=0.03,  # size
			color=RED,  # color
			fill_opacity=0
		)
		dot1 = Dot(
			axes.coords_to_point(2.9, -3, 0),
			radius=0.03,  # size
			color=GREEN,  # color
			fill_opacity=0
		)
		dot2 = Dot(
			axes.coords_to_point(-4.5, 0, 0),
			radius=0.03,  # size
			color=BLUE,  # color
			fill_opacity=0
		)
		dot3 = Dot(
			axes.coords_to_point(2, 4),
			radius=0.03,
			color=RED,
		)
		triangle = always_redraw(lambda: Polygon(
			dot.get_center(),
			dot1.get_center(),
			dot2.get_center(),
			dot.get_center(),
			stroke_color=PURPLE,
			stroke_opacity=0.5,
			fill_color=PURPLE,
			fill_opacity=0.5,
		).round_corners(radius=0.005))
		PM1 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).x,
				   mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).y,
				   0),
			radius=0.03,
			color=GRAY
		))
		PM2 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).x,
				   mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).y,
				   0),
			radius=0.03
		))
		PM3 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).x,
				   mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).y,
				   0),
			radius=0.03
		))
		# DECLIVE DO PE 1
		d1 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		f1 = lambda: foot(V2D(axes.point_to_coords(dot.get_center())), d1())
		line = always_redraw(lambda: axes.plot(
			lambda x: f1()[1] * x + f1()[0],
			color=BLUE
		))
		#DECLIVE DO PE 22
		d2 = lambda: slope(
			V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		f2 = lambda: foot(V2D(axes.point_to_coords(dot1.get_center())), d2())
		line1 = always_redraw(lambda: axes.plot(
			lambda x: f2()[1] * x + f2()[0],
			color=BLUE
		))
		#DECLIVE DO PE 3
		d3 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot.get_center()))
		)
		f3 = lambda: foot(V2D(axes.point_to_coords(dot2.get_center())), d3())
		line2 = always_redraw(lambda: axes.plot(
			lambda x: f3()[1] * x + f3()[0],
			color=BLUE
		))
		# PE 1
		p1 = lambda: intersection(
			d1(), f1()[1], d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], f1()[0]
		)
		pe1 = always_redraw(lambda: Dot(
			point = axes.coords_to_point(p1().x, p1().y, 0 ), #axes.coords_to_point
			radius = 0.03,
			color = WHITE,
		))
		altura1 = always_redraw(lambda: Line(
			start = axes.coords_to_point(p1().x, p1().y, 0 ),
			end = dot.get_center(),
			color= BLUE,
			stroke_opacity=0.3,
		))
		#PE 2
		p2 = lambda: intersection(
			d2(), f2()[1], d2() * - axes.point_to_coords(dot2.get_center())[0] + axes.point_to_coords(dot2.get_center())[1], f2()[0]
		)
		pe2 = always_redraw(lambda: Dot(
			point = axes.coords_to_point(p2().x, p2().y, 0 ),
			radius=0.03,
			color = WHITE,
		))
		altura2 = always_redraw(lambda: Line(
			start=axes.coords_to_point(p2().x, p2().y, 0 ),
			end=dot1.get_center(),
			color=BLUE,
			stroke_opacity=0.3,
		))
		#PE 3
		p3 = lambda: intersection(
			d3(), f3()[1], d3() * - axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1], f3()[0]
		)
		pe3 = always_redraw(lambda: Dot(
			point = axes.coords_to_point(p3().x, p3().y, 0 ),
			radius=0.03,
			color = WHITE,
		))
		altura3 = always_redraw(lambda: Line(
			start=axes.coords_to_point(p3().x, p3().y, 0),
			end=dot2.get_center(),
			color=BLUE,
			stroke_opacity=0.3,
		))
		ortoc = lambda: intersection(
			f1()[1], f2()[1], f1()[0], f2()[0]
		)
		ortocentro = always_redraw(lambda: Dot(
			point = axes.coords_to_point(ortoc().x, ortoc().y, 0 ),
			radius=0.03,
			color = BLUE,
		))
		med1 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot1.get_center()))
		)
		mediatriz = always_redraw(lambda: axes.plot(
			lambda x: med1()[0] * x + med1()[1],
			color=RED,
		))
		med2 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		mediatriz1 = always_redraw(lambda: axes.plot(
			lambda x: med2()[0] * x + med2()[1],
			color=RED,
		))
		circ = lambda: intersection(
			med1()[0], med2()[0], med1()[1], med2()[1]
		)
		circuncentro = always_redraw(lambda: Dot(
			point = axes.coords_to_point(circ().x, circ().y, 0 ),
			color = GREEN,
		))
		dot4 = always_redraw(lambda: Dot(
			point = (
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0 )), V2D(dot.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0 )), V2D(dot.get_center())).y, 0
					 ),
			radius = 0.03,
			color = YELLOW,
		))
		dot5 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).y, 0
			),
			radius=0.03,
			color=YELLOW,
		))
		dot6 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).y, 0
			),
			radius=0.03,
			color=YELLOW,
		))
		centro = lambda: mediumpoint(
			circ(), ortoc()
		)
		raio = lambda: distance(
			V2D(axes.coords_to_point(centro().x, centro().y, 0)),
			V2D(PM1.get_center())
		)
		circle = always_redraw(lambda: Circle(
			radius = raio(),
			color = PINK,
			stroke_opacity=0.4
		).move_to(axes.coords_to_point(centro().x, centro().y, 0)))
		center = always_redraw(lambda: Dot(
			point = axes.coords_to_point(centro().x, centro().y, 0),
			color=RED
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
			Create(PM3),
			#Create(line),
			#Create(dot3),
			#Create(axes),
			#Create(line1),
			#Create(line2),
			Create(pe1),
			Create(pe2),
			Create(pe3),
			#Create(ortocentro),
			#Create(mediatriz),
			#Create(mediatriz1),
			#Create(circuncentro),
			Create(dot4),
			Create(dot5),
			Create(dot6),
			Create(circle),
			Create(center),
			Create(altura1),
			Create(altura2),
			Create(altura3),
		)
		self.wait(1)
		for i in range(10):
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
			radius=0.03,  # size
			color=RED
					  )  # color
		dot=Dot(
			point=(2, 2, 0),
			radius=0.03,  # size
			color=RED,  # color
					  )

		dot1 = Dot(
			point=(2.4, -1.4, 0),
			radius=0.03,  # size
			color=RED,  # color
			)
		dot2 = Dot(
			point=(-3.7, 1.7, 0),
			radius=0.03,  # size
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
		img.scale(1.15)                    # resize
		img.move_to((0, 0., 0))         # center it
		          # offset position

		self.play(FadeIn(img))
		self.play(img.animate.move_to((-3, 2., 0)))
		self.wait(2)

		img1 = ImageMobject("9pcircle03.svg")
		img1.scale(1)  # resize
		img1.move_to((0, 0, 0))  # center it
		# offset position

		self.play(FadeIn(img1))
		self.play(img1.animate.move_to((3, 2.1, 0)))
		self.wait(2)
		img2 = ImageMobject("e562fa4d-b955-4b12-ae3b-e5dc94578c78")
		img2.scale(0.6)  # resize
		img2.move_to((0, 0, 0))  # center it
		# offset position

		self.play(FadeIn(img2))
		self.play(img2.animate.move_to((-3.25, -2.1, 0)))
		self.wait(2)

		img3 = ImageMobject("f5bbcb0b-d75d-4de0-99ec-43d2004d905e-removebg-preview")
		img3.scale(1.2)  # resize
		img3.move_to((0, 0, 0))  # center it
		# offset position

		self.play(FadeIn(img3))
		self.play(img3.animate.move_to((3, -2.3, 0)))
		self.wait(2)

class Amir2(Scene):
	def construct(self):
		axes = Axes(
			x_range=[-14.2222, 14.2222],
			x_length=14.2222,
			y_range=[-8, 8],
			y_length=8
		)
		dot = Dot(
			axes.coords_to_point(7, 6.5, 0),
			radius=0.03,  # size
			color=RED,  # color
			fill_opacity=0
		)
		self.play(FadeIn(dot))
		self.wait(1)
		dot1 = Dot(
			axes.coords_to_point(6.7, -7, 0),
			radius=0.03,  # size
			color=GREEN,  # color
			fill_opacity=0
		)
		self.play(FadeIn(dot1))
		self.wait(1)
		dot2 = Dot(
			axes.coords_to_point(-8.5, 0, 0),
			radius=0.03,  # size
			color=BLUE,  # color
			fill_opacity=0
		)
		self.play(FadeIn(dot2))
		self.wait(1)

		triangle = always_redraw(lambda: Polygon(
			dot.get_center(),
			dot1.get_center(),
			dot2.get_center(),
			dot.get_center(),
			stroke_color=PURPLE,
			stroke_opacity=0.5,
			fill_color=PURPLE,
			fill_opacity=0.5,
		).round_corners(radius=0.005))
		self.play(FadeIn(triangle))
		self.wait(2)

		PM1 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).x,
			       mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).y,
			       0),
			radius=0.03,
			color=GRAY
		))
		PM2 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).x,
			       mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).y,
			       0),
			radius=0.03
		))
		PM3 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).x,
			       mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).y,
			       0),
			radius=0.03
		))
		self.play(FadeIn(PM1, PM2, PM3))
		self.wait(2)
		# DECLIVE DO PE 1
		d1 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		f1 = lambda: foot(V2D(axes.point_to_coords(dot.get_center())), d1())
		line = always_redraw(lambda: axes.plot(
			lambda x: f1()[1] * x + f1()[0],
			color=BLUE
		))
		# DECLIVE DO PE 2
		d2 = lambda: slope(
			V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		f2 = lambda: foot(V2D(axes.point_to_coords(dot1.get_center())), d2())
		line1 = always_redraw(lambda: axes.plot(
			lambda x: f2()[1] * x + f2()[0],
			color=BLUE
		))
		# DECLIVE DO PE 3
		d3 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot.get_center()))
		)
		f3 = lambda: foot(V2D(axes.point_to_coords(dot2.get_center())), d3())
		line2 = always_redraw(lambda: axes.plot(
			lambda x: f3()[1] * x + f3()[0],
			color=BLUE
		))
		self.play(FadeIn(line1, line2, line))
		self.wait(3)
		self.play(FadeOut(line1, line2, line))
		p1 = lambda: intersection(
			d1(), f1()[1],
			d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], f1()[0]
		)
		pe1 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(p1().x, p1().y, 0),  # axes.coords_to_point
			radius=0.03,
			color=WHITE,
		))
		altura1 = always_redraw(lambda: Line(
			start=axes.coords_to_point(p1().x, p1().y, 0),
			end=dot.get_center(),
			color=BLUE,
			stroke_opacity=0.3,
		))
		# PE 2
		p2 = lambda: intersection(
			d2(), f2()[1],
			d2() * - axes.point_to_coords(dot2.get_center())[0] + axes.point_to_coords(dot2.get_center())[1], f2()[0]
		)
		pe2 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(p2().x, p2().y, 0),
			radius=0.03,
			color=WHITE,
		))
		altura2 = always_redraw(lambda: Line(
			start=axes.coords_to_point(p2().x, p2().y, 0),
			end=dot1.get_center(),
			color=BLUE,
			stroke_opacity=0.3,
		))
		# PE 3
		p3 = lambda: intersection(
			d3(), f3()[1],
			d3() * - axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1], f3()[0]
		)
		pe3 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(p3().x, p3().y, 0),
			radius=0.03,
			color=WHITE,
		))
		altura3 = always_redraw(lambda: Line(
			start=axes.coords_to_point(p3().x, p3().y, 0),
			end=dot2.get_center(),
			color=BLUE,
			stroke_opacity=0.3,
		))
		ortoc = lambda: intersection(
			f1()[1], f2()[1], f1()[0], f2()[0]
		)
		ortocentro = always_redraw(lambda: Dot(
			point=axes.coords_to_point(ortoc().x, ortoc().y, 0),
			radius=0.03,
			color=BLUE,
		))
		med1 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot1.get_center()))
		)
		mediatriz = always_redraw(lambda: axes.plot(
			lambda x: med1()[0] * x + med1()[1],
			color=RED,
		))
		med2 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		mediatriz1 = always_redraw(lambda: axes.plot(
			lambda x: med2()[0] * x + med2()[1],
			color=RED,
		))
		circ = lambda: intersection(
			med1()[0], med2()[0], med1()[1], med2()[1]
		)
		circuncentro = always_redraw(lambda: Dot(
			point=axes.coords_to_point(circ().x, circ().y, 0),
			color=GREEN,
		))
		dot4 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot.get_center())).y, 0
			),
			radius=0.03,
			color=YELLOW,
		))
		dot5 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).y, 0
			),
			radius=0.03,
			color=YELLOW,
		))
		dot6 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).y, 0
			),
			radius=0.03,
			color=YELLOW,
		))
		centro = lambda: mediumpoint(
			circ(), ortoc()
		)
		raio = lambda: distance(
			V2D(axes.coords_to_point(centro().x, centro().y, 0)),
			V2D(PM1.get_center())
		)
		circle = always_redraw(lambda: Circle(
			radius=raio(),
			color=PINK,
			stroke_opacity=0.4
		).move_to(axes.coords_to_point(centro().x, centro().y, 0)))
		center = always_redraw(lambda: Dot(
			point=axes.coords_to_point(centro().x, centro().y, 0),
			color=RED
		))
		# DECLIVE DO EULER
		d4 = lambda: slope(
			V2D(axes.point_to_coords(circuncentro.get_center())), V2D(axes.point_to_coords(ortocentro.get_center()))
		)
		b4 = lambda: (
				axes.point_to_coords(circuncentro.get_center())[1]
				- d4() * axes.point_to_coords(circuncentro.get_center())[0]
		)

		reta_euler = always_redraw(lambda: axes.plot(
			lambda x: d4() * x + b4(),
			color=ORANGE,
		))







		self.play(FadeIn(dot, dot1, dot2))
		self.wait(2)
		self.play(FadeIn(triangle))
		self.wait(2)
		self.play(FadeIn(PM1, PM2, PM3))
		self.wait(2)
		self.play(FadeIn(line, line1, line2, ortocentro, pe1, pe2, pe3))
		self.wait(2)
		self.play(FadeOut(line1, line, line2))
		self.wait(2)
		self.play(FadeIn(dot4, dot5, dot6))
		self.wait(2)
		self.play(FadeIn(mediatriz, mediatriz1, circuncentro))
		self.wait(2)
		self.play(FadeOut(mediatriz, mediatriz1))
		self.wait(2)
		self.play(FadeIn(center))
		self.wait(2)
		self.play(FadeIn(circle))
		self.wait(2)
		self.play(FadeIn(reta_euler))


class Amir4(Scene):
	def construct(self):
		axes = Axes(
			x_range=[-14.2222, 14.2222],
			x_length=14.2222,
			y_range=[-8, 8],
			y_length=8
		)


		dot = Dot(
			axes.coords_to_point(5, 4.5, 0),
			radius=0.03,
			color=RED,
			fill_opacity=0
		)

		dot1 = Dot(
			axes.coords_to_point(3.7, -5, 0),
			radius=0.03,
			color=GREEN,
			fill_opacity=0
		)

		dot2 = Dot(
			axes.coords_to_point(-6.5, 0, 0),
			radius=0.03,
			color=BLUE,
			fill_opacity=0
		)


		triangle = always_redraw(lambda: Polygon(
			dot.get_center(),
			dot1.get_center(),
			dot2.get_center(),
			stroke_color=PURPLE,
			stroke_opacity=0.8,
			fill_color=PURPLE,
			fill_opacity=0.4,
		).round_corners(radius=0.005))


		PM1 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).x,
				mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).y,
				0
			),
			radius=0.05,
			color=GRAY
		))

		PM2 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).x,
				mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).y,
				0
			),
			radius=0.05,
			color=GRAY
		))

		PM3 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).x,
				mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).y,
				0
			),
			radius=0.05,
			color=GRAY
		))


		d1 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())),
			V2D(axes.point_to_coords(dot2.get_center()))
		)
		d2 = lambda: slope(
			V2D(axes.point_to_coords(dot.get_center())),
			V2D(axes.point_to_coords(dot2.get_center()))
		)
		d3 = lambda: slope(
			V2D(axes.point_to_coords(dot.get_center())),
			V2D(axes.point_to_coords(dot1.get_center()))
		)


		f1 = lambda: foot(V2D(axes.point_to_coords(dot.get_center())), d1())
		f2 = lambda: foot(V2D(axes.point_to_coords(dot1.get_center())), d2())
		f3 = lambda: foot(V2D(axes.point_to_coords(dot2.get_center())), d3())

		p1 = lambda: intersection(
			d1(), f1()[1],
			d1() * (-axes.point_to_coords(dot1.get_center())[0]) + axes.point_to_coords(dot1.get_center())[1],
			f1()[0]
		)
		pe1 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(p1().x, p1().y, 0),
			radius=0.05,
			color=WHITE,
		))

		p2 = lambda: intersection(
			d2(), f2()[1],
			d2() * (-axes.point_to_coords(dot2.get_center())[0]) + axes.point_to_coords(dot2.get_center())[1],
			f2()[0]
		)
		pe2 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(p2().x, p2().y, 0),
			radius=0.05,
			color=WHITE,
		))

		p3 = lambda: intersection(
			d3(), f3()[1],
			d3() * (-axes.point_to_coords(dot.get_center())[0]) + axes.point_to_coords(dot.get_center())[1],
			f3()[0]
		)
		pe3 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(p3().x, p3().y, 0),
			radius=0.05,
			color=WHITE,
		))


		ortoc = lambda: intersection(f1()[1], f2()[1], f1()[0], f2()[0])

		ortocentro = always_redraw(lambda: Dot(
			point=axes.coords_to_point(ortoc().x, ortoc().y, 0),
			radius=0.05,
			color=BLUE,
		))


		med1 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot.get_center())),
			V2D(axes.point_to_coords(dot1.get_center()))
		)
		med2 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot1.get_center())),
			V2D(axes.point_to_coords(dot2.get_center()))
		)

		circ = lambda: intersection(med1()[0], med2()[0], med1()[1], med2()[1])

		circuncentro = always_redraw(lambda: Dot(
			point=axes.coords_to_point(circ().x, circ().y, 0),
			radius=0.05,
			color=GREEN,
		))


		dot4 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot.get_center())).y,
				0
			),
			radius=0.05, color=YELLOW,
		))
		dot5 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).y,
				0
			),
			radius=0.05, color=YELLOW,
		))
		dot6 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).y,
				0
			),
			radius=0.05, color=YELLOW,
		))

		centro9 = lambda: mediumpoint(circ(), ortoc())

		raio9 = lambda: distance(
			V2D(axes.coords_to_point(centro9().x, centro9().y, 0)),
			V2D(PM1.get_center())
		)

		circle1 = always_redraw(lambda: Circle(
			radius=raio9(),
			color=BLUE,
			stroke_opacity=0.9,
			stroke_width=2,
		).move_to(axes.coords_to_point(centro9().x, centro9().y, 0)))

		center9 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(centro9().x, centro9().y, 0),
			radius=0.05,
			color=BLUE
		))


		raio_circ = lambda: distance(
			V2D(circuncentro.get_center()),
			V2D(dot.get_center())
		)

		circle2 = always_redraw(lambda: Circle(
			radius=raio_circ(),
			color=RED,
			stroke_opacity=0.6,
			stroke_width=2,
			fill_opacity=0.0,
		).move_to(circuncentro.get_center()))


		radius_line_9 = always_redraw(lambda: Line(
			start=axes.coords_to_point(centro9().x, centro9().y, 0),
			end=axes.coords_to_point(centro9().x, centro9().y, 0) + np.array([raio9(), 0, 0]),
			color=BLUE,
			stroke_width=3,
		))


		radius_line_circ = always_redraw(lambda: Line(
			start=axes.coords_to_point(circ().x, circ().y, 0),
			end=axes.coords_to_point(circ().x, circ().y, 0) + np.array([raio_circ(), 0, 0]),
			color=RED,
			stroke_width=3,
		))


		label_r9 = always_redraw(lambda: Text(
			"r", color=WHITE, font_size=36
		).next_to(radius_line_9.get_center(), DOWN, buff=0.15))

		label_rcirc = always_redraw(lambda: Text(
			"R = 2r", color=WHITE, font_size=36
		).next_to(radius_line_circ.get_center(), UP, buff=0.15))


		a = lambda: distance(V2D(dot1.get_center()), V2D(dot2.get_center()))
		b = lambda: distance(V2D(dot.get_center()), V2D(dot2.get_center()))
		c = lambda: distance(V2D(dot.get_center()), V2D(dot1.get_center()))


		incentro_screen = lambda: Vector2D(
			(a() * dot.get_center()[0] + b() * dot1.get_center()[0] + c() * dot2.get_center()[0]) / (a() + b() + c()),
			(a() * dot.get_center()[1] + b() * dot1.get_center()[1] + c() * dot2.get_center()[1]) / (a() + b() + c()),
		)

		I = always_redraw(lambda: Dot(
			point=(incentro_screen().x, incentro_screen().y, 0),
			radius=0.06,
			color=GOLD
		))

		slope_BC_screen = lambda: slope(V2D(dot1.get_center()), V2D(dot2.get_center()))
		intercept_BC_screen = lambda: dot1.get_center()[1] - slope_BC_screen() * dot1.get_center()[0]

		raio_inscrito = lambda: point_to_line_distance(
			incentro_screen(), slope_BC_screen(), intercept_BC_screen()
		)

		incircle = always_redraw(lambda: Circle(
			radius=raio_inscrito(),
			color=RED,
			stroke_opacity=0.9,
			stroke_width=2,
		).move_to((incentro_screen().x, incentro_screen().y, 0)))


		ex1_screen = lambda: Vector2D(
			(-a() * dot.get_center()[0] + b() * dot1.get_center()[0] + c() * dot2.get_center()[0]) / (-a() + b() + c()),
			(-a() * dot.get_center()[1] + b() * dot1.get_center()[1] + c() * dot2.get_center()[1]) / (-a() + b() + c()),
		)
		ex2_screen = lambda: Vector2D(
			(a() * dot.get_center()[0] - b() * dot1.get_center()[0] + c() * dot2.get_center()[0]) / (a() - b() + c()),
			(a() * dot.get_center()[1] - b() * dot1.get_center()[1] + c() * dot2.get_center()[1]) / (a() - b() + c()),
		)
		ex3_screen = lambda: Vector2D(
			(a() * dot.get_center()[0] + b() * dot1.get_center()[0] - c() * dot2.get_center()[0]) / (a() + b() - c()),
			(a() * dot.get_center()[1] + b() * dot1.get_center()[1] - c() * dot2.get_center()[1]) / (a() + b() - c()),
		)

		E1 = always_redraw(lambda: Dot(point=(ex1_screen().x, ex1_screen().y, 0), radius=0.06, color=ORANGE))
		E2 = always_redraw(lambda: Dot(point=(ex2_screen().x, ex2_screen().y, 0), radius=0.06, color=ORANGE))
		E3 = always_redraw(lambda: Dot(point=(ex3_screen().x, ex3_screen().y, 0), radius=0.06, color=ORANGE))

		slope_AC_screen = lambda: slope(V2D(dot.get_center()), V2D(dot2.get_center()))
		intercept_AC_screen = lambda: dot.get_center()[1] - slope_AC_screen() * dot.get_center()[0]
		slope_AB_screen = lambda: slope(V2D(dot.get_center()), V2D(dot1.get_center()))
		intercept_AB_screen = lambda: dot.get_center()[1] - slope_AB_screen() * dot.get_center()[0]

		rex1 = lambda: point_to_line_distance(ex1_screen(), slope_BC_screen(), intercept_BC_screen())
		rex2 = lambda: point_to_line_distance(ex2_screen(), slope_AC_screen(), intercept_AC_screen())
		rex3 = lambda: point_to_line_distance(ex3_screen(), slope_AB_screen(), intercept_AB_screen())

		excircle1 = always_redraw(lambda: Circle(
			radius=rex1(), color=RED, stroke_opacity=0.7, stroke_width=2,
		).move_to((ex1_screen().x, ex1_screen().y, 0)))

		excircle2 = always_redraw(lambda: Circle(
			radius=rex2(), color=RED, stroke_opacity=0.7, stroke_width=2,
		).move_to((ex2_screen().x, ex2_screen().y, 0)))

		excircle3 = always_redraw(lambda: Circle(
			radius=rex3(), color=RED, stroke_opacity=0.7, stroke_width=2,
		).move_to((ex3_screen().x, ex3_screen().y, 0)))


		self.play(
			FadeIn(triangle),
			FadeIn(dot),
			FadeIn(dot1),
			FadeIn(dot2),
		)
		self.wait(1)

		self.play(
			FadeIn(circle1),
			FadeIn(center9),
			FadeIn(PM1),
			FadeIn(PM2),
			FadeIn(PM3),
			FadeIn(pe1),
			FadeIn(pe2),
			FadeIn(pe3),
			FadeIn(dot4),
			FadeIn(dot5),
			FadeIn(dot6),
		)
		self.wait(1)

		self.play(
			FadeIn(circle2),
			FadeIn(circuncentro),
		)
		self.wait(1)


		self.play(
			Create(radius_line_9),
			Create(radius_line_circ),
		)
		self.play(
			FadeIn(label_r9),
			FadeIn(label_rcirc),
		)
		self.wait(4)


		self.play(
			FadeOut(circle2),
			FadeOut(circle1),
			FadeOut(triangle),
			FadeOut(dot),
			FadeOut(dot1),
			FadeOut(dot2),
			FadeOut(PM1),
			FadeOut(PM2),
			FadeOut(PM3),
			FadeOut(pe1),
			FadeOut(pe2),
			FadeOut(pe3),
			FadeOut(dot4),
			FadeOut(dot5),
			FadeOut(dot6),
			FadeOut(center9),
			FadeOut(circuncentro),
			FadeOut(radius_line_9),
			FadeOut(radius_line_circ),
			FadeOut(label_r9),
			FadeOut(label_rcirc),
		)
		self.wait(2)


		self.play(
			FadeIn(triangle),
			FadeIn(dot),
			FadeIn(dot1),
			FadeIn(dot2),
		)
		self.wait(1)

		self.play(
			FadeIn(circle1),
			FadeIn(center9),
			FadeIn(PM1),
			FadeIn(PM2),
			FadeIn(PM3),
			FadeIn(pe1),
			FadeIn(pe2),
			FadeIn(pe3),
			FadeIn(dot4),
			FadeIn(dot5),
			FadeIn(dot6),
		)
		self.wait(1)

		self.play(
			FadeIn(I),
			FadeIn(incircle),
		)
		self.wait(1)

		self.play(
			FadeIn(E1),
			FadeIn(excircle1),
			FadeIn(E2),
			FadeIn(excircle2),
			FadeIn(E3),
			FadeIn(excircle3),
		)
		self.wait(4)
class Amir5(Scene):
	def construct(self):


		titulo = Text("Aplicações da Circunferência dos 9 Pontos", font_size=40, color=WHITE)
		titulo.to_edge(UP, buff=0.5)

		img_intro = ImageMobject("aPnAKMhPOW3kq711OYfv0ggkwBmF17K7vqhzo9IArSntJy32H3Xxc5sUOP_s9j4b1-0weOVyknYzYquE9YA_0GTsqj8GVmg5cH0hCxdZKq6p3CQuSa2zXNd7qmHz74A1plYQV5D5N37rYiCTLYEvQSE7g3l6IDKaqcphG2BKHUkarDYdRLhSLaFnMDCX_mFT")
		img_intro.scale(0.6)
		img_intro.move_to((0, -0.3, 0))

		self.play(FadeIn(titulo, img_intro))

		self.wait(3)
		self.play(FadeOut(titulo), FadeOut(img_intro))
		self.wait(1)


		titulo1 = Text("1. Computação gráfica e modelação 3D", font_size=38, color=BLUE)
		titulo1.to_edge(UP, buff=0.5)

		img1 = ImageMobject("Captura de ecrã 2026-05-21 141501")
		img1.scale(1.5)
		img1.move_to((0, -0.5, 0))

		self.play(FadeIn(titulo1))
		self.play(FadeIn(img1))
		self.wait(4)
		self.play(FadeOut(titulo1), FadeOut(img1))
		self.wait(1)


		titulo2 = Text("2. Engenharia estrutural", font_size=38, color=GREEN)
		titulo2.to_edge(UP, buff=0.5)


		img2 = ImageMobject("EJPfWqMWSVYnErwY7HN6okYfSRxQg8XpqgedaAeQMTwfgMVC851zvm8gezJq1tZyprFVUpnFcPwPUWv6yGbS6RgLPexWFwdZiuGdYUk37uDyCSFDSCf6g1nxqb0K6Aek3JcadSezqAZVSSZMrS2khlFqvlFmpdsVeQYqNpEp97fyABF5ism4XNNzf8SxthM7")
		img2.scale(0.7)
		img2.move_to((0, -0.5, 0))

		self.play(FadeIn(titulo2))
		self.play(FadeIn(img2))
		self.wait(4)
		self.play(FadeOut(titulo2), FadeOut(img2))
		self.wait(1)

		titulo3 = Text("3. GPS e triangulação", font_size=38, color=ORANGE)
		titulo3.to_edge(UP, buff=0.5)


		img3 = ImageMobject("i504981")
		img3.scale(1.3)
		img3.move_to((0, -0.5, 0))

		self.play(FadeIn(titulo3))
		self.play(FadeIn(img3))
		self.wait(4)
		self.play(FadeOut(titulo3), FadeOut(img3))
		self.wait(1)


		titulo4 = Text("4. Robótica e visão artificial", font_size=38, color=RED)
		titulo4.to_edge(UP, buff=0.5)

		img4 = ImageMobject("68e773f2f61ea8b3d65b616b_684d86745567e29449b7156c_67ed573955601cf15bc46ca6_66d17fe9693b439a2b727b6c_66cda30b83266c3f98983b82_66cda2baad76faa6ea906726_Robotics_fig4%2525252520(2)")  # ← nome do ficheiro
		img4.scale(1.1)
		img4.to_edge(DOWN, buff=0.5)

		self.play(FadeIn(titulo4))
		self.play(FadeIn(img4))
		self.wait(4)
		self.play(FadeOut(titulo4), FadeOut(img4))
		self.wait(2)
		#tetas


class Amir3(Scene):
	def construct(self):
		text1 = Text("Ola a todos").shift((0, 2.7, 0))
		axes = Axes(
			x_range=[-14.2222, 14.2222],
			x_length=14.2222,
			y_range=[-8, 8],
			y_length=8,
			tips=False,

		).set_opacity(0.5).shift((1.5, -0.5, 0)).set_z_index(-1)
		dot = Dot(
			axes.coords_to_point(2, 1.7, 0),
			radius=0.05,  # size
			color=RED,  # color
			fill_opacity=0.7
		)
		dot1 = Dot(
			axes.coords_to_point(2.9, -3, 0),
			radius=0.05,  # size
			color=GREEN,  # color
			fill_opacity=0.7
		)
		dot2 = Dot(
			axes.coords_to_point(-4.5, 0, 0),
			radius=0.05,  # size
			color=BLUE,  # color
			fill_opacity=0.7
		)
		dot3 = Dot(
			axes.coords_to_point(2, 4),
			radius=0.03,
			color=RED,
		)
		triangle = always_redraw(lambda: Polygon(
			dot.get_center(),
			dot1.get_center(),
			dot2.get_center(),
			dot.get_center(),
			stroke_color=PURPLE,
			stroke_opacity=0.5,
			fill_color=PURPLE,
			fill_opacity=0.5,
		).round_corners(radius=0.005))
		PM1 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).x,
				   mediumpoint(V2D(dot.get_center()), V2D(dot1.get_center())).y,
				   0),
			radius=0.03,
		))
		PM2 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).x,
				   mediumpoint(V2D(dot1.get_center()), V2D(dot2.get_center())).y,
				   0),
			radius=0.03
		))
		PM3 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).x,
				   mediumpoint(V2D(dot.get_center()), V2D(dot2.get_center())).y,
				   0),
			radius=0.03
		))
		# DECLIVE DO PE 1
		d1 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		f1 = lambda: foot(V2D(axes.point_to_coords(dot.get_center())), d1())
		line = always_redraw(lambda: axes.plot(
			lambda x: f1()[1] * x + f1()[0],
			color=BLUE
		))
		#DECLIVE DO PE 2
		d2 = lambda: slope(
			V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		f2 = lambda: foot(V2D(axes.point_to_coords(dot1.get_center())), d2())
		line1 = always_redraw(lambda: axes.plot(
			lambda x: f2()[1] * x + f2()[0],
			color=BLUE
		))
		#DECLIVE DO PE 3
		d3 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot.get_center()))
		)
		f3 = lambda: foot(V2D(axes.point_to_coords(dot2.get_center())), d3())
		line2 = always_redraw(lambda: axes.plot(
			lambda x: f3()[1] * x + f3()[0],
			color=BLUE
		))
		# PE 1
		p1 = lambda: intersection(
			d1(), f1()[1], d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], f1()[0]
		)
		pe1 = always_redraw(lambda: Dot(
			point = axes.coords_to_point(p1().x, p1().y, 0 ), #axes.coords_to_point
			radius = 0.03,
			color = WHITE,
		))
		altura1 = always_redraw(lambda: Line(
			start = dot.get_center(),
			end = axes.coords_to_point(p1().x, p1().y, 0 ),
			color= BLUE,
			stroke_opacity=0.3,
		))
		#PE 2
		p2 = lambda: intersection(
			d2(), f2()[1], d2() * - axes.point_to_coords(dot2.get_center())[0] + axes.point_to_coords(dot2.get_center())[1], f2()[0]
		)
		pe2 = always_redraw(lambda: Dot(
			point = axes.coords_to_point(p2().x, p2().y, 0 ),
			radius=0.03,
			color = WHITE,
		))
		altura2 = always_redraw(lambda: Line(
			start=dot1.get_center(),
			end=axes.coords_to_point(p2().x, p2().y, 0 ),
			color=BLUE,
			stroke_opacity=0.3,
		))
		#PE 3
		p3 = lambda: intersection(
			d3(), f3()[1], d3() * - axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1], f3()[0]
		)
		pe3 = always_redraw(lambda: Dot(
			point = axes.coords_to_point(p3().x, p3().y, 0 ),
			radius=0.03,
			color = WHITE,
		))
		altura3 = always_redraw(lambda: Line(
			start=dot2.get_center(),
			end=axes.coords_to_point(p3().x, p3().y, 0),
			color=BLUE,
			stroke_opacity=0.3,
		))
		ortoc = lambda: intersection(
			f1()[1], f2()[1], f1()[0], f2()[0]
		)
		ortocentro = always_redraw(lambda: Dot(
			point = axes.coords_to_point(ortoc().x, ortoc().y, 0 ),
			radius=0.03,
			color = BLUE,
		))
		med1 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot1.get_center()))
		)
		pontofixe = lambda: intersection(
			d1(), med1()[0],
			d1() * - axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], med1()[1]
		)
		pontotuff = lambda: intersection(
			d2(), med2()[0],
			d2() * - axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1], med2()[1]
		)
		mediatriz = always_redraw(lambda: Line(
			start = PM1.get_center(),
			end = axes.coords_to_point(pontofixe().x, pontofixe().y, 0 ),
			color = RED,
		))
		med2 = lambda: perpendicular_bisector(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		mediatriz1 = always_redraw(lambda: Line(
			start=PM2.get_center(),
			end=axes.coords_to_point(pontotuff().x, pontotuff().y, 0),
			color=RED,
		))
		circ = lambda: intersection(
			med1()[0], med2()[0], med1()[1], med2()[1]
		)
		circuncentro = always_redraw(lambda: Dot(
			point = axes.coords_to_point(circ().x, circ().y, 0 ),
			color = GREEN,
			radius=0.03,
		))
		dot4 = always_redraw(lambda: Dot(
			point = (
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0 )), V2D(dot.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0 )), V2D(dot.get_center())).y, 0
					 ),
			radius = 0.03,
			color = YELLOW,
		))
		dot5 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot1.get_center())).y, 0
			),
			radius=0.03,
			color=YELLOW,
		))
		dot6 = always_redraw(lambda: Dot(
			point=(
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).x,
				mediumpoint(V2D(axes.coords_to_point(ortoc().x, ortoc().y, 0)), V2D(dot2.get_center())).y, 0
			),
			radius=0.03,
			color=YELLOW,
		))
		centro = lambda: mediumpoint(
			circ(), ortoc()
		)
		raio = lambda: distance(
			V2D(axes.coords_to_point(centro().x, centro().y, 0)),
			V2D(PM1.get_center())
		)
		circle = always_redraw(lambda: Circle(
			radius = raio(),
			color = PINK,
			stroke_opacity=0.4
		).move_to(axes.coords_to_point(centro().x, centro().y, 0)))
		center = always_redraw(lambda: Dot(
			point = axes.coords_to_point(centro().x, centro().y, 0),
			color=RED
		))
		arc1 = always_redraw(lambda: Arc(
			radius = 1.5,
			start_angle = -PI / 1.4,
			angle = PI/1.8,
			arc_center = dot.get_center()
		))
		arc2 = always_redraw(lambda: Arc(
			radius=1.5,
			start_angle=PI / 3.2,
			angle=PI / 1.8,
			arc_center=dot1.get_center()
		))
		linha = always_redraw(lambda: Line(
			start = (circle_intersections(V2D(dot.get_center()), 1.5, V2D(dot1.get_center()), 1.5)[0].x,
					 circle_intersections(V2D(dot.get_center()), 1.5, V2D(dot1.get_center()), 1.5)[0].y, 0),
			end = (circle_intersections(V2D(dot.get_center()), 1.5, V2D(dot1.get_center()), 1.5)[1].x,
					 circle_intersections(V2D(dot.get_center()), 1.5, V2D(dot1.get_center()), 1.5)[1].y, 0),
		))
		arc3 = always_redraw(lambda: Arc(
			radius=2.3,
			start_angle=-PI / 1.4 - PI / 2,
			angle=PI / 1.8,
			arc_center=dot.get_center()
		))
		arc4 = always_redraw(lambda: Arc(
			radius=2.3,
			start_angle=PI / 3.2 - PI / 2,
			angle=PI / 1.8,
			arc_center=dot2.get_center()
		))
		linha2 = always_redraw(lambda: Line(
			start=(circle_intersections(V2D(dot.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[0].x,
				   circle_intersections(V2D(dot.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[0].y, 0),
			end=(circle_intersections(V2D(dot.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[1].x,
				 circle_intersections(V2D(dot.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[1].y, 0),
		))
		arc5 = always_redraw(lambda: Arc(
			radius=2.3,
			start_angle=PI / 3.2 + PI / 3.5,
			angle=PI / 1.8,
			arc_center=dot1.get_center()
		))
		arc6 = always_redraw(lambda: Arc(
			radius=2.3,
			start_angle=PI / 3.2 - PI / 2 - PI / 3.5,
			angle=PI / 1.8,
			arc_center=dot2.get_center()
		))
		linha3 = always_redraw(lambda: Line(
			start=(circle_intersections(V2D(dot1.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[0].x,
				   circle_intersections(V2D(dot1.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[0].y, 0),
			end=(circle_intersections(V2D(dot1.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[1].x,
				 circle_intersections(V2D(dot1.get_center()), 2.3, V2D(dot2.get_center()), 2.3)[1].y, 0),
		))
		arc7 = always_redraw(lambda: Arc(
			radius=4.2 * axes.get_x_unit_size(),
			start_angle=-PI/1.2,
			angle=PI / 1.8,
			arc_center=dot.get_center()
		))
		pontoaura = always_redraw(lambda: Dot(
			point = axes.coords_to_point(line_circle_intersection(d1(), d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], V2D(axes.point_to_coords(dot.get_center())), 4.2)[0].x,
					 line_circle_intersection(d1(), d1() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1], V2D(axes.point_to_coords(dot.get_center())), 4.2)[0].y
					 , 0)
		))
		pontoaura2 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(line_circle_intersection(d1(), d1() * -axes.point_to_coords(dot1.get_center())[0] +
											axes.point_to_coords(dot1.get_center())[1],
																V2D(axes.point_to_coords(dot.get_center())), 4.2)[1].x,
				   line_circle_intersection(d1(), d1() * -axes.point_to_coords(dot1.get_center())[0] +
											axes.point_to_coords(dot1.get_center())[1],
											V2D(axes.point_to_coords(dot.get_center())), 4.2)[1].y
					   , 0)
		))
		arc8 = always_redraw(lambda: Arc(
			radius = 1,
			start_angle = +PI /4,
			angle = PI / 1.8,
			arc_center = pontoaura.get_center()
		))
		arc9 = always_redraw(lambda: Arc(
			radius=1,
			start_angle= 0,
			angle=PI / 1.8,
			arc_center=pontoaura2.get_center()
		))
		###
		arc10 = always_redraw(lambda: Arc(
			radius=4.9 * axes.get_x_unit_size(),
			start_angle= PI / 3,
			angle=PI / 1.8,
			arc_center=dot1.get_center()
		))
		pontoaura3 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(line_circle_intersection(
										d2(),
										d2() * -axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1],
										V2D(axes.point_to_coords(dot1.get_center())),
										4.9)[0].x,
					   line_circle_intersection(
										d2(),
										d2() * -axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1],
										V2D(axes.point_to_coords(dot1.get_center())),
										4.9)[0].y
									   , 0)
		))
		pontoaura4 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(
				line_circle_intersection(
										 d2(),
										 d2() * -axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1],
										 V2D(axes.point_to_coords(dot1.get_center())),
										 4.9)[1].x,
				line_circle_intersection(
										 d2(),
										 d2() * -axes.point_to_coords(dot.get_center())[0] + axes.point_to_coords(dot.get_center())[1],
										 V2D(axes.point_to_coords(dot1.get_center())),
										 4.9)[1].y
				, 0)
		))
		arc11 = always_redraw(lambda: Arc(
			radius=1,
			start_angle=- PI / 1.2 ,
			angle=PI / 1.8,
			arc_center=pontoaura3.get_center()
		))
		arc12 = always_redraw(lambda: Arc(
			radius=1,
			start_angle=- PI / 1.7,
			angle=PI / 1.8,
			arc_center=pontoaura4.get_center()
		))
		arc13 = always_redraw(lambda: Arc(
			radius=7 * axes.get_x_unit_size(),
			start_angle=-PI / 3,
			angle=PI / 1.8,
			arc_center=dot2.get_center()
		))
		pontoaura5 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(line_circle_intersection(
				d3(),
				d3() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1],
				V2D(axes.point_to_coords(dot2.get_center())),
				7)[0].x,
				   line_circle_intersection(
					   d3(),
					   d3() * -axes.point_to_coords(dot1.get_center())[0] +
					   axes.point_to_coords(dot1.get_center())[1],
					   V2D(axes.point_to_coords(dot2.get_center())),
					   7)[0].y
				   , 0)
		))
		pontoaura6 = always_redraw(lambda: Dot(
			point=axes.coords_to_point(
				line_circle_intersection(
					d3(),
					d3() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1],
					V2D(axes.point_to_coords(dot2.get_center())),
					7)[1].x,
				line_circle_intersection(
					d3(),
					d3() * -axes.point_to_coords(dot1.get_center())[0] + axes.point_to_coords(dot1.get_center())[1],
					V2D(axes.point_to_coords(dot2.get_center())),
					7)[1].y
				, 0)
		))
		arc14 = always_redraw(lambda: Arc(
			radius=1.2,
			start_angle=+ PI / 2,
			angle=PI / 1.8,
			arc_center=pontoaura5.get_center()
		))
		arc15 = always_redraw(lambda: Arc(
			radius=1.2,
			start_angle=- PI,
			angle=PI / 1.8,
			arc_center=pontoaura6.get_center()
		))
		arc16 = always_redraw(lambda: Arc(
			radius=0.2,
			start_angle = PI/7,
			angle=PI / 1.8,
			arc_center=ortocentro.get_center()
		))
		arc17 = always_redraw(lambda: Arc(
			radius=0.2,
			start_angle = -PI / 1.15,
			angle=PI / 1.8,
			arc_center=dot.get_center()
		))
		linha4 = always_redraw(lambda: Line(
			start=(circle_intersections(V2D(ortocentro.get_center()), 0.2, V2D(dot.get_center()), 0.2)[0].x,
				   circle_intersections(V2D(ortocentro.get_center()), 0.2, V2D(dot.get_center()), 0.2)[0].y, 0),
			end=(circle_intersections(V2D(ortocentro.get_center()), 0.2, V2D(dot.get_center()), 0.2)[1].x,
				 circle_intersections(V2D(ortocentro.get_center()), 0.2, V2D(dot.get_center()), 0.2)[1].y, 0),
		))
		arc18 = always_redraw(lambda: Arc(
			radius=1.4,
			start_angle=-PI * 1.2 + PI / 2,
			angle=PI / 1.8,
			arc_center=ortocentro.get_center()
		))
		arc19 = always_redraw(lambda: Arc(
			radius=1.4,
			start_angle=-PI / 5 + PI / 2,
			angle=PI / 1.8,
			arc_center=dot1.get_center()
		))
		linha5 = always_redraw(lambda: Line(
			start=(circle_intersections(V2D(ortocentro.get_center()), 1.4, V2D(dot1.get_center()), 1.4)[0].x,
				   circle_intersections(V2D(ortocentro.get_center()), 1.4, V2D(dot1.get_center()), 1.4)[0].y, 0),
			end=(circle_intersections(V2D(ortocentro.get_center()), 1.4, V2D(dot1.get_center()), 1.4)[1].x,
				 circle_intersections(V2D(ortocentro.get_center()), 1.4, V2D(dot1.get_center()), 1.4)[1].y, 0),
		))
		arc20 = always_redraw(lambda: Arc(
			radius=2,
			start_angle=-PI * 1.2,
			angle=PI / 1.8,
			arc_center=ortocentro.get_center()
		))
		arc21 = always_redraw(lambda: Arc(
			radius=2,
			start_angle=-PI / 5,
			angle=PI / 1.8,
			arc_center=dot2.get_center()
		))
		linha6 = always_redraw(lambda: Line(
			start=(circle_intersections(V2D(ortocentro.get_center()), 2, V2D(dot2.get_center()), 2)[0].x,
				   circle_intersections(V2D(ortocentro.get_center()), 2, V2D(dot2.get_center()), 2)[0].y, 0),
			end=(circle_intersections(V2D(ortocentro.get_center()), 2, V2D(dot2.get_center()), 2)[1].x,
				 circle_intersections(V2D(ortocentro.get_center()), 2, V2D(dot2.get_center()), 2)[1].y, 0),
		))
		arc22 = always_redraw(lambda: Arc(
			radius=1,
			start_angle=-PI,
			angle=PI / 1.8,
			arc_center=ortocentro.get_center()
		))
		arc23 = always_redraw(lambda: Arc(
			radius=1,
			start_angle=0,
			angle=PI / 1.8,
			arc_center=circuncentro.get_center()
		))
		linha7 = always_redraw(lambda: Line(
			start=(circle_intersections(V2D(ortocentro.get_center()), 1, V2D(circuncentro.get_center()), 1)[0].x,
				   circle_intersections(V2D(ortocentro.get_center()), 1, V2D(circuncentro.get_center()), 1)[0].y, 0),
			end=(circle_intersections(V2D(ortocentro.get_center()), 1, V2D(circuncentro.get_center()), 1)[1].x,
				 circle_intersections(V2D(ortocentro.get_center()), 1, V2D(circuncentro.get_center()), 1)[1].y, 0),
		))
		linha8 = always_redraw(lambda: Line(
			start = ortocentro.get_center(),
			end = circuncentro.get_center()
		))
		lapis = ImageMobject("lapis-removebg-preview")
		lapis.scale(0.4)
		lapis.rotate(PI/2)
		compasso = ImageMobject("compasso")
		compasso.set(width = 1.5*2)
		compasso.move_to((-5, -3, 3))
		compasso.set_z_index(5)
		texttrespontos = Text(
			"Defenir três pontos no plano.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		texttriangulo = Text(
			"Desenhar o triângulo que conecta os três pontos.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textpm = Text(
			"Desenhar os pontos médios dos vértices do triângulo e o circuncentro.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textoaltura = Text(
			"Desenhar as alturas do triângulo e marcar "
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textointer = Text(
			"os pontos de interseção das mesmas com as arestas do triangulo.."
		).shift((-3, 2.4, 0)).scale(0.5).to_edge(LEFT)
		textortc = Text(
			"Marcar o ortocentro na interseção das alturas do triangulo.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textpm1 = Text(
			"Marcar os pontos médios entre o ortocentro e os vértices do triangulo.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textcentro = Text(
			"Definir o centro da circunferência de 9 pontos.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textcircunferencia = Text(
			"Desenahr a circunferência de 9 pontos.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		self.play(
			Write(texttrespontos),
		)
		self.play(FadeIn(lapis))
		self.play(FadeIn(compasso))
		self.wait(0.3)
		self.play(Create(axes))
		self.wait(1)
		self.play(
			lapis.animate.move_to(dot.get_center()).rotate(PI/3)
		)
		self.play(Create(dot))
		self.wait(0.3)
		self.play(
			lapis.animate.move_to(dot1.get_center()).rotate(PI / 3)
		)
		self.play(Create(dot1))
		self.wait(0.3)
		self.play(
			lapis.animate.move_to(dot2.get_center()).rotate(PI / 3)
		)
		self.play(Create(dot2))
		self.wait(2)
		self.play(
			Unwrite(texttrespontos),
			Write(texttriangulo)
				  )
		self.wait(0.5)
		self.play(
			lapis.animate.move_to(dot.get_center()).rotate(-PI / 3)
		)
		self.play(
			Write(triangle, run_time=7, rate_func=linear),
			Succession(
				ApplyMethod(lapis.move_to, dot1.get_center()),
				ApplyMethod(lapis.move_to, dot2.get_center()),
				ApplyMethod(lapis.move_to, dot.get_center()),
			)
			)
		self.play(
			Unwrite(texttriangulo),
			Write(textpm)
		)
		self.wait(2)
		self.play(compasso.animate.move_to(dot.get_center()).rotate(-PI / 1.4))
		duration = 1  # match your desired Create duration
		speed = (PI / 1.77) / duration

		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc1), run_time=duration, rate_func=linear)
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(dot1.get_center()).rotate(+PI / 1.4 - PI / 1.8 + PI / 3.2))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(
			Create(arc2),
			run_time=duration,
			rate_func=linear,
		)
		compasso.clear_updaters()
		self.play(lapis.animate.move_to(linha.get_start()).rotate(-PI / 3))
		self.play(
			Create(linha),
			lapis.animate.move_to(linha.get_end()).rotate(PI / 3)
		)
		self.play(lapis.animate.move_to(PM1.get_center()).rotate(-PI / 3))
		self.play(Create(PM1),
				  FadeOut(arc1, arc2, linha))
		self.wait(0.5)
		self.play(compasso.animate.move_to(dot.get_center()).rotate(- PI / 1.8 - PI / 3.2 - PI / 1.4 - PI / 2).scale( (2.3*2) / (1.5*2)))

		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc3,
						 rate_func=linear,
						 run_time=duration,))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(dot2.get_center()).rotate(-PI / 1.8 +PI / 1.4 + PI / 2 + PI / 3.2 - PI / 2))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc4,
						 rate_func=linear,
						run_time=duration,))
		compasso.clear_updaters()
		self.play(lapis.animate.move_to(linha2.get_start()).rotate(-PI / 3))
		self.play(Create(linha2),
						 lapis.animate.move_to(linha2.get_end()).rotate(PI / 3))
		self.play(lapis.animate.move_to(PM3.get_center()).rotate(-PI / 3))
		self.play(Create(PM3),
				  FadeOut(arc3, arc4))
		self.wait(0.5)
		self.play(compasso.animate.move_to(dot1.get_center()).rotate(-PI / 3.2 + PI / 2 - PI / 1.8 + PI / 3.2 + PI / 3.5))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc5,
						 rate_func=linear,
						 run_time=duration, ))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(dot2.get_center()).rotate(- 1.8 -PI / 3.2 - PI / 3.5 + (PI / 3.2 - PI / 2 - PI / 3.5)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc6,
						 rate_func=linear,
						 run_time=duration, ))
		compasso.clear_updaters()
		self.play(lapis.animate.move_to(linha3.get_start()).rotate(-PI / 3))
		self.play(Create(linha3),
				  lapis.animate.move_to(linha3.get_end()).rotate(PI / 3))
		self.play(lapis.animate.move_to(PM2.get_center()).rotate(-PI / 3))
		self.play(Create(PM2),
				  FadeOut(arc6, arc5,))
		self.play(lapis.animate.move_to(circuncentro.get_center()).rotate(-PI / 3))
		self.play(Create(circuncentro),
				  FadeOut(linha2, linha3))
		###
		self.wait(2)
		self.play(
			Unwrite(textpm),
			Write(textoaltura),
			Write(textointer),
		)
		self.play(compasso.animate.move_to(dot.get_center()).rotate( - PI / 1.8  - (PI / 3.2 - PI / 2 - PI / 3.5) * 1.03 -PI/1.2).scale((4.2 * axes.get_x_unit_size() * 2) / (2.3 * 2)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc7,
						 rate_func=linear,
						 run_time=duration, ))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(pontoaura.get_center())
			.rotate(- PI / 1.8 + PI / 1.2 + PI /4)
			.scale(2 / (4.2 * axes.get_x_unit_size() * 2)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc8,
						 rate_func=linear,
						 run_time=duration, ))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(pontoaura2.get_center())
				  .rotate(- PI / 1.8 - PI /4))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc9,
						 rate_func=linear,
						 run_time=duration, ))
		compasso.clear_updaters()
		self.play(lapis.animate.move_to(dot.get_center()).rotate(PI / -4))
		self.play(
			Create(altura1),
			lapis.animate.move_to(axes.coords_to_point(p1().x, p1().y, 0 )).rotate(PI / 4),
			FadeOut(arc7, arc8, arc9)
		)
		self.wait(0.3)
		self.play(compasso.animate.move_to(dot1.get_center())
				  .rotate(- PI / 1.8 + PI / 3)
				  .scale(4.9 * axes.get_x_unit_size() * 2 / 2))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc10,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(pontoaura3.get_center())
				  .rotate(- PI / 1.8 - PI / 3 - PI / 1.2)
				  .scale( 2 / 4.9 * axes.get_x_unit_size() * 2))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc11,
						 rate_func = linear,
						 run_time = duration,))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(pontoaura4.get_center())
				  .rotate(- PI / 1.8 + PI / 1.2 - PI / 1.7))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc12,
						 rate_func = linear,
						 run_time = duration,))
		compasso.clear_updaters()
		self.play(lapis.animate.move_to(dot1.get_center()).rotate(PI / -4))
		self.play(
			Create(altura2),
			lapis.animate.move_to(axes.coords_to_point(p2().x, p2().y, 0)).rotate(PI / 4),
			FadeOut(arc10, arc11, arc12)
		)
		self.wait(0.3)
		self.play(compasso.animate.move_to(dot2.get_center())
				  .rotate(- PI / 1.8 + PI / 1.7 -PI / 3)
				  .scale(7 * axes.get_x_unit_size() * 2 / 2))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc13,
						 rate_func=linear,
						 run_time=duration, ))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(pontoaura5.get_center())
				  .rotate(- PI / 1.8 + PI / 3 + PI / 2)
				  .scale(1.2*2/7 * axes.get_x_unit_size() * 2))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc14,
						 rate_func = linear,
						 run_time = duration,))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(pontoaura6.get_center())
				  .rotate(- PI / 1.8 - PI / 2 + PI))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc15,
						 rate_func = linear,
						 run_time = duration,))
		compasso.clear_updaters()
		self.play(lapis.animate.move_to(dot2.get_center()).rotate(PI / -4))
		self.play(
			Create(altura3),
			lapis.animate.move_to(axes.coords_to_point(p3().x, p3().y, 0)).rotate(PI / 4),
			FadeOut(arc13, arc14, arc15)
		)
		self.wait(0.3)
		self.play(
			lapis.animate.move_to(pe1.get_center()).rotate(PI / 3)
		)
		self.play(Create(pe1))
		self.wait(0.3)
		self.play(
			lapis.animate.move_to(pe2.get_center()).rotate(PI / 3)
		)
		self.play(Create(pe2))
		self.wait(0.3)
		self.play(
			lapis.animate.move_to(pe3.get_center()).rotate(PI / 3)
		)
		self.play(Create(pe3))
		self.wait(2)
		self.play(
			Unwrite(textoaltura),
			Unwrite(textointer),
			Write(textortc)
		)
		self.wait(0.5)
		self.play(
			lapis.animate.move_to(ortocentro.get_center()).rotate(PI / 3)
		)
		self.play(
			Create(ortocentro)
		)
		self.wait(2)
		self.play(
			Unwrite(textortc),
			Write(textpm1)
		)
		self.wait(0.5)
		self.play(compasso.animate.move_to(ortocentro.get_center())
				  .rotate(- PI / 1.8 - PI + PI/7)
				  .scale((0.2 * 2) / (1.2 * 2)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc16,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(dot.get_center())
				  .rotate(- PI / 1.8 - PI / 7 -PI / 1.15))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc17,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(
			lapis.animate.move_to(linha4.get_start()).rotate(PI / 3)
		)
		self.play(Create(linha4),
		lapis.animate.move_to(linha4.get_end()).rotate(PI / -3)
				  )
		self.play(
			lapis.animate.move_to(dot4.get_center()).rotate(PI / 3)
		)
		self.play(Create(dot4),
				  FadeOut(arc16, arc17, linha4))
		self.wait(0.3)
		self.play(compasso.animate.move_to(ortocentro.get_center())
				  .rotate(- PI / 1.8 + PI / 1.15 + (-PI * 1.2 + PI / 2))
				  .scale((1.4 * 2) / (0.2 * 2)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc18,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(dot1.get_center())
				  .rotate(- PI / 1.8 - (-PI * 1.2 + PI / 2) + (-PI / 5 + PI / 2)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc19,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(
			lapis.animate.move_to(linha5.get_start()).rotate(PI / 3)
		)
		self.play(Create(linha5),
				  lapis.animate.move_to(linha5.get_end()).rotate(PI / -3))
		self.play(
			lapis.animate.move_to(dot5.get_center()).rotate(PI / 3)
		)
		self.play(Create(dot5),
				  FadeOut(arc18, arc19, linha5))
		self.wait(0.3)
		self.play(compasso.animate.move_to(ortocentro.get_center())
				  .rotate(- PI / 1.8 - (-PI / 5 + PI / 2) -PI * 1.2)
				  .scale((2 * 2) / (1.4 * 2)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc20,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(dot2.get_center())
				  .rotate(- PI / 1.8 + PI * 1.2 - PI / 5))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc21,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(
			lapis.animate.move_to(linha6.get_start()).rotate(PI / 3)
		)
		self.play(Create(linha6),
				  lapis.animate.move_to(linha6.get_end()).rotate(PI / -3))
		self.play(
			lapis.animate.move_to(dot6.get_center()).rotate(PI / 3)
		)
		self.play(Create(dot6),
						 FadeOut(arc21, arc20, linha6))
		self.wait(2)
		self.play(
			Unwrite(textpm1),
			Write(textcentro),
		)
		self.play(compasso.animate.move_to(ortocentro.get_center())
				  .rotate(- PI / 1.8 + PI / 5 - PI)
				  .scale((1 * 2) / (2 * 2)))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc22,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(compasso.animate.move_to(circuncentro.get_center())
				  .rotate(- PI / 1.8 + PI ))
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(arc23,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.play(
			lapis.animate.move_to(linha7.get_start()).rotate(PI / 3)
		)
		self.play(Create(linha7),
				  lapis.animate.move_to(linha7.get_end()).rotate(PI / -3))
		self.play(
			lapis.animate.move_to(linha8.get_start()).rotate(PI / 3)
		)
		self.play(Create(linha8),
				  lapis.animate.move_to(linha8.get_end()).rotate(PI / -3))
		self.play(lapis.animate.move_to(center.get_center()).rotate(PI / 3))
		self.play(Create(center),
				  FadeOut(arc22, arc23, linha7, linha8))
		self.play(
			Unwrite(textcentro),
			Write(textcircunferencia)
		)
		self.play(compasso.animate.move_to(center.get_center())
				  .rotate(- PI / 1.8)
				  .scale( (raio() * 2) / (1 * 2)))
		speed = 2 * PI
		compasso.add_updater(lambda mob, dt: mob.rotate(dt * speed))
		self.play(Create(circle,
						rate_func = linear,
						run_time = duration,
				))
		compasso.clear_updaters()
		self.wait(0.5)
		self.play(lapis.animate.move_to((-3, 0, 0)))
		self.play(compasso.animate.move_to((-2, 0, 0)))

class Amir6(Scene):
    def construct(self):
        img_intro = ImageMobject("Manim_icon.svg")
        img_intro.scale(1)
        img_intro.move_to((0, 0, 0))

        self.play(FadeIn(img_intro))
        self.wait(2)


        self.play(
            img_intro.animate
            .scale(0.4)
            .move_to((-5.5, 2.5, 0)),
            run_time=1.5
        )

        self.wait(2)

        bloco = Code(
            code_string="""
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
    d = math.sqrt((a.x-b.x)2 + (a.y-b.y)2)
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
    return m, b"""
                 ,
            language="Python",

            background="window",

        )
        bloco.scale(0.5)
        bloco.shift((3, 0, 0))

        for linha in bloco.code_lines:
            self.play(AddTextLetterByLetter(linha, time_per_char=0.07))

        self.wait(2)
        img1_intro = ImageMobject("Captura de ecrã 2026-05-21 231455")
        img1_intro.scale(0.5)
        img1_intro.move_to((-3.7, -1, 0))

        self.play(FadeIn(img1_intro))


        self.wait(2)
		#latest