#include <SFML/Graphics.hpp>
#include <functional> 
#include <cmath> 
#include <string>

// Функция для отрисовки графика
void drawGraph(sf::RenderWindow& window, std::function<float(float)> func, float xMin, float xMax, float scaleX, float scaleY, sf::Color color) {
    sf::VertexArray graph(sf::LinesStrip);

    for (float x = xMin; x <= xMax; x += 0.1f) {
        float y = func(x); // Вычисление значения функции

        // Преобразование координат в экранные
        float screenX = 400 + x * scaleX;
        float screenY = 300 - y * scaleY;

        // Добавление точки в массив вершин
        graph.append(sf::Vertex(sf::Vector2f(screenX, screenY), color));
    }

    window.draw(graph);
}

int main() {
    // Создание окна
    sf::RenderWindow window(sf::VideoMode(800, 600), "Приложение для вывода графиков");

    // Переменная для хранения пользовательской точки
    sf::CircleShape userPoint(5); // Радиус 5 пикселей
    userPoint.setFillColor(sf::Color::Red);
    bool userPointExists = false; // Переменная для проверки существования пользовательской точки

    // 1 _ Загрузка шрифта (допишите код)
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        // Если не удалось загрузить стандартный шрифт, пробуем создать системный
        font.loadFromFile("C:/Windows/Fonts/arial.ttf");
    }

    // 2 _ Текст для отображения координат точки (допишите код)
    // Размер текста 20, положение текста (10,10), цвет белый. Текст храните в переменной coordinatesText
    sf::Text coordinatesText;
    coordinatesText.setFont(font);
    coordinatesText.setCharacterSize(20);
    coordinatesText.setFillColor(sf::Color::White);
    coordinatesText.setPosition(10, 10);

    // Оси X и Y
    sf::VertexArray xAxis(sf::Lines, 2);
    xAxis[0].position = sf::Vector2f(50, 300); // Начало оси X
    xAxis[0].color = sf::Color::White; // Цвет оси
    xAxis[1].position = sf::Vector2f(750, 300); // Конец оси X
    xAxis[1].color = sf::Color::White;

    sf::VertexArray yAxis(sf::Lines, 2);
    yAxis[0].position = sf::Vector2f(400, 50); // Начало оси Y
    yAxis[0].color = sf::Color::White; // Цвет оси
    yAxis[1].position = sf::Vector2f(400, 550); // Конец оси Y
    yAxis[1].color = sf::Color::White;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            // Проверка клика мышью
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    // Получение позиции клика
                    sf::Vector2i mousePos = sf::Mouse::getPosition(window);

                    // Преобразование экранных координат в "математические"
                    float mathX = (mousePos.x - 400) / 30.0f; // Масштаб 30 по X
                    float mathY = -(mousePos.y - 300) / 30.0f; // Масштаб 30 по Y (одинаковый с X!)

                    // Установка новой пользовательской точки
                    userPoint.setPosition(mousePos.x - userPoint.getRadius(), mousePos.y - userPoint.getRadius());
                    userPointExists = true; // Помечаем, что точка существует

                    // 3 _ Допишите логику проверки точки по переменным mathX и mathY !
                    // Вычисляем значения функций в точке mathX
                    float parabolaY = mathX * mathX - 2 * mathX - 6; // y1 = x² - 2x - 6
                    float lineY = 2.0f; // y2 = 2 (горизонтальная прямая)

                    std::string region;
                    const float EPSILON = 0.05f; // Допуск для проверки на границу

                    // Проверяем, попадает ли точка на границу
                    if (fabs(mathY - parabolaY) < EPSILON) {
                        region = "Граница (парабола y = x² - 2x - 6)";
                    }
                    else if (fabs(mathY - lineY) < EPSILON) {
                        region = "Граница (прямая y = 2)";
                    }
                    else {
                        // Если не на границе, определяем область

                        // Находим, где парабола пересекает прямую y = 2
                        // Решаем уравнение: x² - 2x - 6 = 2
                        // x² - 2x - 8 = 0
                        // Дискриминант: D = 4 + 32 = 36
                        float intersect1 = (2 - 6) / 2;  // x = -2
                        float intersect2 = (2 + 6) / 2;  // x = 4

                        // Определяем положение относительно прямой y = 2
                        bool aboveLine = mathY > lineY;
                        bool belowLine = mathY < lineY;

                        // Определяем положение относительно параболы y = x² - 2x - 6
                        bool aboveParabola = mathY > parabolaY;
                        bool belowParabola = mathY < parabolaY;

                        // Логика определения области согласно условию:
                        // Слева от параболы означает: mathX < intersect1 (левее -2)
                        // Справа от параболы означает: mathX > intersect2 (правее 4)
                        // Внутри параболы означает: mathX между intersect1 и intersect2 (-2 < mathX < 4)

                        if (aboveLine && mathX < intersect1) {
                            // Выше прямой y=2 и слева от параболы (x < -2)
                            region = "Oblast 1";
                        }
                        else if (belowLine && belowParabola) {
                            // Ниже обеих функций
                            region = "Oblast 2";
                        }
                        else if (belowLine && mathX > intersect1 && mathX < intersect2) {
                            // Ниже прямой y=2 и внутри параболы (-2 < x < 4)
                            region = "Oblast 3";
                        }
                        else if (aboveLine && mathX > intersect2) {
                            // Выше прямой y=2 и справа от параболы (x > 4)
                            region = "Oblast 4";
                        }
                        else {
                            // Оставшиеся области (например, выше прямой и внутри параболы)
                            region = "Ne vhodit v Oblast 1-4";
                        }
                    }

                    // Обновление текста с координатами точки 
                    coordinatesText.setString("X: " + std::to_string(mathX) +
                        ", Y: " + std::to_string(mathY) +
                        "\n" + region);
                }
            }
        }

        // 4 _ Очистка экрана (допишите код)
        window.clear(sf::Color::Black);

        // Отрисовка осей
        window.draw(xAxis);
        window.draw(yAxis);

        // 5 _  Отрисовка графика y1 = x*x - 2*x - 6 
        // Используем одинаковый масштаб по X и Y для правильного отображения
        drawGraph(window, [](float x) { return x * x - 2 * x - 6; }, -10, 10, 30, 30, sf::Color::Blue);

        // 5 _   Отрисовка графика y2 = 2 
        // Используем тот же масштаб по Y = 30
        drawGraph(window, [](float x) { return 2; }, -10, 10, 30, 30, sf::Color::Red);

        // Отрисовка пользовательской точки, если она существует
        if (userPointExists) {
            window.draw(userPoint);
            window.draw(coordinatesText);
        }

        // Отображение нового кадра
        window.display();
    }

    return 0;

}

