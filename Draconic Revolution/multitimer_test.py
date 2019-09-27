# Importing Engine

import pyglet as pg
from pyglet.window import key

# Direct OpenGL commands to this window.
#platform = pg.window.get_platform()
display = pg.canvas.get_display()
screen = display.get_default_screen()
template = pg.gl.Config(alpha_size=8)
config = screen.get_best_config(template)
window = pg.window.Window(config=config)

class Disp(pg.event.EventDispatcher):
	def sig(self):
		self.dispatch_event('on_signal')

	def on_signal(self):
		A.timer.tick()
		pg.clock.tick()

class A:
	timer = pg.clock.Clock()
	ev = Disp()
	def __init__(self, a):
		self.a = a

	def inc(self, Non):
		self.a += 1

	def keep_inc(self, Non):
		self.a = 0
		A.timer.schedule_interval(self.inc, 1/100)
		while(self.a <= 10):
			A.ev.sig()
			print(self.a)
		A.timer.unschedule(self.inc)


@window.event
def on_key_press(symbol, modifiers):
	global ts

	if(symbol == key.Q):
		for t in ts:
			pg.clock.schedule_once(t.keep_inc, 1/100)

def hi(Non):
	print("aaa")

Disp.register_event_type('on_signal')
pg.clock.schedule_interval(hi, 1/100)

ts = [A(0),A(0)]

pg.app.run()
