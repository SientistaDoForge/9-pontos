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
def slope(a = Vector2D, b = Vector2D):
	d = (a.x - b.x)/(a.y - b.y)
	return d
def distance(a, b):
	d = math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)
	return d
def bosta(teste1):
	pass
class Main(Scene):
	def construct(self):
		text1 = Text("Ola a todos").shift((0, 2.7, 0))
		dot = Dot(
			point=(2, 2, 0),
			radius=0.1,  # size
			color=RED,  # color
		)
		dot1 = Dot(
			point=(2, -1, 0),
			radius=0.1,  # size
			color=RED,  # color
		)
		dot2 = Dot(
			point=(-3, 2, 0),
			radius=0.1,  # size
			color=RED,  # color
		)


		# Step 1
		self.play(Write(text1))
		self.wait(6.7)
		self.play(Create(dot))
		self.play(Create(dot1))
		self.play(Create(dot2))


