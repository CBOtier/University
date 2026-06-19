import time
import random
from concurrent.futures import ProcessPoolExecutor



 # быстрая сортировка как в лабораторной №3


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



# Параллельная быстрая сортировка

MIN_CHUNK_FOR_PARALLEL = 2000  # ниже этого порога параллелить невыгодно


def _quick_sort_worker(array):

    return quick_sort(array)


def quick_sort_parallel(array, num_threads):
    if num_threads <= 1 or len(array) < MIN_CHUNK_FOR_PARALLEL:
        return quick_sort(array)

    if len(array) <= 1:
        return array

    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]

    threads_left = num_threads // 2
    threads_right = num_threads - threads_left

    with ProcessPoolExecutor(max_workers=2) as executor:
        future_left = executor.submit(quick_sort_parallel, left, threads_left)
        future_right = executor.submit(quick_sort_parallel, right, threads_right)
        sorted_left = future_left.result()
        sorted_right = future_right.result()

    return sorted_left + middle + sorted_right


# Бенчмаркинг

def benchmark(sort_function, data, *args):
    arr = data.copy()
    start = time.perf_counter()
    sort_function(arr, *args)
    elapsed = time.perf_counter() - start  # секунды
    return elapsed


def run_benchmarks():
    sizes = [100, 1000, 10000, 20000, 30000, 40000, 50000]
    thread_counts = [2, 4, 8]
    runs = 3

    results = []

    for n in sizes:
        normal_times = []
        parallel_times = {t: [] for t in thread_counts}

        for _ in range(runs):
            data = [random.randint(0, 1000000) for _ in range(n)]

            normal_times.append(benchmark(quick_sort, data))

            for t in thread_counts:
                parallel_times[t].append(benchmark(quick_sort_parallel, data, t))

        normal_avg = sum(normal_times) / runs
        parallel_avg = {t: sum(parallel_times[t]) / runs for t in thread_counts}

        row = {
            "n": n,
            "normal": normal_avg,
            2: parallel_avg[2],
            4: parallel_avg[4],
            8: parallel_avg[8],
        }
        results.append(row)

        print(f"N = {n}")
        print("  Обычная сортировка:        ", round(normal_avg, 6), "с")
        for t in thread_counts:
            print(f"  Параллельная ({t} потока(ов)): ", round(parallel_avg[t], 6), "с")

    return results


if __name__ == "__main__":
    arr3 = [3, 6, 8, 10, 1, 2, 1]
    print(quick_sort_parallel(arr3.copy(), 4))

    data = run_benchmarks()

    # Сохраняем результаты для построения отчёта
    import json
    with open("benchmark_results.json", "w") as f:
        json.dump(data, f, indent=2)
