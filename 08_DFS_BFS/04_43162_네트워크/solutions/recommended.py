"""방문하지 않은 컴퓨터마다 DFS를 시작해 연결요소 계산.

복잡도: O(n^2) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(n, computers):
    # 이 구현의 선택: 방문하지 않은 컴퓨터마다 DFS를 시작해 연결요소 계산
    # 상태 정의: 방문한 컴퓨터 집합과 현재 DFS가 덮는 하나의 연결요소를 구분한다.
    # 핵심 불변식: DFS가 끝나면 시작 컴퓨터와 경로로 연결된 모든 컴퓨터가 방문 상태이다.
    visited = [False] * n
    networks = 0
    for start in range(n):
        if visited[start]:
            continue
        networks += 1
        stack = [start]
        visited[start] = True
        while stack:
            node = stack.pop()
            for neighbor, connected in enumerate(computers[node]):
                if connected and not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
    return networks
