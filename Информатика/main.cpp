#include <iostream>
#include <limits>

using namespace std;

// Функция для ввода массива
void inputArray(int* arr, int size) {
    cout << "Vvedite " << size << " elementi massiva:\n";
    for (int i = 0; i < size; i++) {
        cout << "Element " << i + 1 << ": ";
        cin >> *(arr + i);  // Используем указательную арифметику
    }
}

// Функция для нахождения минимального элемента в массиве
int findMinValue(const int* arr, int size) {
    int minVal = *arr;  // Начинаем с первого элемента
    for (int i = 1; i < size; i++) {
        if (*(arr + i) < minVal) {
            minVal = *(arr + i);
        }
    }
    return minVal;
}

// Функция для прибавления значения ко всем элементам массива
void addValueToArray(int* arr, int size, int value) {
    for (int i = 0; i < size; i++) {
        *(arr + i) += value;  // Прибавляем значение к каждому элементу
    }
}

// Функция для вывода массива
void printArray(const int* arr, int size, const char* arrayName) {
    cout << arrayName << ": [";
    for (int i = 0; i < size; i++) {
        cout << *(arr + i);
        if (i < size - 1) {
            cout << ", ";
        }
    }
    cout << "]\n";
}

// Функция для копирования массива (чтобы сохранить исходные значения)
void copyArray(const int* source, int* destination, int size) {
    for (int i = 0; i < size; i++) {
        *(destination + i) = *(source + i);
    }
}

int main() {
    const int SIZE = 5;
    int A[SIZE], B[SIZE];
    int A_copy[SIZE], B_copy[SIZE];  // Копии для хранения исходных значений

    // Ввод массивов
    cout << " Vvod massiva A \n";
    inputArray(A, SIZE);

    cout << "\n Vvod massiva B \n";
    inputArray(B, SIZE);

    // Сохраняем копии исходных массивов
    copyArray(A, A_copy, SIZE);
    copyArray(B, B_copy, SIZE);

    // Находим минимальные значения
    int minA = findMinValue(A, SIZE);
    int minB = findMinValue(B, SIZE);


    // Прибавляем минимальные значения к массивам
    addValueToArray(A, SIZE, minA);
    addValueToArray(B, SIZE, minB);

    // Вывод результатов
    cout << "\n Iznachalnie massivi \n";
    printArray(A_copy, SIZE, "A");
    printArray(B_copy, SIZE, "B");

    cout << "\n new massiv \n";
    printArray(A, SIZE, "A");

    printArray(B, SIZE, "B");

    return 0;
}