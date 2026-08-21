"""대각선 교차를 잡도록 이동을 2분할하고 새 간선의 재방문 정점 집계.

복잡도: O(a) time, O(a) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(arrows):
    # 이 구현의 선택: 대각선 교차를 잡도록 이동을 2분할하고 새 간선의 재방문 정점 집계
    # 상태 정의: 방향 이동을 두 반걸음으로 나누고 방문 정점과 무방향 간선을 따로 기록한다.
    # 핵심 불변식: 이미 방문한 정점에 처음 쓰는 간선으로 들어갈 때 정확히 하나의 새 방이 생긴다.
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    point = (0, 0)
    vertices = {point}
    edges = set()
    rooms = 0
    for arrow in arrows:
        dx, dy = directions[arrow]
        for _ in range(2):
            next_point = (point[0] + dx, point[1] + dy)
            edge_key = (point, next_point)
            reverse_key = (next_point, point)
            if next_point in vertices and edge_key not in edges:
                rooms += 1
            vertices.add(next_point)
            edges.add(edge_key)
            edges.add(reverse_key)
            point = next_point
    return rooms
