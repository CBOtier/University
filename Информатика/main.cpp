#include <iostream>
#include <cmath>
#include <algorithm>

using namespace std;

int main() {
    float x, y, R, S;

    cin >> x >> y;

    // Вычисление R = x * log10(y)
    R = x * log10(y);  // 

    // Вычисление S = sec(x) * кубический корень из y
    S = (1.0f / cos(x)) * cbrt(y);  

    cout << R << endl;
    cout << S << endl;
    cout << max(R, S) << endl;

    return 0;
}