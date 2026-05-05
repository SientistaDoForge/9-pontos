from manim import *
import time


config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 7.0  # physical units for scene height
config.frame_width = 12.0  # physical units for scene width
config.frame_rate = 60


class Main(Scene):
	def construct(self):
		text1 = Text("Ola a todos").shift(UP)
		dot = Dot(
			point=(2, 2, 0),
			radius=0.1,  # size
			color=RED,  # color
		)

		# Step 1
		self.play(Write(text1))
		time.sleep(2)
		self.play(Create(dot))


#gonçaloide