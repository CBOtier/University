import time
import sys

ms = [1, 2, 3, 4, 5, 6]
n = 4
d = 7

# Память до
mem_before = sys.getsizeof(ms)
for item in ms:
    mem_before += sys.getsizeof(item)

st_tm = time.time()
for _ in range(5000):
    ms.insert(n, d)
end_tm = time.time()

# Память после
mem_after = sys.getsizeof(ms)
for item in ms:
    mem_after += sys.getsizeof(item)

res_tm = (end_tm - st_tm) * 1000
print(f"Время: {res_tm:.2f} мс")
print(f"Память: {mem_after - mem_before} байт")
print(f"Размер списка: {len(ms)} элементов")