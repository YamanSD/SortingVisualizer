# SortingVisualizer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)

The SortingVisualizer project is a sorting algorithms visualizer that provides a graphical demonstration of how various sorting algorithms work. With a user-friendly GUI, it allows users to interactively observe the sorting process.

This project is heavily inspired by Bingmann's [Sounds of Sorting](https://github.com/bingmann/sound-of-sorting)

![SortingVisualizer Screenshot 1](/images/pysorter_0.png)

## Installation

To install and set up the SortingVisualizer project, follow these steps:

1. Make sure you have Python 3.9 or later installed on your machine.
2. Clone the project repository: `git clone https://github.com/your-username/SortingVisualizer.git`
3. Change into the project directory: `cd SortingVisualizer`
4. Install the required dependencies using pip: `pip install -r requirements.txt`

## Usage

- Once the project is installed, you run the main.py file by: `python3 main.py`

- The visualizer's GUI will be displayed, allowing you to interact with the sorting algorithms.

## Features

The GUI provides the following controls:

- Start/Stop: Control the execution of the current sorting algorithm.
- Shuffle Array: Randomly shuffle the elements in the array.
- Resize Array: Change the size of the array to be sorted.
- Change Sorting Algorithm: Select from a list of supported sorting algorithms.
- Positive Integers or Positives/Negatives: Choose whether to allow positive integers only or both positive and negative integers.
- Customize Display Colors: Modify the colors of the displayed elements, such as bar colors and background colors.

## Supported Sorting Algorithms

The SortingVisualizer includes the following sorting algorithms:

- Bogo Sort
- Bubble Sort
- Shaker Sort
- Insertion Sort
- Binary Insertion Sort
- Gnome Sort
- Brick Sort
- Selection Sort
- Comb Sort
- Shell Sort
- Heap Sort
- Tim Sort
- Bim Sort
- Qim Sort
- M-Qim Sort
- Merge Sort
- Intro Sort
- Quick Sort
- Middle Quick Sort
- Hybrid QSort
- Hybrid QSort v2
- Radix Sort
- Radix Sort v2

Please note that some of these algorithms are custom implementations.

## Known Issues

- No sound generation is included.
- The visualizer works best with in-place sorting algorithms. Radix sorts "break" the array while sorting.
- The code structure and comments are not optimal due to the project being the developer's first experience.

## Contributing

Contributions to the SortingVisualizer project are welcome! If you would like to contribute, please follow these steps:

1. Fork the project repository.
2. Create a new branch for your contribution.
3. Make your changes and commit them with clear and descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request, describing the purpose and details of your contribution.

## License

The SortingVisualizer project is licensed under the [MIT License](LICENSE).

