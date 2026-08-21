"""각 선수에서 정방향·역방향 DFS로 비교 가능한 선수 집계.

복잡도: O(n*(n+e)) time, O(n+e) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/49191/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(n, results):
    # 이 구현의 선택: 각 선수에서 정방향·역방향 DFS로 비교 가능한 선수 집계
    # 상태 정의: win[a][b]를 a가 b를 이긴 사실이 직접 또는 간접으로 알려졌는지로 둔다.
    # 핵심 불변식: 중간 선수 k까지 반영한 뒤 행렬은 그 선수들을 경유하는 모든 승패 도달성을 포함한다.
    defeated = [[] for _ in range(n + 1)]
    defeated_by = [[] for _ in range(n + 1)]
    for winner, loser in results:
        defeated[winner].append(loser)
        defeated_by[loser].append(winner)

    def reachable(start, graph):
        seen = set()
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        return seen

    answer = 0
    for player in range(1, n + 1):
        known = reachable(player, defeated) | reachable(player, defeated_by)
        known.discard(player)  # 승패 순환이 있어도 자기 자신은 비교 대상이 아니다.
        answer += len(known) == n - 1
    return answer
