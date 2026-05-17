import random
from asyncio import wait

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

class Amir2(Scene):
	def construct(self):
		axes = Axes(
			x_range=[-12, 12],  # wider to match the wider frame
			y_range=[-7, 7],
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
			radius=0.03
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
		line = always_redraw(lambda: DashedVMobject(
			axes.plot(lambda x: f1()[1] * x + f1()[0], color=BLUE),
			num_dashes=100,
			dashed_ratio=0.5,
		))
		# DECLIVE DO PE 2
		d2 = lambda: slope(
			V2D(axes.point_to_coords(dot.get_center())), V2D(axes.point_to_coords(dot2.get_center()))
		)
		f2 = lambda: foot(V2D(axes.point_to_coords(dot1.get_center())), d2())
		line1 = always_redraw(lambda: axes.plot(
			lambda x: f2()[1] * x + f2()[0], color=BLUE
		))
		# DECLIVE DO PE 3
		d3 = lambda: slope(
			V2D(axes.point_to_coords(dot1.get_center())), V2D(axes.point_to_coords(dot.get_center()))
		)
		f3 = lambda: foot(V2D(axes.point_to_coords(dot2.get_center())), d3())
		line2 = always_redraw(lambda: axes.plot(
			lambda x: f3()[1] * x + f3()[0], color=BLUE
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
		self.play(FadeIn(pe1, pe2, pe3))
		self.wait(2)

		ortoc = lambda: intersection(
			f1()[1], f2()[1], f1()[0], f2()[0]
		)
		ortocentro = always_redraw(lambda: Dot(
			point=axes.coords_to_point(ortoc().x, ortoc().y, 0),
			radius=0.03,
			color=GREEN,
		))
		self.play(FadeIn(ortocentro))
		self.wait(2)

		PM4 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot.get_center()), V2D(ortocentro.get_center())).x,
			       mediumpoint(V2D(dot.get_center()), V2D(ortocentro.get_center())).y,
			       0),
			radius=0.03
		))
		PM5 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot1.get_center()), V2D(ortocentro.get_center())).x,
			       mediumpoint(V2D(dot1.get_center()), V2D(ortocentro.get_center())).y,
			       0),
			radius=0.03
		))
		PM6 = always_redraw(lambda: Dot(
			point=(mediumpoint(V2D(dot2.get_center()), V2D(ortocentro.get_center())).x,
			       mediumpoint(V2D(dot2.get_center()), V2D(ortocentro.get_center())).y,
			       0),
			radius=0.03
		))
		self.play(FadeIn(PM4, PM5, PM6))
		m = lambda: perpendicular_bisector(V2D(dot1.get_center()),  V2D(dot2.get_center()))
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
		texttrespontos = Text(
			"Defenir três pontos no plano.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		texttriangulo = Text(
			"Desenhar o triângulo que conecta os três pontos.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textpm = Text(
			"Desenhar os pontos médios dos vértices do triângulo.."
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textoaltura = Text(
			"Desenhar as alturas do triângulo"
		).shift((-3, 3, 0)).scale(0.5).to_edge(LEFT)
		textointer = Text(
			"e marcar os pontos de interseção das mesmas com o triangulo.."
		).shift((-3, 2.6, 0)).scale(0.5).to_edge(LEFT)
		self.play(
			Write(texttrespontos),
		)
		self.wait(0.3)
		self.play(Create(axes))
		self.wait(1)
		self.play(Create(dot))
		self.wait(0.3)
		self.play(Create(dot1))
		self.wait(0.3)
		self.play(Create(dot2))
		self.wait(2)
		self.play(
			Unwrite(texttrespontos),
			Write(texttriangulo)
				  )
		self.wait(0.5)
		self.play(Write(triangle), run_time=4, rate_func=linear)
		self.play(
			Unwrite(texttriangulo),
			Write(textpm)
		)
		self.wait(2)
		self.play(Create(PM1))
		self.wait(0.5)
		self.play(Create(PM2))
		self.wait(0.5)
		self.play(Create(PM3))
		self.wait(2)
		self.play(
			Unwrite(textpm),
			Write(textoaltura),
			Write(textointer),
		)
		self.play(Create(altura1))
		self.wait(0.5)
		self.play(Create(altura2))
		self.wait(0.5)
		self.play(Create(altura3))
		self.wait(0.5)
		self.play(Create(pe1))
		self.wait(0.5)
		self.play(Create(pe2))
		self.wait(0.5)
		self.play(Create(pe3))