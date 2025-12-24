#include <SFML/Graphics.hpp>

int main() {
    const int WINDOW_SIZE = 500;
    const int CELL_SIZE = 50;
    const int GRID_SIZE = 10; // 500 / 50 = 10 ячеек

    sf::RenderWindow window(sf::VideoMode(WINDOW_SIZE, WINDOW_SIZE),
        "Cells Above Main Diagonal");

    // Основной цикл
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Очищаем экран
        window.clear(sf::Color::White);

        // Вложенные циклы для отрисовки сетки
        for (int i = 0; i <= GRID_SIZE; ++i) {
            // Вертикальные линии
            sf::Vertex vertical_line[] = {
                sf::Vertex(sf::Vector2f(i * CELL_SIZE, 0), sf::Color::Black),
                sf::Vertex(sf::Vector2f(i * CELL_SIZE, WINDOW_SIZE), sf::Color::Black)
            };
            window.draw(vertical_line, 2, sf::Lines);

            // Горизонтальные линии
            sf::Vertex horizontal_line[] = {
                sf::Vertex(sf::Vector2f(0, i * CELL_SIZE), sf::Color::Black),
                sf::Vertex(sf::Vector2f(WINDOW_SIZE, i * CELL_SIZE), sf::Color::Black)
            };
            window.draw(horizontal_line, 2, sf::Lines);
        }

        // Создаем прямоугольник для закрашивания ячеек
        sf::RectangleShape cell(sf::Vector2f(CELL_SIZE - 2, CELL_SIZE - 2));

        // Алгоритм закрашивания ячеек выше главной диагонали
        for (int row = 0; row < GRID_SIZE; ++row) {
            for (int col = 0; col < GRID_SIZE; ++col) {
                // Проверяем условие: ячейка выше главной диагонали
                // Главная диагональ: row == col
                // Выше диагонали: row < col
                if (row < col) {
                    cell.setPosition(col * CELL_SIZE + 1, row * CELL_SIZE + 1);
                    cell.setFillColor(sf::Color(0, 120, 255)); // Синий цвет
                    window.draw(cell);
                }
            }
        }

        window.display();
    }

    return 0;
}