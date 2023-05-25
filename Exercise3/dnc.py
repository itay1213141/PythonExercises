from random import randint


def dnc(baseFunc, combineFunc):
    def func(array):
        array_length = len(array)

        if array_length == 1:
            return baseFunc(array[0])

        if array_length == 2:
            return combineFunc(array[0], array[1])

        middle_index = array_length // 2
        first_half = array[:middle_index]
        second_half = array[middle_index:]

        return combineFunc(func(first_half), func(second_half))

    return func


def maxAreaHist(hist):
    pass


maxAreaHist([6, 2, 5, 4, 5, 1, 6])
