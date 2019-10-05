import random

from PyQt5.QtCore import QPoint


class FigureBase:

	def __init__(self, canvas_w, canvas_h, segment_div=2, edges_names=None):
		self._edges = self._get_edges(canvas_w, canvas_h)
		self._segment_div = segment_div
		if edges_names is None:
			raise ValueError('edges_names is not set')
		self._edges_names = edges_names

	@staticmethod
	def _get_edges(w, h):
		return {}

	def _rand_edge(self):
		return random.choice(self._edges_names)

	@staticmethod
	def _calc_one_nth(p1, p2, n):
		delta_x = (p2[0] - p1[0]) / n
		delta_y = (p2[1] - p1[1]) / n
		return (
			p1[0] + delta_x,
			p1[1] + delta_y
		)

	def _calc_point(self, p1, p2):
		return self._calc_one_nth(p1, p2, self._segment_div)

	def calc_points(self, initial, n):
		points = [QPoint(initial[0], initial[1])]
		current_point = initial
		for _ in range(n):
			edge = self._edges[self._rand_edge()]
			new_point = self._calc_point(current_point, edge)
			points.append(QPoint(new_point[0], new_point[1]))
			current_point = new_point
		return points


class Triangle(FigureBase):

	def __init__(self, canvas_w, canvas_h, segment_div=2):
		super().__init__(canvas_w, canvas_h, segment_div, '123')

	@staticmethod
	def _get_edges(w, h):
		return {
			'1': (0, h),
			'2': (w / 2, 0),
			'3': (w, h)
		}


class Square(FigureBase):

	def __init__(self, canvas_w, canvas_h, segment_div=2):
		super().__init__(canvas_w, canvas_h, segment_div, '1234')

	@staticmethod
	def _get_edges(w, h):
		return {
			'1': (0, h),
			'2': (0, 0),
			'3': (w, 0),
			'4': (w, h)
		}


class Diamond(FigureBase):

	def __init__(self, canvas_w, canvas_h, segment_div=2):
		super().__init__(canvas_w, canvas_h, segment_div, '1234')

	@staticmethod
	def _get_edges(w, h):
		return {
			'1': (0, h / 2),
			'2': (w / 2, 0),
			'3': (w, h / 2),
			'4': (w / 2, h)
		}
