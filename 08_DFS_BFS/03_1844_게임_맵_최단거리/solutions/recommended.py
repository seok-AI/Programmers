"""시작점부터 레벨 순서 BFS로 최단거리 탐색.

복잡도: O(n*m) time, O(n*m) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import deque

def solution(maps):
    # 이 구현의 선택: 시작점부터 레벨 순서 BFS로 최단거리 탐색
    # 상태 정의: 큐에는 시작점에서의 최단거리가 확정된 칸과 그 거리를 둔다.
    # 핵심 불변식: BFS에서 처음 방문한 순간의 거리가 가중치 1인 격자의 최단거리이다.
    height, width = len(maps), len(maps[0])
    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while queue:
        row, column, distance = queue.popleft()
        if (row, column) == (height - 1, width - 1):
            return distance
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row, next_column = row + dr, column + dc
            if 0 <= next_row < height and 0 <= next_column < width and maps[next_row][next_column] == 1 and (next_row, next_column) not in visited:
                visited.add((next_row, next_column))
                queue.append((next_row, next_column, distance + 1))
    return -1
