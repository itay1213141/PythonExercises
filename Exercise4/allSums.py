def allSumsDP(arr):
    all_sums = set()

    def calculateSums(current_sum, current_index, calculated):
        if current_index == len(arr):
            all_sums.add(current_sum)
            return

        if (current_sum, current_index) in calculated:
            return

        calculated.add((current_sum, current_index))

        calculateSums(current_sum + arr[current_index], current_index + 1, calculated)
        calculateSums(current_sum, current_index + 1, calculated)

    calculateSums(0, 0, set())
    return all_sums
