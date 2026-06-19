import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from typing import Dict, List, Tuple
import math
import osmnx as ox
import os

def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Вычисляет расстояние между двумя точками на поверхности Земли (в километрах)
    """
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371  # Радиус Земли в км

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

import heapq

def dijkstra(graph: Dict[Tuple[float, float], List[Tuple[Tuple[float, float], float]]],
              start: Tuple[float, float],
              end: Tuple[float, float]) -> Tuple[List[Tuple[float, float]], float, List[str]]:
    # Приоритетная очередь для хранения (расстояние, узел)
    # ВАШ КОД
    pq = [(0, start)]
    
    # Словарь для хранения кратчайшего расстояния до каждого узла и предыдущего узла
    # ВАШ КОД
    distances = {start: 0}
    previous = {}
    
    # Множество посещённых узлов
    # ВАШ КОД
    visited = set()

    # ВАШ КОД
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        if current_node == end:
            break
            
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                if neighbor in visited:
                    continue
                    
                new_distance = current_dist + weight
                
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))

    # Восстановление пути
    # ВАШ КОД
    path = []
    current = end
    
    # Здесь не собираем названия улиц, так как их нет в графе, возвращаем пустой список
    # ВАШ КОД
    if current not in previous and current != start:
        return [], 0, []
    
    # Реконструкция пути от конца к началу
    # ВАШ КОД
    while current in previous:
        path.append(current)
        current = previous[current]
    path.append(start)
    path.reverse()

    # Общее расстояние от начала до конца
    # ВАШ КОД
    total_distance = distances.get(end, 0)
    
    # Создаем список названий улиц (пустой, так как в графе их нет)
    street_names = []

    return path, total_distance, street_names


def build_graph(edges: List[Tuple[Tuple[float, float], Tuple[float, float], str]]) -> Dict[Tuple[float, float], List[Tuple[Tuple[float, float], float]]]:
    """
    Строит граф из рёбер
    """
    graph = {}
    for start, end, _ in edges:
        dist = haversine(start, end)
        graph.setdefault(start, []).append((end, dist))
        graph.setdefault(end, []).append((start, dist))  # если граф неориентированный
    return graph

def read_graphml(file_path: str) -> Tuple[Dict[str, Tuple[float, float]], List[Tuple[Tuple[float, float], Tuple[float, float], str]]]:
    """
    Читает GraphML файл и возвращает узлы и ребра с названиями улиц

    Args:
        file_path: путь к файлу .graphml

    Returns:
        Кортеж (nodes, edges), где:
        - nodes: словарь {node_id: (x, y)}
        - edges: список [((x1, y1), (x2, y2), название_улицы), ...]
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'g': 'http://graphml.graphdrawing.org/xmlns'}

    nodes = {}
    for node in root.findall('.//g:node', ns):
        node_id = node.get('id')
        x, y = None, None
        for data in node.findall('.//g:data', ns):
            if data.get('key') == 'd4':  # x координата (обычно longitude)
                x = float(data.text)
            elif data.get('key') == 'd5':  # y координата (обычно latitude)
                y = float(data.text)
        if x is not None and y is not None:
            nodes[node_id] = (x, y)

    edges = []
    for edge in root.findall('.//g:edge', ns):
        source = edge.get('source')
        target = edge.get('target')
        street_name = None

        for data in edge.findall('.//g:data', ns):
            if data.get('key') == 'd18':  # название улицы
                street_name = data.text if data.text else None

        if source in nodes and target in nodes:
            edges.append((nodes[source], nodes[target], street_name))

    return nodes, edges

def find_street_index(edges: List[Tuple[Tuple[float, float], Tuple[float, float], str]], 
                        street_name_query: str) -> Tuple[int, str]:
    """
    Возвращает индекс (номер) и название улицы по заданному имени

    Args:
        edges: список рёбер с названиями улиц
        street_name_query: название улицы для поиска

    Returns:
        Кортеж (индекс, название_улицы), если найдено, иначе (-1, None)
    """
    for i, (_, _, name) in enumerate(edges):
        if name and name.lower() == street_name_query.lower():
            return i, name
    return -1, None

def visualize_path_with_network(nodes, edges, path, street_names=None, figsize=(20, 20)):
    """
    Визуализация всей дорожной сети + маршрута красным.
    Если передан список street_names, то названия улиц выводятся вдоль маршрута.
    """
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # Все рёбра — серые
    all_lines = [(start, end) for start, end, _ in edges]
    lc = LineCollection(all_lines, linewidths=0.3, colors='gray', alpha=0.4)
    ax.add_collection(lc)

    # Путь — красный
    if path and len(path) > 1:
        path_lines = [(path[i], path[i+1]) for i in range(len(path)-1)]
        lc_path = LineCollection(path_lines, linewidths=2.0, colors='red', alpha=0.9)
        ax.add_collection(lc_path)

        # Отображаем названия улиц, если они заданы
        if street_names:
            for i in range(len(path)-1):
                mid_point = ((path[i][0] + path[i+1][0]) / 2, (path[i][1] + path[i+1][1]) / 2)
                if i < len(street_names) and street_names[i]:
                    plt.text(mid_point[0], mid_point[1], street_names[i],
                            fontsize=8, color='blue', ha='center')

    ax.autoscale()
    plt.axis('equal')
    plt.title('Кратчайший маршрут')
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.grid(False)
    plt.tight_layout()
    plt.show()

def save_visualization(filename: str, dpi: int = 300) -> None:
    """
    Сохраняет текущую визуализацию в файл

    Args:
        filename: имя файла для сохранения
        dpi: разрешение изображения
    """
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close()


def visualize_only_path(path, figsize=(10, 10)):
    """
    Визуализирует только маршрут (без остального графа)
    """
    if not path or len(path) < 2:
        print("Маршрут слишком короткий или отсутствует.")
        return

    plt.figure(figsize=figsize)
    ax = plt.gca()

    path_lines = [(path[i], path[i+1]) for i in range(len(path)-1)]
    lc_path = LineCollection(path_lines, linewidths=2.5, colors='red', alpha=0.9)
    ax.add_collection(lc_path)

    ax.autoscale()
    plt.axis('equal')
    plt.title("Кратчайший маршрут")
    plt.xlabel("Долгота")
    plt.ylabel("Широта")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Функция для скачивания графа города
def download_city_graph(city_name: str, country: str = None, filename: str = None, network_type: str = 'drive'):
    """
    Скачивает граф дорожной сети города с OpenStreetMap и сохраняет в GraphML файл
    
    Args:
        city_name: название города
        country: название страны (опционально)
        filename: имя файла для сохранения (если None, генерируется автоматически)
        network_type: тип сети ('drive', 'walk', 'bike', 'all')
    
    Returns:
        путь к сохраненному файлу
    """
    # Формируем запрос для OSMnx
    if country:
        query = f'{city_name}, {country}'
    else:
        query = city_name
    
    print(f"Скачивание графа для: {query}")
    
    try:
        # Скачиваем граф
        G = ox.graph_from_place(query, network_type=network_type)
        
        # Генерируем имя файла, если не указано
        if filename is None:
            filename = f"{city_name.lower().replace(' ', '_')}_road_network.graphml"
        
        # Сохраняем граф в файл
        ox.save_graphml(G, filename)
        print(f"Граф сохранен в файл: {filename}")
        return filename
        
    except Exception as e:
        print(f"Ошибка при скачивании графа: {e}")
        return None


# Пример использования
if __name__ == "__main__":
    # Скачиваем граф Берлина
    print("=== Скачивание графа Берлина ===")
    graph_file = download_city_graph('Berlin', 'Germany', 'berlin_road_network.graphml')
    
    if graph_file is None:
        print("Не удалось скачать граф. Проверьте подключение к интернету.")
        exit(1)
    
    # 1. Загрузка данных из скачанного файла
    print(f"\n=== Загрузка графа из файла: {graph_file} ===")
    nodes, edges = read_graphml(graph_file)
    
    print(f"Загружено узлов: {len(nodes)}")
    print(f"Загружено ребер: {len(edges)}")
    
    # 2. Задаём названия улиц для начала и конца маршрута (для Берлина)
    # Можно использовать известные улицы Берлина
    start_street_query = "Unter den Linden"      # Известная улица в центре Берлина
    end_street_query = "Karl-Marx-Allee"          # Другая известная улица
    
    print(f"\nПоиск улиц:")
    print(f"Стартовая улица: {start_street_query}")
    print(f"Конечная улица: {end_street_query}")
    
    # 3. Используем find_street_index для определения нужных рёбер
    start_index, start_street = find_street_index(edges, start_street_query)
    end_index, end_street = find_street_index(edges, end_street_query)
    
    if start_index == -1:
        print(f"\nУлица '{start_street_query}' не найдена. Пробуем другие варианты...")
        # Пробуем альтернативные названия
        start_alternatives = ["Unter den Linden", "Friedrichstraße", "Alexanderplatz"]
        for alt in start_alternatives:
            start_index, start_street = find_street_index(edges, alt)
            if start_index != -1:
                print(f"Найдена улица: {start_street}")
                break
    
    if end_index == -1:
        print(f"Улица '{end_street_query}' не найдена. Пробуем другие варианты...")
        end_alternatives = ["Karl-Marx-Allee", "Frankfurter Allee", "Potsdamer Platz"]
        for alt in end_alternatives:
            end_index, end_street = find_street_index(edges, alt)
            if end_index != -1:
                print(f"Найдена улица: {end_street}")
                break
    
    if start_index == -1 or end_index == -1:
        print("\nНе удалось найти заданную улицу для начала или конца маршрута")
        print("Используем случайные точки из графа для демонстрации...")
        
        # Берем первые попавшиеся узлы из графа
        if nodes:
            node_list = list(nodes.values())
            if len(node_list) >= 2:
                start_node = node_list[0]
                end_node = node_list[len(node_list)//2]
                print(f"Стартовая точка: {start_node}")
                print(f"Конечная точка: {end_node}")
                
                # 4. Строим граф и ищем кратчайший путь
                graph = build_graph(edges)
                path, distance, street_names = dijkstra(graph, start_node, end_node)
                
                if path:
                    print(f"\nНайден путь длиной {distance:.2f} км")
                    print(f"Количество точек в пути: {len(path)}")
                    
                    # 5. Визуализация маршрута
                    visualize_path_with_network(nodes, edges, path, street_names)
                else:
                    print("Путь не найден")
    else:
        # 4. Определяем стартовый и конечный узлы:
        start_node = edges[start_index][0]
        end_node = edges[end_index][1]
        
        print(f"\nСтартовый узел: {start_node}")
        print(f"Конечный узел: {end_node}")
        
        # 5. Строим граф и ищем кратчайший путь
        print("\nПоиск кратчайшего пути...")
        graph = build_graph(edges)
        path, distance, street_names = dijkstra(graph, start_node, end_node)

        if not path:
            print("Путь не найден")
        else:
            print(f"\nНайден путь длиной {distance:.2f} км")
            print(f"Количество точек в пути: {len(path)}")
            print("Улицы на пути:", ", ".join(filter(None, street_names)) if street_names else "Названия улиц не доступны")

            # 6. Визуализация маршрута
            visualize_path_with_network(nodes, edges, path, street_names)
            
            # Сохраняем визуализацию (опционально)
            # save_visualization('berlin_shortest_path.png')