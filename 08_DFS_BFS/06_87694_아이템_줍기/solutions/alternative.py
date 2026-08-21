"""각 격자점이 합성 도형의 외곽선인지 직접 판정 후 BFS.

복잡도: O(C^2*r) time, O(C^2) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/87694/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque

def solution(rectangle, characterX, characterY, itemX, itemY):
    # 이 구현의 선택: 각 격자점이 합성 도형의 외곽선인지 직접 판정 후 BFS
    # 상태 정의: 좌표를 두 배로 키운 격자에서 합성 직사각형의 외곽선 칸만 통로로 둔다.
    # 핵심 불변식: 내부 칸은 어떤 직사각형의 변과 겹쳐도 다시 통로가 되지 않으며 BFS는 외곽선만 지난다.
    doubled = [[2 * value for value in rect] for rect in rectangle]

    def boundary(x, y):
        on_edge = any(
            x1 <= x <= x2 and y1 <= y <= y2 and (x in (x1, x2) or y in (y1, y2))
            for x1, y1, x2, y2 in doubled
        )
        inside = any(x1 < x < x2 and y1 < y < y2 for x1, y1, x2, y2 in doubled)
        return on_edge and not inside

    start = (2 * characterX, 2 * characterY)
    target = (2 * itemX, 2 * itemY)
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (x, y), distance = queue.popleft()
        if (x, y) == target:
            return distance // 2
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_point = (x + dx, y + dy)
            if 0 <= next_point[0] <= 100 and 0 <= next_point[1] <= 100 and next_point not in visited and boundary(*next_point):
                visited.add(next_point)
                queue.append((next_point, distance + 1))
