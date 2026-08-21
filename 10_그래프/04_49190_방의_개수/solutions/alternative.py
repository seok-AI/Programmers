"""확대 경로 그래프의 V-E+F 관계로 방 개수 계산.

복잡도: O(a) time, O(a) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/49190/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(arrows):
    # 이 구현의 선택: 확대 경로 그래프의 V-E+F 관계로 방 개수 계산
    # 상태 정의: 방향 이동을 두 반걸음으로 나누고 방문 정점과 무방향 간선을 따로 기록한다.
    # 핵심 불변식: 이미 방문한 정점에 처음 쓰는 간선으로 들어갈 때 정확히 하나의 새 방이 생긴다.
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    current = (0, 0)
    vertices = {current}
    edges = set()
    for arrow in arrows:
        dx, dy = directions[arrow]
        for _ in range(2):
            neighbor = (current[0] + dx, current[1] + dy)
            vertices.add(neighbor)
            edges.add(frozenset((current, neighbor)))
            current = neighbor
    # 연결 평면 그래프에서 내부 면의 수 = E - V + 1.
    return len(edges) - len(vertices) + 1
