import math

a = 1
b = 2

def f(x):
    return (math.sin(x) + 5) - (math.sin(x) + 3)

def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        coeff = 4 if i % 2 != 0 else 2
        total += coeff * f(a + i * h)
    return (h / 3) * total

s = 2.0

print("Точное значение:", s)
print()
print("N        | Площадь    | Погрешность | Точность")


for n in [2, 4, 10, 50, 100, 500, 1000, 5000, 10000]:
    area = simpson(f, a, b, n)
    error = abs(area - s)
    accuracy = 100.0 * (1 - error / s)
    print(f"N={n}: площадь={area}, погрешность={error}, точность={accuracy}%")