"""BFS의 현재 레이어 집합을 교체하며 마지막 레이어 크기 반환.

복잡도: O(n+e) time, O(n+e) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/49189/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import defaultdict

def solution(n, edge):
    # 이 구현의 선택: BFS의 현재 레이어 집합을 교체하며 마지막 레이어 크기 반환
    # 상태 정의: 1번에서 각 노드까지의 BFS 거리 배열을 유지한다.
    # 핵심 불변식: 큐에 처음 들어갈 때 기록한 거리는 1번에서 그 노드까지의 최단거리이다.
    graph = defaultdict(set)
    for left, right in edge:
        graph[left].add(right)
        graph[right].add(left)
    visited = {1}
    layer = {1}
    while layer:
        next_layer = set()
        for node in layer:
            next_layer.update(graph[node] - visited)
        if not next_layer:
            return len(layer)
        visited.update(next_layer)
        layer = next_layer
