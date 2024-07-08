from engine import *


class AnimationFrame:
	def __init__(self, state: str, speed: float, frames: list[pygame.Surface]):
		self.state = state
		self.speed = speed
		self.frames = frames

		self.index = 0

	def reset(self):
		self.index = 0

	def get(self):
		self.index += 1
		if self.index >= len(self.frames):
			self.index = 0

		return self.frames[self.index]

	def __str__(self):
		return f"State: {self.state}"


class Animator:
	def __init__(self):
		self.frames: dict[str, dict[str, AnimationFrame]] = {}
		self.curr_frame: AnimationFrame = None
		self.frame_index = 0

	def add(self, dir: str, state: str, images: list[pygame.Surface], speed: float):
		length = len(images)
		speed = speed / 10
		frames = []

		for i in np.arange(0, length, speed):
			frames.append(images[int(i)])

		if not dir in self.frames:
			self.frames.update({ dir: {} })

		self.frames[dir].update({
				state: AnimationFrame(state, speed, frames)
		})

	def switch(self, dir: str, state: str):
		if self.curr_frame:
			if self.curr_frame.state == state:
				return

		self.curr_frame = self.frames[dir][state]
		self.curr_frame.reset()

	def get(self):
		return self.curr_frame.get()

