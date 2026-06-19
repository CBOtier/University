import time
import random



#  Radix Sort


def merge_buckets(buckets):
    merged_array = []
    for bucket in buckets:
        merged_array.extend(bucket)
    return merged_array


def sort_by_digit(array, digit_place):
    buckets = [[] for _ in range(10)]
    for num in array:
        bucket_index = (num // digit_place) % 10
        buckets[bucket_index].append(num)
    new_array = merge_buckets(buckets)
    for i in range(len(array)):
        array[i] = new_array[i]


def radix_sort(array):
    max_num = max(array)
    digit_place = 1
    while max_num // digit_place > 0:
        sort_by_digit(array, digit_place)
        digit_place *= 10
    return array


#  Merge Sort


def merge_sort(array):
    if len(array) > 1:
        mid = len(array) // 2
        left_half = array[:mid]
        right_half = array[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = 0  
        j = 0  
        k = 0  

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                array[k] = left_half[i]
                i += 1
            else:
                array[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            array[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            array[k] = right_half[j]
            j += 1
            k += 1

    return array



#  Quick Sort


def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def quick_sort_recursive(array, low, high):
    if low < high:
        pivot_index = partition(array, low, high)
        quick_sort_recursive(array, low, pivot_index - 1)
        quick_sort_recursive(array, pivot_index + 1, high)


def quick_sort(array):
    quick_sort_recursive(array, 0, len(array) - 1)
    return array




def benchmark(sort_function, data):
    arr = data.copy()
    start = time.perf_counter()
    sort_function(arr)
    elapsed = (time.perf_counter() - start) * 1000  # ms
    return elapsed


def run_benchmarks():
    sizes = [100, 500, 1000, 5000, 10000]
    runs = 5

    for n in sizes:
        radix_times = []
        merge_times = []
        quick_times = []

        for _ in range(runs):
            data = [random.randint(0, 10000) for _ in range(n)]
            radix_times.append(benchmark(radix_sort, data))
            merge_times.append(benchmark(merge_sort, data))
            quick_times.append(benchmark(quick_sort, data))

        r = sum(radix_times) / runs
        m = sum(merge_times) / runs
        q = sum(quick_times) / runs

  
        print("  Radix Sort:", round(r, 2), "ms")
        print("  Merge Sort:", round(m, 2), "ms")
        print("  Quick Sort:", round(q, 2), "ms")


if __name__ == "__main__":

   
    arr = [170, 45, 75, 90, 2, 802, 24, 66]
    radix_sort(arr)
    print(arr)


    arr2 = [38, 27, 43, 3, 9, 82, 10]
    merge_sort(arr2)
    print(arr2)


    arr3 = [3, 6, 8, 10, 1, 2, 1]
    quick_sort(arr3)
    print(arr3)

    run_benchmarks()