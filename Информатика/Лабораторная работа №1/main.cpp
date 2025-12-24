#include <iostream>
#include <cmath>
#include <algorithm>

using namespace std;

int main() {
    float x, y, R, S;

    cin >> x >> y;

    R = x * log10(y);
    S = (1.0f / cos(x)) * cbrt(y);

    cout << R << endl;
    cout << S << endl;
    cout << max(R, S) << endl;

    system("pause"); // Окно не закроется пока не нажмете любую клавишу
    
    return 0;
}
