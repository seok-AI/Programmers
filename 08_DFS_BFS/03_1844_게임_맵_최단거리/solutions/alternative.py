"""거리 배열을 방문 표시로 겸용하는 BFS.

복잡도: O(n*m) time, O(n*m) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/1844/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque

def solution(maps):
    # 이 구현의 선택: 거리 배열을 방문 표시로 겸용하는 BFS
    # 상태 정의: 큐에는 시작점에서의 최단거리가 확정된 칸과 그 거리를 둔다.
    # 핵심 불변식: BFS에서 처음 방문한 순간의 거리가 가중치 1인 격자의 최단거리이다.
    height, width = len(maps), len(maps[0])
    distance = [[-1] * width for _ in range(height)]
    distance[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        row, column = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row, next_column = row + dr, column + dc
            if 0 <= next_row < height and 0 <= next_column < width and maps[next_row][next_column] and distance[next_row][next_column] == -1:
                distance[next_row][next_column] = distance[row][column] + 1
                queue.append((next_row, next_column))
    return distance[-1][-1]
