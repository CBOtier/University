def find_first(nums, target):
    left = 0
    right = len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            result = mid
            right = mid - 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def find_last(nums, target):
    left = 0
    right = len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            result = mid
            left = mid + 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


nums = list(map(int, input().split()))
target = int(input())

first = find_first(nums, target)
last = find_last(nums, target)

if first == -1:
    print("Элемент не найден в массиве")
else:
    print(f"Первое вхождение элемента {target} находится по индексу {first}")
    print(f"Последнее вхождение элемента {target} находится по индексу {last}")


# Примеры:
# nums = [2, 5, 5, 5, 6, 8, 9, 9], target = 5
# → Первое вхождение элемента 5 находится по индексу 1
#   Последнее вхождение элемента 5 находится по индексу 3
#
# nums = [2, 5, 5, 5, 6, 8, 9, 9], target = 4
# → Элемент не найден в массиве
