def merge(left, right):
    left_i = 0
    right_i = 0
    result = []
    while left_i < len(left) and right_i < len(right):
        if left[left_i] < right[right_i]:
            result.append(left[left_i])
            left_i += 1
        else:
            result.append(right[right_i])
            right_i += 1

    result += left[left_i:]
    result += right[right_i:]
    return result


def merge_sort(list):
    if len(list) <= 1:
        return list
    half = len(list) // 2
    left = merge_sort(list[:half])
    right = merge_sort(list[half:])

    return merge(left, right)


ordered_array = merge_sort([int(x) for x in input().split()])
