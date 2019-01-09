def sort(array):
    if len(array) < 2:
        return array

    is_tuple = type(array) is tuple

    middle = len(array) / 2
    left_list = sort(array[:middle])
    right_list = sort(array[middle:])
    sorted_array = merge(list(left_list), list(right_list))

    return tuple(sorted_array) if is_tuple else sorted_array


def merge(list1, list2):
    result = []

    while list1 and list2:
        current_list = list1 if list1[0] < list2[0] else list2
        result.append(current_list.pop(0))

    result += list1 + list2
    return result
