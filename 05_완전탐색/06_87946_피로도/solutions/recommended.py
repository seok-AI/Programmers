"""방문 배열을 되돌리는 DFS로 가능한 순서 탐색.

복잡도: O(n!) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(k, dungeons):
    # 이 구현의 선택: 방문 배열을 되돌리는 DFS로 가능한 순서 탐색
    # 상태 정의: 현재 피로도, 방문한 던전 집합, 지금까지 방문 수를 DFS 상태로 둔다.
    # 핵심 불변식: 재귀 경로에서 방문 표시는 그 경로가 선택한 던전과 정확히 일치한다.
    visited = [False] * len(dungeons)
    best = 0

    def explore(fatigue, count):
        nonlocal best
        best = max(best, count)
        for index, (required, cost) in enumerate(dungeons):
            if not visited[index] and fatigue >= required:
                visited[index] = True
                explore(fatigue - cost, count + 1)
                visited[index] = False

    explore(k, 0)
    return best
