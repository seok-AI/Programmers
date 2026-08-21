"""음수 간선이 없는 그래프의 Dijkstra 최단거리 참조 구현."""

import heapq
import math


def dijkstra(
    node_count: int, edges: list[list[int]], start: int, *, directed: bool = True
) -> list[float | int]:
    """[출발, 도착, 비용] 간선으로 start부터의 최단거리를 반환한다."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(node_count)]
    for source, target, cost in edges:
        if cost < 0:
            raise ValueError("Dijkstra는 음수 간선을 처리할 수 없습니다.")
        graph[source].append((target, cost))
        if not directed:
            graph[target].append((source, cost))

    distance: list[float | int] = [math.inf] * node_count
    distance[start] = 0
    heap: list[tuple[int, int]] = [(0, start)]
    while heap:
        current_distance, node = heapq.heappop(heap)
        # 더 짧은 경로가 이미 기록된 낡은 힙 항목은 확장하지 않는다.
        if current_distance != distance[node]:
            continue
        for neighbor, cost in graph[node]:
            candidate = current_distance + cost
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distance


if __name__ == "__main__":
    graph_edges = [[0, 1, 5], [0, 2, 1], [2, 1, 2], [1, 3, 1], [2, 3, 8]]
    assert dijkstra(4, graph_edges, 0) == [0, 3, 1, 4]
    print("Dijkstra 스니펫 자체 검증 PASS")
