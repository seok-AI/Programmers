"""무가중 그래프와 격자 BFS의 최소 참조 구현."""

from collections import deque


def graph_distances(node_count: int, edges: list[list[int]], start: int) -> list[int]:
    """0..node_count-1 정점의 무방향 그래프에서 start까지 간선 수를 반환한다."""
    graph = [[] for _ in range(node_count)]
    for left, right in edges:
        graph[left].append(right)
        graph[right].append(left)

    distance = [-1] * node_count
    distance[start] = 0
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] != -1:
                continue
            # 처음 큐에 넣는 순간이 start에서 neighbor까지의 최단거리다.
            distance[neighbor] = distance[node] + 1
            queue.append(neighbor)
    return distance


def grid_distance(board: list[list[int]]) -> int:
    """1인 칸만 지나 (0,0)에서 우하단까지 가는 칸 수, 불가능하면 -1."""
    rows, columns = len(board), len(board[0])
    queue = deque([(0, 0)])
    distance = [[-1] * columns for _ in range(rows)]
    distance[0][0] = 1
    while queue:
        row, column = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, column + dc
            if not (0 <= nr < rows and 0 <= nc < columns):
                continue
            if board[nr][nc] == 0 or distance[nr][nc] != -1:
                continue
            distance[nr][nc] = distance[row][column] + 1
            queue.append((nr, nc))
    return distance[-1][-1]


if __name__ == "__main__":
    assert graph_distances(4, [[0, 1], [1, 2], [0, 3]], 0) == [0, 1, 2, 1]
    assert grid_distance([[1, 1, 0], [0, 1, 1]]) == 4
    print("BFS 스니펫 자체 검증 PASS")
