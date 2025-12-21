#include <iostream>
#include <cmath>
#include <algorithm>

using namespace std;

int main() {
    float x, y;

    cin >> x >> y;

    // Вычисляем R, заменяя log10(0 или отрицательного) на 0
    float R = x * log10(max(y, 0.000001f));

    // Вычисляем S, избегая деления на 0
    float cos_val = cos(x);
    float sec_val = 1.0f / (abs(cos_val) < 0.000001f ? 0.000001f : cos_val);
    float S = sec_val * cbrt(y);

    cout << R << endl;
    cout << S << endl;
    cout << max(R, S) << endl;

    return 0;
}