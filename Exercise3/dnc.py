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


# This is an actual divide and conquer solution, but its not 'efficient' apparently
def maxAreaHist2(array):
    def calculateArea(heights, start, end):
        if start > end:
            return 0

        min_index = start

        for i in range(start, end + 1):
            if heights[i] < heights[min_index]:
                min_index = i

        range_width = (end - start + 1)

        return max(
            heights[min_index] * range_width,
            calculateArea(heights, start, min_index - 1),
            calculateArea(heights, min_index + 1, end),
        )

    return calculateArea(array, 0, len(array) - 1)


def maxAreaHist(array):
    stack = []
    max_area = 0
    i = 0

    while i < len(array):
        if not stack or array[i] >= array[stack[-1]]:
            stack.append(i)
            i += 1
        else:
            top_index = stack.pop()
            area = (
                array[top_index]
                * (i if not stack else i - stack[-1] - 1)
            )
            max_area = max(max_area, area)

    while stack:
        top_index = stack.pop()
        area = (
            array[top_index]
            * (i if not stack else i - stack[-1] - 1)
        )
        max_area = max(max_area, area)

    return max_area
