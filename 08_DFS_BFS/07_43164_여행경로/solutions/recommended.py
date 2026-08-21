"""도착지를 최소 힙으로 관리하는 Hierholzer 오일러 경로.

복잡도: O(e log e) time, O(e) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import defaultdict
import heapq

def solution(tickets):
    # 이 구현의 선택: 도착지를 최소 힙으로 관리하는 Hierholzer 오일러 경로
    # 상태 정의: 현재 탐색 경로 스택과 더 갈 항공권이 없는 정점부터 쌓는 역방향 route를 둔다.
    # 핵심 불변식: route에 빠진 공항 뒤에는 남은 미사용 항공권이 없으므로 오일러 경로의 뒤쪽이 확정된다.
    graph = defaultdict(list)
    for departure, arrival in tickets:
        heapq.heappush(graph[departure], arrival)
    stack = ["ICN"]
    route = []
    while stack:
        airport = stack[-1]
        if graph[airport]:
            stack.append(heapq.heappop(graph[airport]))
        else:
            route.append(stack.pop())
    return route[::-1]
