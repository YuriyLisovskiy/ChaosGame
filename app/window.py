from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import (
	QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, QThreadPool, QRegExp

from app.settings import APP_MIN_WIDTH, APP_MIN_HEIGHT, APP_NAME, APP_FONT
from app.canvas import Canvas
from app.widgets import QPushButton
from app.utility import Worker

from app.core.figure import Triangle, Square, Diamond


class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__(None, Qt.WindowFlags())

		self.window().setWindowTitle(APP_NAME)
		self.setMinimumWidth(APP_MIN_WIDTH)
		self.setMinimumHeight(APP_MIN_HEIGHT)

		self.thread_pool = QThreadPool()

		self._initial_point = None
		self._drown_points = None
		self._canvas = Canvas(initial_point_handler=self._initial_point_handler)

		self._btn_draw = QPushButton(self.tr('Draw'), 90, 30, self._draw_points)
		self._btn_draw.setEnabled(False)

		self._btn_reset = QPushButton(self.tr('Reset'), 90, 30, self._reset_canvas)
		self._btn_reset.setEnabled(False)

		self._btn_save = QPushButton(self.tr('Save'), 90, 30, self._save_canvas)
		self._btn_save.setEnabled(False)

		self._points_count_line_edit = QLineEdit()
		self._segment_div_line_edit = QLineEdit()

		main_widget = self.init_main_widget()
		self.setCentralWidget(main_widget)

		# self.setup_navigation_menu()
		self.setFont(QFont('SansSerif', APP_FONT))

	def _reset_canvas(self):
		self._initial_point = None
		self._drown_points = None
		self._canvas.clean()
		self._btn_draw.setEnabled(False)
		self._btn_reset.setEnabled(False)
		self._btn_save.setEnabled(False)

	def _save_canvas(self):
		# TODO:
		print('Canvas is saved')

	def _draw_points(self):
		worker = Worker(self._draw_points_fn)
		worker.signals.error.connect(self._popup_err)
		worker.signals.param_success.connect(self._draw_points_finished)
		self.thread_pool.start(worker)

	def _draw_points_finished(self, points):
		self._drown_points = points
		self._canvas.set_points(points)
		self._btn_save.setEnabled(True)

	def _draw_points_fn(self):
		triangle = Triangle(
			self._canvas.width(),
			self._canvas.height(),
			int(self._segment_div_line_edit.text())
		)
		return triangle.calc_points(
			(self._initial_point.x(), self._initial_point.y()),
			int(self._points_count_line_edit.text())
		)

	def _initial_point_handler(self, point):
		if self._initial_point is None:
			self._initial_point = point
			self._btn_draw.setEnabled(True)
			self._btn_reset.setEnabled(True)
			return point
		return None

	def _add_input_field(self, parent, title, default=None, regex=None):
		widget = QWidget(self, flags=self.windowFlags())
		layout = QVBoxLayout(widget)
		layout.addWidget(QLabel(title), 0, Qt.AlignLeft)
		line_edit = QLineEdit()
		if default is not None:
			line_edit.setText(str(default))
		line_edit.setAlignment(Qt.AlignHCenter)
		if regex is not None:
			line_edit.setValidator(QRegExpValidator(QRegExp(regex), line_edit))
			line_edit.textChanged.connect(self._inputs_changed)
		layout.addWidget(line_edit, 0, Qt.AlignLeft)
		parent.addWidget(widget, 0, Qt.AlignHCenter)
		return line_edit

	def init_main_widget(self):
		layout = QVBoxLayout()

		# noinspection PyArgumentList
		layout.addWidget(self._canvas)

		container = QWidget(self, flags=self.windowFlags())
		container.setStyleSheet('background-color: lightgray;')
		container.setFixedHeight(100)

		tools = QHBoxLayout(container)

		self._points_count_line_edit = self._add_input_field(tools, 'Points count:', 100000, '[1-9]+[0-9]*')
		self._segment_div_line_edit = self._add_input_field(tools, 'Segment divisor:', 2, '[1-9]+[0-9]*')

		tools.addWidget(self._btn_draw, 0, Qt.AlignHCenter)
		tools.addWidget(self._btn_reset, 0, Qt.AlignHCenter)
		tools.addWidget(self._btn_save, 0, Qt.AlignHCenter)

		# noinspection PyArgumentList
		layout.addWidget(container)

		widget = QWidget(flags=self.windowFlags())
		widget.setLayout(layout)
		return widget

	@staticmethod
	def _empty(inp):
		return len(inp.text()) == 0

	def _inputs_changed(self):
		if self._empty(self._segment_div_line_edit) or self._empty(self._points_count_line_edit) or self._initial_point is None:
			self._btn_draw.setEnabled(False)
		else:
			self._btn_draw.setEnabled(True)

	def _popup_err(self, err):
		err_msg = 'Input data error\nCheck inputs'
		if err is not None:
			err_msg = err[1]
		msg_box = QMessageBox()
		msg_box.warning(self, 'Input data error', err_msg, QMessageBox.Ok)
		self._btn_draw.setEnabled(True)
