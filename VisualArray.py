from __future__ import annotations

from __vimports import Bar, Color, MainWindow, Qt, SortingAlgorithm, Union, _TWR_FACTORS, \
    ticker, _resolution, app, shuffle, rand_array, QAction, QSlider, QMenu, \
    QPushButton, QFont, bubble_sort, insertion_sort, gnome_sort, quick_sort, selection_sort, \
    shaker_sort, comb_sort, brick_sort, heap_sort, intro_sort, shell_sort, tim_sort, \
    merge_sort, radix_sort, radix_sort_v2, hybrid_QSort_v2, hybrid_QSort, middle_quick_sort, \
    binary_insertion_sort, bim_sort, qim_sort, m_qim_sort, bogo_sort, sysexit

"""________________________Constants________________________"""

_WR_FACTORS: list[int] = _TWR_FACTORS[-20:] if 20 < len(_TWR_FACTORS) else \
    [1] * (20 - len(_TWR_FACTORS)) + _TWR_FACTORS  # Slider ticks constant

_BUILTIN_FUNCS: dict[str, SortingAlgorithm] = {' '.join(__temp.__name__.title().split('_')): __temp for __temp in
                                               [bogo_sort,
                                                bubble_sort,
                                                shaker_sort,
                                                insertion_sort,
                                                binary_insertion_sort,
                                                gnome_sort,
                                                brick_sort,
                                                selection_sort,
                                                comb_sort,
                                                shell_sort,
                                                heap_sort,
                                                tim_sort,
                                                bim_sort,
                                                qim_sort,
                                                m_qim_sort,
                                                merge_sort,
                                                intro_sort,
                                                quick_sort,
                                                middle_quick_sort,
                                                hybrid_QSort,
                                                hybrid_QSort_v2,
                                                radix_sort,
                                                radix_sort_v2,
                                                ]}  # Dict of builtin sorting algorithms

"""________________________Visual Array________________________"""


class VisualArray(MainWindow):
    """Array class that is responsible for handling assignment and accessing of the bars.
       --Note that this has been done the way it is due to the fact that python does not allow to
       override assignment of objects--
    """

    def __init__(self, values: list[int] = None, *, only_positive: bool = False, true_random: bool = False,
                 sample_size: int = _resolution[0], select_color: Color = (0, 255, 0),
                 bar_color: Color = (255, 255, 255), access_color: Color = (255, 0, 0),
                 is_separated: bool = True, background_color: Color = (0, 0, 0),
                 economical: bool = False, no_toolBar: bool = False, delay: float = 0.001) -> None:
        """Assertions"""
        if VisualArray.check_given_values(values):
            sample_size = len(values)  # Checks the length of the given values.

        else:
            VisualArray.check_given_sample_size(sample_size)  # Checks the sample size.

        """Other attributes"""

        self.algorithm: SortingAlgorithm = quick_sort  # Current algorithm used by the main array.

        self.is_algo_running: bool = False  # True if a sorting algorithm or shuffle has been called.

        self.sample_size: int = sample_size  # Number of elements in the main array.

        self.true_random: bool = true_random  # If False, after sorting the array, the values increase constantly.

        self.finished: bool = False  # True if the array is sorted.

        self.economical: bool = economical  # True results in no coloring when accessing values.

        self.delay: float = 0.001  # A virtual delay to slow down the visualization.

        self.running: bool = False  # Indicates whether the executed function is paused.

        """Bar attributes"""

        bar_width: int = _resolution[0] // sample_size - is_separated  # Width of the bars of the array.

        if bar_width < 1:
            bar_width, is_separated = 1, False

        """ToolBar attributes"""

        super(VisualArray, self).__init__(color=background_color, bar_color=bar_color,
                                          selection_color=select_color, access_color=access_color,
                                          bar_width=bar_width, is_separated=is_separated,
                                          only_positive=only_positive, no_toolBar=no_toolBar, delay=delay)

        self.setWindowTitle("Sorting Visualizer")

        if not no_toolBar:
            self.prompt = self.eco_button = self.only_positive_button = \
                self.slider = self.algorithm_selector = None
            self.__create_toolBar()

        """Container"""

        values = self.rand_values() if not values else values  # Values that are used to make the bars.

        self.load_background()  # Loads the background.

        self._bar_objects: list[Bar] = [self.bar_at(values[i], i) for i in
                                        range(len(values))]  # Creates and draws the bars from values.

        self.cache_counter: int = max(_WR_FACTORS[0] // 8, len(self) // 40)

        self.update()

    def __str__(self) -> str:
        """Returns a string of the values of the bars"""

        return str([int(i) for i in self._bar_objects])

    def __repr__(self) -> str:
        """Returns a string of the QRect objects in the array"""

        return str([str(i) for i in self._bar_objects])

    def __len__(self) -> int:
        """Returns the number of elements in the main array"""

        return len(self._bar_objects)

    def __call__(self, sorting_algorithm: SortingAlgorithm = None) -> None:
        """Has the same effect of calling self.run(sorting_algorithm)"""

        return self.run(sorting_algorithm)

    def __getitem__(self, index: Union[slice, int, Bar]) -> Union[Bar, list[Bar]]:
        """Returns the Bar located at index if index is an int.
        Else returns a list of Bars in the given index slice"""

        while not self.running:
            # Pauses the execution of the currently running algorithm.

            if self.isHidden():
                quit()
            app.processEvents()

        if isinstance(index, slice):
            index = slice(index.start if index.start else 0,
                          index.stop if index.stop else len(self),
                          index.step if index.step else 1)

            if not self.economical:
                for i in range(*index.indices(index.stop - index.start)):
                    self.threaded_fill(i, self.access_color)

            return self._bar_objects[index]

        if self.cache_counter <= len(self.cache):
            self.process_cache()

        index = int(index)

        if not self.economical:
            self.threaded_fill(index, self.access_color)

        return self._bar_objects[index]

    def __setitem__(self, index: Union[slice, int], new_val: Union[list, Bar, int, VisualArray]) -> None:
        """Changes the value of the bar at the given index, internally and visually, if index is int.
        Else changes the values in the given index slice, internally and visually."""

        if isinstance(index, slice):
            index = slice(index.start if index.start else 0,
                          index.stop if index.stop else len(self),
                          index.step if index.step else 1)

            for i in range(index.start, index.stop):
                while not self.running:
                    if self.isHidden():
                        quit()
                    app.processEvents()

                self._bar_objects[i] = self.bar_at(new_val[i - index.start], i)

            self.update()
            return

        if not self.economical:
            self.threaded_fill(index, self.access_color)

        index = int(index)

        while not self.running:
            if self.isHidden():
                quit()
            app.processEvents()

        if self.cache_counter <= len(self.cache):
            self.process_cache()

        self._bar_objects[index] = self.bar_at(new_val, index)

        ticker(self.update)

    def run(self, func: SortingAlgorithm = None) -> None:
        """Displays the screen and runs the sorting algorithm"""

        self.showFullScreen()

        self.show()

        self.algorithm = func if func is not None else self.algorithm

        app.exec_()

    def quit(self) -> None:
        self.running = True
        sysexit(0)

    def __create_toolBar(self) -> None:
        """Creates the tool bar and its widgets"""

        self.addToolBar(self.tool_bar)

        # Buttons

        self.create_button(self.quit,
                           "Terminates the python script",
                           "Quit")

        self.create_button(self.shuffle,
                           "Shuffles the array and restarts the sorting algorithm",
                           "Shuffle n'Restart")

        self.create_button(self.start,
                           "Pauses or resumes the sorting algorithm",
                           "Start / Pause")

        # End of buttons

        # Size Slider

        self.slider: QSlider = QSlider(Qt.Horizontal, self)

        self.slider.setToolTip("Creates a new array of the selected size")

        self.slider.setRange(0, min(19, len(_WR_FACTORS)))

        self.slider.setTickInterval(1)

        self.slider.setTickPosition(QSlider.TicksBothSides)

        self.slider.setFixedSize(400, 14)

        self.slider.setValue(_WR_FACTORS.index(self.sample_size))

        self.slider.valueChanged.connect(lambda __value: self.change_size(_WR_FACTORS[__value]))

        self.tool_bar.addWidget(self.slider)

        self.tool_bar.addSeparator()

        # End of slider

        # Color Pickers

        self.create_button(self.bar_color_picker,
                           "Displays a color wheel to change the bar color",
                           "Bar Color",
                           push=True,
                           size=(65, 13),
                           separate=False)

        self.create_button(self.background_color_picker,
                           "Displays a color wheel to change the background color",
                           "Background Color",
                           push=True,
                           size=(110, 13),
                           separate=False)

        self.create_button(self.access_color_picker,
                           "Displays a color wheel to change the access color",
                           "Access Color",
                           push=True,
                           size=(90, 13),
                           separate=False)

        self.create_button(self.selection_color_picker,
                           "Displays a color wheel to change the selection color",
                           "Selection Color",
                           push=True,
                           size=(100, 13),
                           separate=False)

        self.tool_bar.addSeparator()

        # End of color pickers

        # Algorithm Dropdown Menu

        self.algorithm_selector: QPushButton = QPushButton(' '.join(self.algorithm.__name__.title().split('_')))

        self.algorithm_selector.setFixedSize(95, 13)

        self.algorithm_selector.setToolTip("List containing the builtin sorting algorithms")

        self.algorithm_selector.setFont(QFont("Monaco", 9, QFont.Monospace))

        self.tool_bar.addWidget(self.algorithm_selector)

        menu: QMenu = QMenu()

        for i in _BUILTIN_FUNCS:
            menu.addAction(i)

        self.algorithm_selector.setMenu(menu)

        def menu_handler_main(selected: any) -> None:
            self.clear_cache()

            self.start() if self.running else ...

            self.algorithm = _BUILTIN_FUNCS[selected.text()]

            name: str = self.algorithm.__name__.title()

            self.algorithm_selector.setText(' '.join(name.split('_')) if len(name) < 15
                                            else ''.join(_str[0] for _str in name.split('_')))

            self.algorithm(self)
            self.end_sort()

        menu.triggered.connect(menu_handler_main)

        # End of dropdown menu

        # Only Positive Attribute

        self.only_positive_button = QAction(f"Only Positive: {self.only_positive}", self)

        self.only_positive_button.setToolTip("Creates a new array only containing positive values if set to True")

        def change_op() -> None:
            self.only_positive = not self.only_positive
            self.only_positive_button.setText(f"Only Positive: {self.only_positive}")

            self.change_size(self.sample_size)

        self.only_positive_button.triggered.connect(change_op)

        self.tool_bar.addAction(self.only_positive_button)

        # End of positive attribute

        # Efficiency Button

        self.eco_button = QAction(f"Efficient: {bool(self.economical)}", self)

        self.eco_button.setToolTip("Speeds up the sorting algorithm")

        def change_eco() -> None:
            self.economical = not self.economical
            self.eco_button.setText(f"Efficient: {self.economical}")
            for __i in self.cache:
                self.load_bar(self._bar_objects[__i])

        self.eco_button.triggered.connect(change_eco)

        self.tool_bar.addAction(self.eco_button)

        # End of efficiency button

    def swap(self, i: int, j: int) -> None:
        """Efficient swap of elements between i and j"""

        self._bar_objects[i], self._bar_objects[j] = \
            self.bar_at(self[j], i), self.bar_at(self[i], j)

        ticker(self.update)

    def clear(self) -> None:
        [self.bar_at(self._bar_objects[i], i) for i in range(len(self))]

        self.update()

    def end_sort(self) -> None:
        """Called at the end of the sorting algorithm"""

        self.clear_cache()
        self.clear()

        for i in range(len(self) - 1):
            self.nu_fill(self._bar_objects[i], self.selection_color)
            self.nu_fill(self._bar_objects[i + 1], self.access_color)

            if not i % 5:
                self.update()

        self.clear()

        self.running = self.is_algo_running = False
        self.finished = True

        self.set_slider_active(True)

    @staticmethod
    def check_given_values(values: list[int]) -> bool:
        if not values:
            return False

        assert _WR_FACTORS[0] <= len(values) <= _resolution[
            0], f"len(values) larger than resolution width ({_resolution[0]}) " \
                f"or less than minimum allowable ({_WR_FACTORS[0]})"
        assert not (_resolution[0] % len(values)), f"resolution width ({_resolution[0]}) not divisible by len(values)"
        return True

    @staticmethod
    def check_given_sample_size(sample_size: int) -> None:
        if sample_size is None:
            return

        assert _WR_FACTORS[0] <= sample_size, f"sample_size was not given or less than minimum allowable ({_WR_FACTORS[0]})"
        assert sample_size <= _resolution[0], f"sample size larger than resolution width ({_resolution[0]})"
        assert not (_resolution[0] % sample_size), f"resolution width ({_resolution[0]}) not divisible by sample_size"

    def shuffle(self) -> None:
        """Shuffles the array (in real time) and restarts the sorting algorithm"""

        self.finished = False

        self.set_slider_active(False)

        self.running = self.is_algo_running = True

        shuffle(self)

        self.running = self.is_algo_running = False

        self.set_slider_active(True)

        self.clear_cache()

    def start(self) -> None:
        """Starts / Pauses / Resumes the sorting algorithm or shuffle"""

        if self.finished:
            self.end_sort()
            return

        self.running = not self.running

        self.set_slider_active(not self.running)

        if not self.is_algo_running and self.algorithm:
            self.is_algo_running = True
            self.algorithm(self)
            self.end_sort()

    def rand_values(self) -> list[int]:
        """Returns an list of random values"""

        return rand_array(1, _resolution[1], self.sample_size, self.true_random) \
            if self.only_positive else \
            rand_array(-_resolution[1] // 2 + 1, _resolution[1] // 2 - 1, self.sample_size, self.true_random)

    def set_slider_active(self, state: bool) -> None:
        """Disables and enables the slider"""

        self.slider.setDisabled(not state)
        self.slider.setUpdatesEnabled(state)
        self.algorithm_selector.setDisabled(not state)
        self.only_positive_button.setDisabled(not state)

    def change_size(self, size: int) -> None:
        """Creates a new array with the given size"""

        self.cache.clear()

        self.finished = False

        self.sample_size = size

        is_separated: bool = True

        bar_width: int = _resolution[0] // self.sample_size - is_separated

        if bar_width < 1:
            bar_width, is_separated = 1, False

        self.bar_width, self.is_separated = bar_width, is_separated

        self._bar_objects[::] = self.rand_values()

        for i in range(len(self._bar_objects)):
            self._bar_objects[i] = self.bar_at(self._bar_objects[i], i)

        self.running = self.is_algo_running = False

        self.cache_counter: int = max(_WR_FACTORS[0] // 8, len(self) // 40)

        self.update()

        return

    def color_selector(self, element: int) -> None:
        """Color wheel widget used to change the color of elements on display"""

        was_running: bool = self.running

        self.start() if self.running else ...

        attrs: tuple[str, str, str, str] = ("bar_color", "color", "access_color", "selection_color")

        self.color_wheel.show()

        self.color_wheel.setCurrentColor(super().__getattribute__(attrs[element]))

        while not self.color_wheel.isHidden():
            super().__setattr__(attrs[element], self.color_wheel.currentColor())

            if element == 2 and not self.economical:
                for i in self.cache:
                    self.nu_fill(self._bar_objects[i], self.access_color)

            else:
                self.clear_cache() if self.economical and element == 3 else ...

                for i in range(len(self)):
                    if i in self.cache:
                        self.bar_at(self._bar_objects[i], i)
                        self.nu_fill(self._bar_objects[i], self.access_color)
                        continue

                    self.bar_at(self._bar_objects[i], i)

            self.update()

        self.start() if was_running else ...
        self.color_wheel.setDisabled(True)
        self.color_wheel.setHidden(True)
        self.color_wheel.setUpdatesEnabled(False)

        return

    def bar_color_picker(self) -> None:
        """Place-Holder function for the bar color wheel"""

        return self.color_selector(0)

    def background_color_picker(self) -> None:
        """Place-Holder function for the background color wheel"""

        return self.color_selector(1)

    def access_color_picker(self) -> None:
        """Place-Holder function for the access color"""

        return self.color_selector(2)

    def selection_color_picker(self) -> None:
        """Place-Holder function for the selection color"""

        return self.color_selector(3)
