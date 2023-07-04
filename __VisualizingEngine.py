from __future__ import annotations

from sys import argv
from time import sleep

from PyQt5.QtCore import QRect, QRunnable, pyqtSlot, QThreadPool, QIODevice
from PyQt5.QtGui import QColor, QPen, QBrush, QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QAction, \
    QToolBar, QPushButton, QColorDialog

from typing import Union, Callable, TypeVar
from collections import deque


Virtual_Array = TypeVar("Virtual_Array")

app: QApplication = QApplication(argv)  # PyQt application that runs the code.

app.setStyle("Fusion")  # Style of the tool bar, and its widgets.

Color = Union[tuple[int, int, int], QColor]  # Color type used by the classes.

_resolution: list[int, int] = [app.primaryScreen().size().width(),
                               app.primaryScreen().size().height()]  # Resolution of the display in use.

_UPDATER: bool = False  # Update counter used by ticker.


def ticker(func: Callable) -> None:
    """Updates the display every other modification"""

    global _UPDATER
    func() if _UPDATER else ...
    _UPDATER = not _UPDATER


class Bar(QRect):
    """Bar class that is responsible for handling comparisons between elements of the array"""
    def __init__(self, value: int, index: int, width: int, is_separated: bool, is_positive: bool) -> None:
        """Initializes a QRect object using the appropriate coordinates and dimensions, based on the provided values.
           Gives the bar its actual value, and draws it on the canvas, WITHOUT UPDATING THE SCREEN.
        """

        if not value:
            value += 1

        super().__init__(index * (width + is_separated), _resolution[1] - int(value), width - is_separated, int(value)) \
            if is_positive else \
            super().__init__(index * (width + is_separated),
                             _resolution[1] // 2 - (int(value) if 0 < int(value) else 0), width - is_separated,
                             abs(value))

        self.val: int = value

    def __eq__(self, other: Union[Bar, int]) -> bool:
        """Equality operation between a bar and another bar, or an int"""

        return self.val == (other.val if isinstance(other, Bar) else other)

    def __ne__(self, other: Union[Bar, int]) -> bool:
        """Non-equality operation between a bar and another bar, or an int"""

        return self.val != (other.val if isinstance(other, Bar) else other)

    def __lt__(self, other: Union[Bar, int]) -> bool:
        """Less-than operation between a bar and another bar, or an int"""

        return self.val < (other.val if isinstance(other, Bar) else other)

    def __gt__(self, other: Union[Bar, int]) -> bool:
        """Greater-than operation between a bar and another bar, or an int"""

        return self.val > (other.val if isinstance(other, Bar) else other)

    def __le__(self, other: Union[Bar, int]) -> bool:
        """Less-than-or-equal operation between a bar and another bar, or an int"""

        return self.val <= (other.val if isinstance(other, Bar) else other)

    def __ge__(self, other: Union[Bar, int]) -> bool:
        """Greater-than-or-equal operation between a bar and another bar, or an int"""

        return self.val >= (other.val if isinstance(other, Bar) else other)

    def __add__(self, other: Union[Bar, int]) -> int:
        """Addition operation between a bar and another bar, or an int"""

        return self.val + (other.val if isinstance(other, Bar) else other)

    def __radd__(self, other: int) -> int:
        """Addition operation between an int and a bar"""

        return self + other

    def __sub__(self, other: Union[Bar, int]) -> int:
        """Subtraction operation between a bar and another bar, or an int"""

        return self.val - (other.val if isinstance(other, Bar) else other)

    def __rsub__(self, other: int) -> int:
        """Subtraction operation between an int and a bar"""

        return other - self.val

    def __mul__(self, other: Union[int, Bar]) -> int:
        """Multiplication operation between a bar and another bar, or an int"""

        return self.val * (other.val if isinstance(other, Bar) else other)

    def __rmul__(self, other: int) -> int:
        """Multiplication operation between an int and a bar"""

        return other * self.val

    def __truediv__(self, other: Union[Bar, int]) -> float:
        """Division operation between a bar and another bar, or an int"""

        return self.val / (other.val if isinstance(other, Bar) else other)

    def __rtruediv__(self, other: int) -> float:
        """Division operation between an int and a bar"""

        return other / self.val

    def __floordiv__(self, other: Union[Bar, int]) -> int:
        """Integer-Division operation between a bar and another bar, or an int"""

        return self.val // (other.val if isinstance(other, Bar) else other)

    def __rfloordiv__(self, other: int) -> int:
        """Integer-Division operation between an int and a bar"""

        return other // self.val

    def __mod__(self, other: Union[Bar, int]) -> int:
        """Modulo operation between a bar and another bar, or an int"""

        return self.val % (other.val if isinstance(other, Bar) else other)

    def __rmod__(self, other: int) -> int:
        """Modulo operation between an int and a bar"""

        return other % self.val

    def __pow__(self, power: Union[Bar, int], modulo=None) -> int:
        """Exponentiation operation between a bar and another bar, or an int"""

        return self.val ** (power.val if isinstance(power, Bar) else power)

    def __rpow__(self, other: int) -> int:
        """Exponentiation operation between an int and a bar"""

        return other ** self.val

    def __abs__(self) -> int:
        """Returns the absolute value of self.val"""

        return abs(self.val)

    def __floor__(self) -> int:
        """Returns the floor of self.val"""

        return self.val.__floor__()

    def __hash__(self) -> int:
        """Hashes self.val"""

        return hash(self.val)

    def __bool__(self) -> bool:
        """Bool of self.val"""

        return bool(self.val)

    def __int__(self) -> int:
        """Returns self.val as an integer"""

        return self.val

    def __float__(self) -> float:
        """Returns self.val as a float"""

        return float(self.val)

    def __str__(self) -> str:
        """Returns the string representation of QRect"""

        return super().__str__()


class ThreadedTask(QRunnable):
    """Class responsible for multi-threading of tasks"""

    def __init__(self, parent, func: Callable, *args, **kwargs) -> None:
        super(ThreadedTask, self).__init__()
        self.func: Callable = func
        self.args: list = list(args)  # Args to be given to the threaded function.
        self.kwargs: dict = kwargs  # Keyword Args to be given to the threaded function.
        self.parent: Virtual_Array = parent  # VisualArray that is used to determine when to pause the thread.

    @pyqtSlot()
    def run(self) -> None:
        """Function that is called once the thread is started by the thread pool of the visual array"""

        while not self.parent.running:
            app.processEvents()

        """This try-statement is used to make sure that cache collisions are inconsequential. 
        These collisions occur once the sorting algorithm is paused and then the size is changed."""

        try:
            self.func(*self.args, **self.kwargs)

        except IndexError:
            return


class MainWindow(QMainWindow):
    """This class is responsible for handling the visualization of the different elements of the visual array"""

    def __init__(self, color: Color, bar_color: Color, access_color: Color,
                 selection_color: Color, bar_width: int, is_separated: bool,
                 only_positive: bool, no_toolBar: bool, delay: float) -> None:
        super().__init__()

        if not no_toolBar:  # Does not have any effect in the app.
            self.tool_bar: QToolBar = QToolBar("")

            self.tool_bar.setFixedSize(_resolution[0], 21)

            self.tool_bar.setMovable(False)

            self.tool_bar.setFont(QFont("Monaco", 10, QFont.Monospace))

            _resolution[1] -= 20

        """Other attributes"""

        self.label: QLabel = QLabel()  # Label of the MainWindow objects

        self.canvas: QPixmap = QPixmap(_resolution[0], _resolution[1])  # Canvas used to display the elements on.

        self.thread_pool: QThreadPool = QThreadPool()  # Thread pool responsible for handling threads.

        self.label.setPixmap(self.canvas)

        self.setCentralWidget(self.label)  # Centers the canvas.

        self.bar_width: int = bar_width  # Bar width of the canvas.

        self.is_separated: bool = is_separated  # Indicates whether the bars are separated or not.

        self.only_positive: bool = only_positive  # Indicates whether the array contains only positive values.

        self.cache: deque = deque()  # Cache used to store access bars.

        self.delay: float = delay  # Artificial delay to slow down the sorting.

        """Color attributes"""

        self.color_wheel: QColorDialog = QColorDialog()

        self.color: QColor = QColor(*color)

        self.access_color: QColor = QColor(*access_color)

        self.selection_color: QColor = QColor(*selection_color)

        self.bar_color: QColor = QColor(*bar_color)

    def bar_at(self, value: Union[Bar, int], index: int) -> Bar:
        """Erases the contents at the given index.
        Creates and loads a bar object of value := value at the given index"""

        return self.load_bar(Bar(int(value), index, self.bar_width, self.is_separated, self.only_positive))

    def nu_fill(self, q_rect: Union[QRect, list, tuple], color: QColor) -> None:
        """Fills the provided QRect object with the given color"""

        if isinstance(q_rect, list) or isinstance(q_rect, tuple):
            q_rect: QRect = QRect(*q_rect)

        painter: QPainter = QPainter(self.label.pixmap())
        painter.setPen(QPen(color))
        painter.setBrush(QBrush(color))
        painter.drawRect(q_rect)
        painter.end()

    def load_background(self) -> None:
        """Loads the background"""

        self.nu_fill((0, 0, _resolution[0], _resolution[1]), self.color)

    def load_bar(self, bar: Bar) -> Bar:
        """Draws the given bar"""

        self.nu_fill((bar.x(), 0, self.bar_width, _resolution[1]), self.color)
        self.nu_fill(bar, self.bar_color)
        return bar

    def process_cache(self) -> None:
        self.bar_at(self._bar_objects[(i := self.cache.popleft())], i)

    def clear_cache(self) -> None:
        [self.bar_at(self._bar_objects[(i := self.cache.pop())], i) for _ in range(len(self.cache))]
        self.update()

    def select(self, index: int) -> None:
        """Marks the index by selection color"""

        self.nu_fill(self._bar_objects[index], self.selection_color)

    def _real_threaded_fill(self, index: int, color: Color) -> None:
        """Actual function that changes the color of a bar"""

        self.nu_fill(self._bar_objects[index], color)

        sleep(self.delay)

        self.cache.append(index)

    def threaded_fill(self, index: int, color: Color) -> None:
        """Creates a thread to change the color of the bar to self.access color for self.delay seconds"""

        self.thread_pool.tryStart(ThreadedTask(self, self._real_threaded_fill, index, color))

    def threaded_update(self) -> None:
        """Creates a thread that updates the screen"""

        self.thread_pool.tryStart(ThreadedTask(self, self.update))

    def update(self) -> None:
        """Updates the screen"""

        super().update()
        app.processEvents()

    def create_button(self, function: Callable, tip: str, title: str,
                      separate: bool = True, push: bool = False,
                      size: tuple[int, int] = None) -> Union[QPushButton, QAction]:
        """Creates a button with given parameters."""

        button: Union[QPushButton, QAction] = QPushButton(title) if push else QAction(title, self)
        button.pressed.connect(function) if push else button.triggered.connect(function)
        button.setToolTip(tip)
        self.tool_bar.addSeparator() if separate else ...
        button.setFixedSize(len(title) + 2, 13) if push else ...
        button.setFixedSize(*size) if size else ...

        self.tool_bar.addAction(button) if isinstance(button, QAction) else self.tool_bar.addWidget(button)

        return button
