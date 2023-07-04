"""Built-in Sorting Algorithms Used in the Visualizer."""

from typing import TypeVar, Callable
from random import shuffle


Visual_Array = TypeVar("Visual_Array")
Bar = TypeVar("Bar")

"""Insertion Sort"""


def slice_insertion_sort(arr: Visual_Array, left: int, right: int) -> Visual_Array:
    for i in range(left + 1, right + 1):
        element = arr[i]
        j: int = i - 1

        while left <= j and element < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = element

    return arr


def insertion_sort(arr: Visual_Array) -> None:
    for i in range(1, len(arr)):
        element = arr[i]
        j: int = i - 1

        while 0 <= j and element < arr[j]:
            arr.select(i)
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = element


"""Bubble Sort"""


def bubble_sort(arr: Visual_Array) -> None:
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            arr.select(len(arr) - i - 1)

            if arr[j + 1] < arr[j]:
                arr[j + 1], arr[j] = arr[j], arr[j + 1]


"""Genome Sort"""


def gnome_sort(arr: Visual_Array) -> None:
    index = 0

    while index < len(arr):
        if not index or arr[index - 1] <= arr[index]:
            index += 1

        else:
            if not arr.economical:
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
            else:
                arr.swap(index, index - 1)

            index -= 1


"""Selection Sort"""


def selection_sort(arr: Visual_Array) -> None:
    for i in range(len(arr)):
        min_index: int = i

        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j

        if not arr.economical:
            arr[i], arr[min_index] = arr[min_index], arr[i]

        else:
            arr.swap(i, min_index)


"""Shaker Sort"""


def slice_shaker_sort(arr: Visual_Array, start: int, end: int) -> None:
    swapped: bool = True

    while swapped:
        swapped = False

        for i in range(start, end):
            if arr[i + 1] < arr[i]:
                if not arr.economical:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                else:
                    arr.swap(i, i + 1)

                swapped = True

        if not swapped:
            break

        swapped = False

        end -= 1

        for i in range(end - 1, start - 1, -1):
            if arr[i + 1] < arr[i]:
                if not arr.economical:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                else:
                    arr.swap(i, i + 1)

                swapped = True

        start += 1


def shaker_sort(arr: Visual_Array) -> None:
    return slice_shaker_sort(arr, 0, len(arr) - 1)


"""Comb Sort"""


def getNextGap(gap: int) -> int:
    return result if 1 <= (result := (gap * 10) // 13) else 1


def comb_sort(arr: Visual_Array) -> None:
    gap: int = len(arr)

    swapped: bool = True

    while gap != 1 or swapped:
        gap, swapped = getNextGap(gap), False

        for i in range(0, len(arr) - gap):
            if arr[i + gap] < arr[i]:
                if not arr.economical:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                else:
                    arr.swap(i, i + gap)

                swapped = True


"""Brick Sort"""


def brick_sort(arr: Visual_Array, _is_sorted: bool = False) -> None:
    while not _is_sorted and (_is_sorted := True):
        for j in range(2):
            for i in range(j, len(arr) - 1, 2):
                if arr[i + 1] < arr[i]:
                    if not arr.economical:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    else:
                        arr.swap(i, i + 1)

                    _is_sorted = False


"""Heap Sort"""


def heapify(arr: Visual_Array, n: int, i: int) -> None:
    largest: int = i
    l: int = 2 * i + 1
    r: int = l + 1

    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r

    if largest != i:
        if not arr.economical:
            arr[i], arr[largest] = arr[largest], arr[i]
        else:
            arr.swap(i, largest)

        heapify(arr, n, largest)


def heap_sort(arr: Visual_Array) -> None:
    n: int = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        if not arr.economical:
            arr[i], arr[0] = arr[0], arr[i]
        else:
            arr.swap(i, 0)

        heapify(arr, i, 0)


"""Quick Sort"""


def _partition(start: int, end: int, array) -> int:
    pivot_index: int = start
    pivot = array[pivot_index]

    array.select(pivot_index)

    while start < end:
        while start < len(array) and array[start] <= pivot:
            start += 1

        while pivot < array[end]:
            end -= 1

        if start < end:
            if not array.economical:
                array[start], array[end] = array[end], array[start]
            else:
                array.swap(start, end)

    if not array.economical:
        array[end], array[pivot_index] = array[pivot_index], array[end]
    else:
        array.swap(end, pivot_index)

    return end


def _real_quick_sort(array: Visual_Array, start: int, end: int) -> None:
    if start < end:
        p: int = _partition(start, end, array)

        _real_quick_sort(array, start, p - 1)
        _real_quick_sort(array, p + 1, end)


def quick_sort(array: Visual_Array) -> None:
    _real_quick_sort(array, 0, len(array) - 1)


"""Intro Sort"""


def intro_sort(arr: Visual_Array) -> None:
    intro_sort_helper(arr, 0, len(arr), (len(arr).bit_length() - 1) * 2)


def intro_sort_helper(arr: Visual_Array, start: int, end: int, depth: int) -> None:
    if end - start <= 1:
        return
    elif not depth:
        intro_heapsort(arr, start, end)
    else:
        p: int = intro_partition(arr, start, end)
        intro_sort_helper(arr, start, p + 1, depth - 1)
        intro_sort_helper(arr, p + 1, end, depth - 1)


def swap(arr: Visual_Array, i: int, j: int) -> None:
    if not arr.economical:
        arr[i], arr[j] = arr[j], arr[i]
    else:
        arr.swap(i, j)


def intro_partition(arr: Visual_Array, start: int, end: int) -> int:
    pivot, i, j = arr[start], start - 1, end
    arr.select(start)

    while True:
        i += 1
        j -= 1

        while arr[i] < pivot:
            i += 1

        while pivot < arr[j]:
            j -= 1

        if j <= i:
            arr.bar_at(arr._bar_objects[start], start)
            return j

        swap(arr, i, j)


def intro_heapsort(arr: Visual_Array, start: int, end: int) -> None:
    intro_build_max_heap(arr, start, end)

    for i in range(end - 1, start, -1):
        swap(arr, start, i)
        max_heapify(arr, index=0, start=start, end=i)


def intro_build_max_heap(arr: Visual_Array, start: int, end: int) -> None:
    index: int = (end - start - 2) // 2

    while 0 <= index:
        max_heapify(arr, index, start, end)
        index -= 1


def max_heapify(arr: Visual_Array, index: int, start: int, end: int) -> None:
    size: int = end - start
    l, r = 2 * index + 1, 2 * (index + 1)

    largest: int = l if l < size and arr[start + index] < arr[start + l] \
        else index

    if r < size and arr[start + largest] < arr[start + r]:
        largest = r

    if largest != index:
        swap(arr, start + largest, start + index)
        max_heapify(arr, largest, start, end)


"""Shell Sort"""


def shell_sort(array: Visual_Array) -> None:
    n: int = len(array)
    m: int = n // 2

    while 0 < m:
        for i in range(m, n):
            temp = array[i]
            j: int = i

            while m <= j and temp < array[j - m]:
                array[j] = array[j - m]
                j -= m

            array[j] = temp

        m //= 2


"""Tim Sort"""


def find_min_run(n: int, init: int) -> int:
    r: int = 0
    while init <= n:
        r |= n & 1
        n >>= 1

    return n + r


def merge(array: Visual_Array, l: int, m: int, r: int) -> None:
    array_length1, array_length2 = m - l + 1, r - m
    left, right = [array[l + i] for i in range(array_length1)], [array[m + i + 1] for i in range(array_length2)]

    i, j, k = 0, 0, l

    while j < array_length2 and i < array_length1:
        if left[i] <= right[j]:
            array[k] = left[i]
            i += 1

        else:
            array[k] = right[j]
            j += 1

        k += 1

    while i < array_length1:
        array[k] = left[i]
        k += 1
        i += 1

    while j < array_length2:
        array[k] = right[j]
        k += 1
        j += 1


def tim_sort(array: Visual_Array, func: Callable = slice_insertion_sort, init_min_run: int = 16) -> None:
    n: int = len(array)
    min_run: int = find_min_run(n, init_min_run)

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        func(array, start, end)

    while min_run < n:
        for left in range(0, n, 2 * min_run):
            merge(array,
                  left,
                  min(n - 1, left + min_run - 1),
                  min((left + 2 * min_run - 1), n - 1))

        min_run *= 2


"""Merge Sort"""


def merge_sort(arr: Visual_Array) -> None:
    return _real_merge_sort(arr, 0, len(arr) - 1)


def _real_merge_sort(arr: Visual_Array, l: int, r: int) -> None:
    if l < r:
        m: int = l + (r - l) // 2

        _real_merge_sort(arr, l, m)
        _real_merge_sort(arr, m + 1, r)

        merge(arr, l, m, r)


"""Hybrid QSort"""


def partition_hybrid(arr: Visual_Array, low: int, high: int) -> int:
    pivot: Bar = arr[high]
    j: int = low

    for i in range(low, high):
        if arr[i] < pivot:
            if not arr.economical:
                arr[i], arr[j] = arr[j], arr[i]
            else:
                arr.swap(i, j)

            j += 1

    if not arr.economical:
        arr[j], arr[high] = arr[high], arr[j]
    else:
        arr.swap(j, high)

    return j


def _real_hybrid_QSort(arr: Visual_Array, low: int, high: int) -> None:
    if low < high:
        pivot = partition_hybrid(arr, low, high)
        _real_hybrid_QSort(arr, low, pivot - 1)
        _real_hybrid_QSort(arr, pivot + 1, high)


def hybrid_QSort(arr: Visual_Array) -> None:
    return _real_hybrid_QSort(arr, 0, len(arr) - 1)


def hybrid_QSort_v2(arr: Visual_Array) -> None:
    return _real_hybrid_QSort_2(arr, 0, len(arr) - 1)


def _real_hybrid_QSort_2(arr: Visual_Array, low: int, high: int) -> None:
    while low < high:
        if high - low + 1 < 10:
            slice_insertion_sort(arr, low, high)
            break

        else:
            pivot = partition_hybrid(arr, low, high)

            if pivot - low < high - pivot:
                _real_hybrid_QSort_2(arr, low, pivot - 1)
                low = pivot + 1
            else:
                _real_hybrid_QSort_2(arr, pivot + 1, high)
                high = pivot - 1


"""Quick Sort Middle Pivot"""


def middle_partition(arr: Visual_Array, low: int, high: int) -> int:
    pivot: Bar = arr[(pivot_index := ((low := low - 1) + (high := high + 1)) // 2)]
    arr.select(pivot_index)

    while True:
        low += 1
        while arr[low] < pivot:
            low += 1

        high -= 1
        while pivot < arr[high]:
            high -= 1

        if low >= high:
            arr.bar_at(arr._bar_objects[pivot_index], pivot_index)
            return high

        arr[low], arr[high] = arr[high], arr[low]


def _real_middle_quick_sort(items, low, high):
    if low < high:
        split_index = middle_partition(items, low, high)
        _real_middle_quick_sort(items, low, split_index)
        _real_middle_quick_sort(items, split_index + 1, high)


def middle_quick_sort(arr: Visual_Array) -> None:
    _real_middle_quick_sort(arr, 0, len(arr) - 1)


"""Binary Insertion Sort"""


def _binary_search(arr: Visual_Array, item: Bar, low: int, high: int) -> int:
    if high <= low:
        return low + 1 if arr[low] < item else low

    return mid + 1 if item == arr[(mid := (low + high) // 2)] else \
        _binary_search(arr, item, mid + 1, high) if arr[mid] < item else \
        _binary_search(arr, item, low, mid - 1)


def binary_insertion_slice_sort(arr: Visual_Array, left: int, right: int) -> None:
    for i in range(left + 1, right + 1):
        selected, j = arr[i], i - 1
        arr.select(i)

        loc = _binary_search(arr, selected, left, j)

        while loc <= j:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = selected


def binary_insertion_sort(arr: Visual_Array) -> None:
    for i in range(0, len(arr)):
        selected: Bar = arr[(j := i)]
        arr.select(i)

        loc: int = _binary_search(arr, selected, 0, j)

        while loc <= (j := j - 1):
            arr[j + 1] = arr[j]

        arr[j + 1] = selected


"""Binary Tim Sort"""


def bim_sort(arr: Visual_Array) -> None:
    return tim_sort(arr, binary_insertion_slice_sort)


"""Middle Quick Tim Sort"""


def m_qim_sort(arr: Visual_Array) -> None:
    return tim_sort(arr, _real_middle_quick_sort, 32)


"""Quick Tim Sort"""


def qim_sort(arr: Visual_Array) -> None:
    return tim_sort(arr, _real_quick_sort, 32)


"""Radix Sort"""


def countingSort(array: Visual_Array, place: int, version: int) -> None:
    size, count = len(array), [0] * 10
    place_holder: list[Bar] = array[:] if version else [0] * size

    for i in range(size):
        count[(place_holder[i] if version else array[i]) // place % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i: int = size

    if version:
        while 0 <= (i := i - 1):
            index: int = place_holder[i] // place
            array[count[index % 10] - 1] = place_holder[i]
            count[index % 10] -= 1

    else:
        while 0 <= (i := i - 1):
            index: int = array[i] // place
            place_holder[count[index % 10] - 1] = array[i]
            count[index % 10] -= 1

    if not version:
        for i in range(size):
            array[i] = place_holder[i]


def radix_sort(array: Visual_Array, version: int = 0) -> None:
    max_element: Bar = max(array)

    place: int = 1
    while 0 < max_element // place:
        countingSort(array, place, version)
        place *= 10

    if array.only_positive:
        return

    for i in range(len(array)):
        if array[i] < 0:
            fn_index: int = i
            break

    if fn_index != len(array) // 2:
        return merge(array, 0, fn_index - 1, len(array) - 1)

    for i in range(fn_index):
        if not array.economical:
            array[i], array[i + fn_index] = array[i + fn_index], array[i]
        else:
            array.swap(i, i + fn_index)


"""Radix Sort V2"""


def radix_sort_v2(array: Visual_Array) -> None:
    return radix_sort(array, 1)


"""Bogo Sort"""


def is_sorted(arr: Visual_Array, predicate: Callable = lambda x, y: x <= y) -> bool:
    for i in range(1, len(arr)):
        if not predicate(arr[i - 1], arr[i]):
            return False
    return True


def bogo_sort(arr: Visual_Array) -> None:
    while not is_sorted(arr):
        shuffle(arr)
