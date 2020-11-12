def merge(left, right):
    left_i = 0
    right_i = 0
    result = []
    while left_i < len(left) and right_i < len(right):
        if left[left_i][0] < right[right_i][0]:
            result.append(left[left_i])
            left_i += 1
        else:
            result.append(right[right_i])
            right_i += 1

    result += left[left_i:]
    result += right[right_i:]
    return result


def merge_sort(array):
    if len(array) <= 1:
        return array
    half = len(array) // 2
    left = merge_sort(array[:half])
    right = merge_sort(array[half:])

    return merge(left, right)
