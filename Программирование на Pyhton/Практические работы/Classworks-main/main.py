# main.py
from calculator.basic import add, subtract, multiply
from calculator.advanced import power, square_root
from calculator.advanced.trigonometry import sin, cos, tan
import sys

print(add(2, 3))             # Вывод: 5
print(subtract(5, 2))        # Вывод: 3
print(power(2, 3))           # Вывод: 8
print(square_root(16))       # Вывод: 4.0
print(multiply(4, 5))
print(sys.path)
print(sin(0)) 
print(cos(0))  
print(tan(0))