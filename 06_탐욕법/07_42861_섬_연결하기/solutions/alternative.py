"""현재 트리와 연결되는 최소 간선을 고르는 Prim MST.

복잡도: O(e log e) time, O(n+e) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42861/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

import heapq

def solution(n, costs):
    # 이 구현의 선택: 현재 트리와 연결되는 최소 간선을 고르는 Prim MST
    # 상태 정의: 각 섬의 연결요소 대표를 Union-Find로 관리한다.
    # 핵심 불변식: 선택한 간선은 사이클이 없고, 처리한 비용 이하 간선으로 만들 수 있는 최소 신장 숲이다.
    graph = [[] for _ in range(n)]
    for left, right, cost in costs:
        graph[left].append((cost, right))
        graph[right].append((cost, left))
    visited = [False] * n
    heap = [(0, 0)]
    total = count = 0
    while heap and count < n:
        cost, node = heapq.heappop(heap)
        if visited[node]:
            continue
        visited[node] = True
        total += cost
        count += 1
        for next_cost, neighbor in graph[node]:
            if not visited[neighbor]:
                heapq.heappush(heap, (next_cost, neighbor))
    return total
