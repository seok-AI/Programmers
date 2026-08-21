"""좌표를 2배 확대해 사각형 테두리만 남긴 뒤 BFS.

복잡도: O(C^2) time, O(C^2) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import deque

def solution(rectangle, characterX, characterY, itemX, itemY):
    # 이 구현의 선택: 좌표를 2배 확대해 사각형 테두리만 남긴 뒤 BFS
    # 상태 정의: 좌표를 두 배로 키운 격자에서 합성 직사각형의 외곽선 칸만 통로로 둔다.
    # 핵심 불변식: 내부 칸은 어떤 직사각형의 변과 겹쳐도 다시 통로가 되지 않으며 BFS는 외곽선만 지난다.
    grid = [[0] * 102 for _ in range(102)]
    for x1, y1, x2, y2 in rectangle:
        x1, y1, x2, y2 = 2 * x1, 2 * y1, 2 * x2, 2 * y2
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if x1 < x < x2 and y1 < y < y2:
                    grid[x][y] = 2  # 내부는 이후 다른 사각형의 변도 지나갈 수 없다.
                elif grid[x][y] != 2:
                    grid[x][y] = 1
    start = (2 * characterX, 2 * characterY)
    target = (2 * itemX, 2 * itemY)
    queue = deque([(start[0], start[1], 0)])
    visited = {start}
    while queue:
        x, y, distance = queue.popleft()
        if (x, y) == target:
            return distance // 2
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_point = (x + dx, y + dy)
            if grid[next_point[0]][next_point[1]] == 1 and next_point not in visited:
                visited.add(next_point)
                queue.append((next_point[0], next_point[1], distance + 1))
