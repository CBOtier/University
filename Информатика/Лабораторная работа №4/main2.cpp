#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void processSets() {
    int n, m;

    cout << "Razmer pervogo mn: ";
    cin >> n;
    cout << "Razmer vtorogo mn: ";
    cin >> m;

    vector<int> A(n), B(m);

    // Ввод первого множества
    cout << "\npervoe mn: ";
    for (int i = 0; i < n; i++) cin >> A[i];

    // Ввод второго множества
    cout << "vtoroe mn: ";
    for (int i = 0; i < m; i++) cin >> B[i];

    // Вектор для результата
    vector<int> result;

    // Добавляем нечетные из первого множества
    for (int x : A) {
        if (x % 2 != 0) {
            if (find(result.begin(), result.end(), x) == result.end()) {
                result.push_back(x);
            }
        }
    }

    // Добавляем нечетные из второго множества
    for (int x : B) {
        if (x % 2 != 0) {
            if (find(result.begin(), result.end(), x) == result.end()) {
                result.push_back(x);
            }
        }
    }

    // Сортируем результат
    sort(result.begin(), result.end());

    // Вывод
    cout << "\nResult: ";
    for (int x : result) cout << x << " ";
    cout << endl;
}

int main() {
    processSets();
    return 0;
}
