"""도착지를 역정렬한 스택으로 관리하는 Hierholzer 경로.

복잡도: O(e log e) time, O(e) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/43164/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import defaultdict

def solution(tickets):
    # 이 구현의 선택: 도착지를 역정렬한 스택으로 관리하는 Hierholzer 경로
    # 상태 정의: 현재 탐색 경로 스택과 더 갈 항공권이 없는 정점부터 쌓는 역방향 route를 둔다.
    # 핵심 불변식: route에 빠진 공항 뒤에는 남은 미사용 항공권이 없으므로 오일러 경로의 뒤쪽이 확정된다.
    graph = defaultdict(list)
    for departure, arrival in sorted(tickets, reverse=True):
        graph[departure].append(arrival)
    path, route = ["ICN"], []
    while path:
        while graph[path[-1]]:
            path.append(graph[path[-1]].pop())
        route.append(path.pop())
    return route[::-1]
