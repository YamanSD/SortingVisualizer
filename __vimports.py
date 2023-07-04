"""Messy import file"""

from __VisualizingEngine import Union, \
    _resolution, Color, ticker, MainWindow, ThreadedTask, QAction, QPushButton, QFont, app

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QSlider, QMenu

from random import randint, shuffle as true_shuffle

from sys import exit as sysexit

from __builtin_algorithms import *

from time import sleep

VisualArray = list[any]

SortingAlgorithm = Union[Callable[Union[VisualArray, list], any], None]


def shuffle(arr: any) -> None:
    return true_shuffle(arr)


def rand_array(begin: int, end: int, size: int, true_rand: bool) -> [int]:
    if true_rand:
        return [randint(begin, end) for _ in range(size)]

    increase: float = _resolution[1] / size

    result: list[int] = [round((i + (1 if 0 <= i else 0)) * increase) if -1 <= i
                         else (i + (1 if 0 <= i else 0)) * increase
                         for i in range(-size // 2, size // 2)] \
        if begin < 0 else \
        [(i + 1) * increase for i in range(size)]

    shuffle(result)

    return result


def ge_factors(n: int) -> list[int]:
    return [n // i for i in range(int(n ** 0.5) * 2, 0, -1) if not n % i]


_TWR_FACTORS: list[int] = ge_factors(_resolution[0])
