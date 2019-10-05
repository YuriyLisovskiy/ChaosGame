from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt


class Canvas(QWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(None, flags=Qt.WindowFlags())
		self._points_to_draw = []
		self._initial_point_handler = kwargs.get('initial_point_handler', None)
		if self._initial_point_handler is None:
			raise ValueError('initial_point_handler is not defined')

	def paintEvent(self, paint_event):
		painter = QPainter(self)
		pen = QPen()
		pen.setWidth(5)
		painter.setPen(pen)
		for point in self._points_to_draw:
			painter.drawPoint(point)

	def mouseReleaseEvent(self, cursor_event):
		initial_point = self._initial_point_handler(cursor_event.pos())
		if initial_point is not None:
			self._points_to_draw.clear()
			self._points_to_draw.append(cursor_event.pos())
			self.update()

	def set_points(self, points):
		if points is not None:
			self._points_to_draw = points
			self.update()

	def clean(self):
		self.set_points([])
