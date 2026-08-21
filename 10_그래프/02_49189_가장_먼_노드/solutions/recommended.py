"""1번 노드부터 BFS 거리 계산 후 최댓값 빈도 집계.

복잡도: O(n+e) time, O(n+e) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import deque

def solution(n, edge):
    # 이 구현의 선택: 1번 노드부터 BFS 거리 계산 후 최댓값 빈도 집계
    # 상태 정의: 1번에서 각 노드까지의 BFS 거리 배열을 유지한다.
    # 핵심 불변식: 큐에 처음 들어갈 때 기록한 거리는 1번에서 그 노드까지의 최단거리이다.
    graph = [[] for _ in range(n + 1)]
    for left, right in edge:
        graph[left].append(right)
        graph[right].append(left)
    distance = [-1] * (n + 1)
    distance[1] = 0
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    farthest = max(distance)
    return distance.count(farthest)
